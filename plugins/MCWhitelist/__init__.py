import discord
from discord.ext import commands
from Globals import PRIMARY_GUILD, VERIFIED_ROLE
from Plugin import AutomataPlugin
from plugins.MCWhitelist.mojang_api import MOJANG_API_BASE, MojangAPI
from plugins.MCWhitelist.whitelist_http_api import WhitelistHttpApi


class MCWhitelist(AutomataPlugin):
    """Provides Minecraft account whitelisting for MUNCS Craft."""

    def __init__(self, manifest, bot: commands.Bot):
        super().__init__(manifest, bot)
        self.whitelist_http_api = WhitelistHttpApi()

    async def cog_load(self):
        self.whitelisted_accounts = (
            self.bot.database.automata.mcwhitelist_whitelisted_accounts
        )
        self.disallowed_members = (
            self.bot.database.automata.mcwhitelist_disallowed_members
        )
        self.mojang_api = MojangAPI(self.bot.database.automata.mojangapi_profile_cache)
        await self.mojang_api.ensure_collection_expiry()

    async def get_whitelisted_account(self, member):
        query = {"discord_id": member.id}
        return await self.whitelisted_accounts.find_one(query)

    async def is_minecraft_account_already_associated(self, username):
        whitelist = await self.whitelist_http_api.whitelist()
        return any(entry["name"] == username for entry in whitelist)

    async def is_disallowed(self, member):
        query = {"discord_id": member.id}
        return await self.disallowed_members.find_one(query) is not None

    async def remove_whitelisted_account(self, ctx, whitelisted_account):
        username = whitelisted_account["minecraft_username"]
        await self.whitelist_http_api.remove(username)
        await self.whitelisted_accounts.delete_many({"discord_id": ctx.author.id})

    async def account_embed(self, whitelisted_account):
        embed = discord.Embed()

        profile = await self.mojang_api.profile_from_uuid(
            whitelisted_account["minecraft_uuid"]
        )

        if profile is not None:
            skin_url = self.mojang_api.skin_url_from_profile(profile)
            if skin_url is not None:
                embed.set_image(url=skin_url)

        username = whitelisted_account["minecraft_username"]
        embed.colour = discord.Colour.dark_green()
        embed.add_field(name="Minecraft Username", value=username)
        return embed

    @commands.group()
    async def whitelist(self, ctx: commands.Context):
        """Manage the MUNCS Craft server whitelist."""
        if not ctx.invoked_subcommand:
            whitelisted_account = await self.get_whitelisted_account(ctx.author)
            if whitelisted_account is not None:
                embed = await self.account_embed(whitelisted_account)
                await ctx.send(embed=embed)
            else:
                await ctx.send(
                    "You don't have a Minecraft account associated with yourself yet, run !whitelist add <username>."
                )

    @whitelist.command(name="add")
    async def whitelist_add(self, ctx: commands.Context, username: str):
        """Add users to the MUNCS Craft servers whitelist."""
        if await self.is_disallowed(ctx.author):
            await ctx.send(
                f"You are disallowed from being added to the MUNCS Craft whitelist."
            )
            return

        whitelisted_account = await self.get_whitelisted_account(ctx.author)
        if whitelisted_account is not None:
            username = whitelisted_account["minecraft_username"]
            await ctx.send(
                f"You already have the Minecraft account '{username}' associated with your Discord account, run !whitelist remove first to change/add a different one."
            )
            return

        verified_role = self.bot.get_guild(PRIMARY_GUILD).get_role(VERIFIED_ROLE)
        if verified_role not in ctx.author.roles:
            await ctx.send(
                "You must first verify your MUN account using !identity before adding yourself to the whitelist."
            )
            return

        mojang_resp = await self.mojang_api.info_from_username(username)
        if mojang_resp is None:
            await ctx.send(
                f"Error verifying username '{username}' from Mojang, are you sure you typed it correctly?"
            )
            return

        if await self.is_minecraft_account_already_associated(username):
            await ctx.send(
                f"Username '{username}' is already on the whitelist, reach out to an executive to resolve this issue."
            )
            return

        await self.whitelist_http_api.add(username)

        new_whitelisted_account = {
            "discord_id": ctx.author.id,
            "minecraft_username": username,
            "minecraft_uuid": mojang_resp["id"],
        }
        await self.whitelisted_accounts.insert_one(new_whitelisted_account)

        embed = await self.account_embed(new_whitelisted_account)
        await ctx.send("Minecraft account whitelisted!", embed=embed)

    @whitelist.command(name="remove")
    async def whitelist_remove(self, ctx: commands.Context):
        """Remove users from the MUNCS Craft servers whitelist."""
        whitelisted_account = await self.get_whitelisted_account(ctx.author)
        if whitelisted_account is None:
            await ctx.send(
                f"You don't have the Minecraft account to remove, run !whitelist add <username> first."
            )
            return

        await self.remove_whitelisted_account(ctx, whitelisted_account)
        username = whitelisted_account["minecraft_username"]
        await ctx.send(f"Minecraft account '{username}' removed from the whitelist.")

    @whitelist.command(name="disallow")
    @commands.has_permissions(view_audit_log=True)
    async def whitelist_disallow(self, ctx: commands.Context, user: discord.Member):
        """Disallow users from adding themselves to the MUNCS Craft whitelist."""
        if await self.is_disallowed(user):
            await ctx.send("User already disallowed.")
            return

        whitelisted_account = await self.get_whitelisted_account(user)
        if whitelisted_account is not None:
            await self.remove_whitelisted_account(ctx, whitelisted_account)
            await ctx.send("User now disallowed, and removed from the whitelist.")
        else:
            await ctx.send("User now disallowed.")

        await self.disallowed_members.insert_one({"discord_id": user.id})

    @whitelist.command(name="allow")
    @commands.has_permissions(view_audit_log=True)
    async def whitelist_allow(self, ctx: commands.Context, user: discord.Member):
        """Allows users to add themselves to the MUNCS Craft whitelist, if previously disallowed."""
        if not await self.is_disallowed(user):
            await ctx.send("User already allowed.")
            return

        await self.disallowed_members.delete_many({"discord_id": user.id})
        await ctx.send("User now allowed.")

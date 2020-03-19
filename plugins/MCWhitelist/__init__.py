import discord
from discord.ext import commands
import requests

from Plugin import AutomataPlugin
from Globals import mongo_client

MOJANG_API_BASE = "https://api.mojang.com"


class MojangAPI:
    """https://wiki.vg/Mojang_API"""

    username_base = f"{MOJANG_API_BASE}/users/profiles/minecraft"

    def info_from_username(self, username):
        try:
            return requests.get(f"{MojangAPI.username_base}/{username}").json()
        except:
            return None


class MCWhitelist(AutomataPlugin):
    """Provides Minecraft account whitelisting for MUNCS Craft."""

    def __init__(self, manifest, bot: commands.Bot):
        super().__init__(manifest, bot)

        self.whitelisted_accounts = (
            mongo_client.automata.mcwhitelist_whitelisted_accounts
        )
        self.mojang_api = MojangAPI()

    async def get_whitelisted_account(self, member):
        query = {"discord_id": member.id}
        return await self.whitelisted_accounts.find_one(query)

    @commands.group()
    async def whitelist(self, ctx: commands.Context):
        """Manage the MUNCS Craft server whitelist."""
        if not ctx.invoked_subcommand:
            whitelisted_account = await self.get_whitelisted_account(ctx.author)
            if whitelisted_account:
                username = whitelisted_account["minecraft_username"]
                embed = discord.Embed()
                embed.colour = discord.Colour.dark_green()
                embed.add_field(name="Minecraft Username", value=username)
                await ctx.send(embed=embed)
            else:
                await ctx.send(
                    "You don't have a Minecraft account associated with yourself yet, run !whitelist add <username>."
                )

    @whitelist.command(name="add")
    async def whitelist_add(self, ctx: commands.Context, username: str):
        """Add users to the MUNCS Craft servers whitelist."""
        whitelisted_account = await self.get_whitelisted_account(ctx.author)
        if whitelisted_account:
            username = whitelisted_account["minecraft_username"]
            await ctx.send(
                f"You already have the Minecraft account '{username}' associated with your Discord account, run !whitelist remove first to change/add a different one."
            )
            return

        mojang_resp = self.mojang_api.info_from_username(username)

        if not mojang_resp:
            await ctx.send(
                f"Error verifying username '{username}' from Mojang, are you sure you typed your username correctly?"
            )
            return

        # TODO if name good, actually whitelist

        await self.whitelisted_accounts.insert_one(
            {
                "discord_id": ctx.author.id,
                "minecraft_username": username,
                "minecraft_uuid": mojang_resp["id"],
            }
        )

        await ctx.send("Minecraft account whitelisted!")

    @whitelist.command(name="remove")
    async def whitelist_remove(self, ctx: commands.Context):
        """Remove users from the MUNCS Craft servers whitelist."""
        whitelisted_account = await self.get_whitelisted_account(ctx.author)
        if not whitelisted_account:
            await ctx.send(
                f"You don't have the Minecraft account to remove, run !whitelist add <usernmae> first."
            )
            return

        username = whitelisted_account["minecraft_username"]

        # TODO actually remove from whitelist

        await self.whitelisted_accounts.delete_many({"discord_id": ctx.author.id})

        await ctx.send(f"Minecraft account '{username}' removed from the whitelist.")

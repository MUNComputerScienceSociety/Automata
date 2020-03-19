import asyncio
import json
from base64 import b64decode
from datetime import datetime

import requests
import discord
from discord.ext import commands

from Plugin import AutomataPlugin
from Globals import mongo_client, VERIFIED_ROLE, PRIMARY_GUILD

MOJANG_API_BASE = "https://api.mojang.com"
MOJANG_SESSIONSERVER_BASE = "https://sessionserver.mojang.com"


class MojangAPI:
    """https://wiki.vg/Mojang_API"""

    username_base = f"{MOJANG_API_BASE}/users/profiles/minecraft"
    profile_base = f"{MOJANG_SESSIONSERVER_BASE}/session/minecraft/profile"

    def __init__(self):
        self.profile_cache = mongo_client.automata.mojangapi_profile_cache

        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.ensure_collection_expiry())

    async def ensure_collection_expiry(self):
        await self.profile_cache.create_index(
            "datetime", expireAfterSeconds=900  # 15 minutes
        )

    def info_from_username(self, username):
        try:
            return requests.get(f"{MojangAPI.username_base}/{username}").json()
        except:
            return None

    async def profile_from_uuid(self, uuid):
        cached = await self.profile_cache.find_one({"uuid": uuid})

        if cached:
            return cached["data"]

        try:
            resp = requests.get(f"{MojangAPI.profile_base}/{uuid}").json()
        except:
            return None

        await self.profile_cache.insert_one(
            {"datetime": datetime.utcnow(), "uuid": uuid, "data": resp}
        )
        return resp

    def skin_url_from_profile(self, profile):
        if (not profile) and (not profile["properties"]):
            return None

        textures_encoded = next(
            x for x in profile["properties"] if x["name"] == "textures"
        )

        if not textures_encoded:
            return None

        textures = json.loads(b64decode(textures_encoded["value"]))

        if (not textures["textures"]) and (not textures["SKIN"]):
            return None

        return textures["textures"]["SKIN"]["url"]


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

    async def account_embed(self, whitelisted_account):
        embed = discord.Embed()

        profile = await self.mojang_api.profile_from_uuid(
            whitelisted_account["minecraft_uuid"]
        )

        if profile:
            skin_url = self.mojang_api.skin_url_from_profile(profile)
            if skin_url:
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
            if whitelisted_account:
                embed = await self.account_embed(whitelisted_account)
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

        verified_role = self.bot.get_guild(PRIMARY_GUILD).get_role(VERIFIED_ROLE)

        if verified_role not in ctx.author.roles:
            await ctx.send(
                "You must first verify your MUN account using !identity before adding yourself to the whitelist."
            )
            return

        mojang_resp = self.mojang_api.info_from_username(username)

        if not mojang_resp:
            await ctx.send(
                f"Error verifying username '{username}' from Mojang, are you sure you typed your username correctly?"
            )
            return

        # TODO actually whitelist

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
        if not whitelisted_account:
            await ctx.send(
                f"You don't have the Minecraft account to remove, run !whitelist add <usernmae> first."
            )
            return

        username = whitelisted_account["minecraft_username"]

        # TODO actually remove from whitelist

        await self.whitelisted_accounts.delete_many({"discord_id": ctx.author.id})

        await ctx.send(f"Minecraft account '{username}' removed from the whitelist.")

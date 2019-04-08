import time
from datetime import timezone

import discord
from discord.ext import commands
import requests

from Plugin import AutomataPlugin
from DB import client


class MUNIdentity(AutomataPlugin):
    """Provides identity validation and management services."""

    def __init__(self, manifest, bot: commands.Bot):
        super().__init__(manifest, bot)
        self.identities = client.automata.munidentity_identities

    async def on_member_join(member: discord.Member):
        await member.send(f"Welcome to the MUN Computer Science Society Discord server, {member.mention}.\nIf you have a MUN account, please visit https://auth.muncompsci.ca to verify yourself.\nOtherwise, contact an executive to gain further access.")

    @commands.group()
    async def identity(self, ctx: commands.Context):
        """Manage identity validation."""
        if not ctx.invoked_subcommand:
            identity = await self.identities.find_one({"discord_id": ctx.author.id})
            if identity is not None:
                embed = discord.Embed()
                embed.colour = discord.Colour.green()
                embed.set_footer(text="Identity verified.")
                embed.add_field(name="MUN Username", value=identity["mun_username"])
                await ctx.send(embed=embed)
            else:
                await ctx.send("You have not yet verified your identity. Please go to https://auth.muncompsci.ca to verify.")

    @identity.command(name="verify")
    async def identity_verify(self, ctx: commands.Context, code: str):
        """Verify your identity."""
        resp = requests.get(f"https://auth.muncompsci.ca/identity/{code}")
        if resp.status_code == requests.codes.ok:
            username = resp.text
            await self.identities.insert_one({"discord_id": ctx.author.id, "mun_username": username})
            await ctx.author.add_roles(self.bot.get_guild(514110851016556567).get_role(564672793380388873), reason=f"Identity verified. MUN username: {username}")
            await ctx.send("Identity verified!")
        else:
            await ctx.send("It appears that code is invalid. Please double-check that you copied all characters from the site, and try again.")

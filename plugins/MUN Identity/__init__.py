from typing import Optional, Union, Dict

import discord
from discord.ext import commands
import requests

from Plugin import AutomataPlugin
from Globals import mongo_client


class MUNIdentity(AutomataPlugin):
    """Provides identity validation and management services."""

    def __init__(self, manifest, bot: commands.Bot):
        super().__init__(manifest, bot)
        self.identities = mongo_client.automata.munidentity_identities

    async def get_identity(self, *, member: Union[discord.User, int] = None,
                           mun_username: str = None) -> Optional[Dict[str, Union[str, int]]]:
        """Retrieve identity details for a given user.

        :param member: The Discord server member to retrieve details for, defaults to None
        :param member: Union[discord.Member, int], optional
        :param mun_username: The MUN username to retrieve details for, defaults to None
        :param mun_username: str, optional
        :return: The data stored about the user's identity
        :rtype: Optional[Dict[str, Union[str, int]]]
        """
        if isinstance(member, int):
            member_id = member
        elif member is not None:
            member_id = member.id
        query = {}
        if member is not None:
            query["discord_id"] = member_id
        if mun_username is not None:
            query["mun_username"] = mun_username
        identity = await self.identities.find_one(query)
        return identity

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        await member.send(f"Welcome to the MUN Computer Science Society Discord server, {member.mention}.\nIf you have a MUN account, please visit https://discord.muncompsci.ca/auth to verify yourself.\nOtherwise, contact an executive to gain further access.")

    @commands.group()
    async def identity(self, ctx: commands.Context):
        """Manage identity validation."""
        if not ctx.invoked_subcommand:
            identity = await self.get_identity(member=ctx.author)
            if identity is not None:
                embed = discord.Embed()
                embed.colour = discord.Colour.green()
                embed.add_field(name="MUN Username", value=identity["mun_username"])
                await ctx.send(embed=embed)
            else:
                await ctx.send("You have not yet verified your identity. Please go to https://discord.muncompsci.ca/auth to verify.")

    @identity.command(name="verify")
    async def identity_verify(self, ctx: commands.Context, code: str):
        """Verify your identity."""
        current_identity = await self.get_identity(member=ctx.author)
        if current_identity is not None:
            await ctx.author.add_roles(self.bot.get_guild(514110851016556567).get_role(564672793380388873), reason=f"Identity verified. MUN username: {current_identity['mun_username']}")
            await ctx.send("Your identity is already verified. If for some reason you need to change your verified username, contact an executive.")
            return
        resp = requests.get(f"https://discord.muncompsci.ca/identity/{code}")
        if resp.status_code == requests.codes.ok:
            username = resp.text
            current_identity = await self.get_identity(mun_username=username)
            if current_identity is not None:
                await ctx.send("An existing user is already verified with that username. If you have lost access to a previous account, contact an executive.")
                return
            await self.identities.insert_one({
                "discord_id": ctx.author.id,
                "mun_username": username
            })
            await ctx.author.add_roles(self.bot.get_guild(514110851016556567).get_role(564672793380388873), reason=f"Identity verified. MUN username: {username}")
            await ctx.send("Identity verified!")
        else:
            await ctx.send("It appears that code is invalid. Please double-check that you copied all characters from the site, and try again.")

    @identity.command(name="check")
    @commands.has_permissions(view_audit_log=True)
    async def identity_check(self, ctx: commands.Context, user: discord.Member):
        """Check the identity verification status of a user."""
        identity = await self.identities.find_one({"discord_id": user.id})
        if identity is not None:
            embed = discord.Embed()
            embed.colour = discord.Colour.green()
            embed.add_field(name="MUN Username", value=identity["mun_username"])
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed()
            embed.colour = discord.Colour.red()
            embed.add_field(name="MUN Username", value="No username verified.")
            await ctx.send(embed=embed)

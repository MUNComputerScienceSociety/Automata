import asyncio
from datetime import datetime
from typing import Dict, List, Optional, Union

import httpx
import nextcord
from Globals import DISCORD_AUTH_URI, PRIMARY_GUILD, VERIFIED_ROLE, mongo_client
from nextcord.ext import commands
from Plugin import AutomataPlugin
from pymongo import CursorType


class MUNIdentity(AutomataPlugin):
    """Provides identity validation and management services."""

    def __init__(self, manifest, bot: commands.Bot):
        super().__init__(manifest, bot)

        self.identities = mongo_client.automata.munidentity_identities

    async def get_identity(
        self, *, member: Union[nextcord.User, int] = None, mun_username: str = None
    ) -> Optional[Dict[str, Union[str, int]]]:
        """Retrieve identity details for a given user.

        :param member: The Discord server member to retrieve details for, defaults to None
        :param member: Union[nextcord.Member, int], optional
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
    async def on_member_join(self, member: nextcord.Member):
        await member.send(
            f"Welcome to the MUN Computer Science Society Discord server, {member.mention}.\nIf you have a MUN account, please visit https://discord.muncompsci.ca/auth to verify yourself.\nOtherwise, contact an executive to gain further access."
        )

    @commands.group()
    async def identity(self, ctx: commands.Context):
        """Manage identity validation."""
        if not ctx.invoked_subcommand:
            identity = await self.get_identity(member=ctx.author)
            if identity is not None:
                embed = nextcord.Embed()
                embed.colour = nextcord.Colour.green()
                embed.add_field(name="MUN Username", value=identity["mun_username"])
                await ctx.send(embed=embed)
            else:
                await ctx.send(
                    "You have not yet verified your identity. Please go to https://discord.muncompsci.ca/auth to verify."
                )

    @identity.command(name="verify")
    async def identity_verify(self, ctx: commands.Context, code: str):
        """Verify your identity."""
        current_identity = await self.get_identity(member=ctx.author)
        if current_identity is not None:
            await self.bot.get_guild(PRIMARY_GUILD).get_member(ctx.author.id).add_roles(
                self.bot.get_guild(PRIMARY_GUILD).get_role(VERIFIED_ROLE),
                reason=f"Identity verified. MUN username: {current_identity['mun_username']}",
            )
            await ctx.send(
                "Your identity is already verified. If for some reason you need to change your verified username, contact an executive."
            )
            return
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{DISCORD_AUTH_URI}/identity/{code}")
        if resp.status_code == httpx.codes.OK:
            username = resp.text
            current_identity = await self.get_identity(mun_username=username)
            if current_identity is not None:
                await ctx.send(
                    "An existing user is already verified with that username. If you have lost access to a previous account, contact an executive."
                )
                return
            await self.identities.insert_one(
                {"discord_id": ctx.author.id, "mun_username": username}
            )
            await self.bot.get_guild(PRIMARY_GUILD).get_member(ctx.author.id).add_roles(
                self.bot.get_guild(PRIMARY_GUILD).get_role(VERIFIED_ROLE),
                reason=f"Identity verified. MUN username: {username}",
            )
            await ctx.send("Identity verified!")
        else:
            await ctx.send(
                "It appears that code is invalid. Please double-check that you copied all characters from the site, and try again."
            )

    @identity.command(name="check")
    @commands.has_permissions(view_audit_log=True)
    async def identity_check(self, ctx: commands.Context, user: nextcord.Member):
        """Check the identity verification status of a user."""
        identity = await self.identities.find_one({"discord_id": user.id})
        if identity is not None:
            embed = nextcord.Embed()
            embed.colour = nextcord.Colour.green()
            embed.add_field(name="MUN Username", value=identity["mun_username"])
            await ctx.send(embed=embed)
        else:
            embed = nextcord.Embed()
            embed.colour = nextcord.Colour.red()
            embed.add_field(name="MUN Username", value="No username verified.")
            await ctx.send(embed=embed)

    @identity.command(name="remove")
    @commands.has_permissions(manage_messages=True)
    async def identity_remove(self, ctx: commands.Context, user: nextcord.Member):
        """Remove the identity from a user."""
        identity = await self.get_identity(member=user)
        if identity is not None:
            await self.identities.delete_one({"discord_id": user.id})
            await self.bot.get_guild(PRIMARY_GUILD).get_member(user.id).remove_roles(
                self.bot.get_guild(PRIMARY_GUILD).get_role(VERIFIED_ROLE),
                reason=f"Identity manually removed by {ctx.author.name}#{ctx.author.discriminator}. MUN username: {identity['mun_username']}",
            )
            embed = nextcord.Embed()
            embed.colour = nextcord.Colour.green()
            embed.add_field(
                name="MUN Username",
                value=f"User `{user.name}#{user.discriminator}` with username `{identity['mun_username']}` was removed.",
            )
            await ctx.send(embed=embed)
        else:
            embed = nextcord.Embed()
            embed.colour = nextcord.Colour.red()
            embed.add_field(
                name="MUN Username", value="No username verified for the given user."
            )
            await ctx.send(embed=embed)

    @identity.command(name="associate")
    @commands.has_permissions(manage_messages=True)
    async def identity_associate(
        self, ctx: commands.Context, user: nextcord.Member, mun_username: str
    ):
        """Manually associate a Discord account to a MUN username."""
        identity = await self.get_identity(member=user)
        if identity is not None:
            await ctx.send(
                "Specified Discord user already has a MUN username associated with their account."
            )
            return

        identity = await self.get_identity(mun_username=mun_username)
        if identity is not None:
            await ctx.send(
                "Specified MUN username is already associated with a Discord user."
            )
            return

        await self.identities.insert_one(
            {"discord_id": user.id, "mun_username": mun_username}
        )
        await self.bot.get_guild(PRIMARY_GUILD).get_member(user.id).add_roles(
            self.bot.get_guild(PRIMARY_GUILD).get_role(VERIFIED_ROLE),
            reason=f"Identity manually associated by {ctx.author.name}#{ctx.author.discriminator}. MUN username: {mun_username}",
        )
        await ctx.send("Identity associated.")

    @identity.command(name="disassociate")
    async def identity_disassociate(self, ctx: commands.Context):
        """Disassociate your own identity from your discord account."""
        current_identity = await self.get_identity(member=ctx.author)
        if current_identity is None:
            await ctx.reply("You don't have an identity associated with your account.")
            return
        embed = nextcord.Embed()
        embed.colour = nextcord.Colour.red()
        embed.add_field(
            name="Identity Disassociation",
            value=f"Are you sure you want to disassociate your identity from your account?",
        )
        message = await ctx.reply(embed=embed)
        confirmed = await self.get_confirmation(ctx, message)
        if not confirmed:
            await ctx.reply("Disassociation cancelled.")
            return
        await self.identities.delete_one({"discord_id": ctx.author.id})
        await self.bot.get_guild(PRIMARY_GUILD).get_member(ctx.author.id).remove_roles(
            self.bot.get_guild(PRIMARY_GUILD).get_role(VERIFIED_ROLE),
            reason=f"Identity manually disassociated by {ctx.author.name}#{ctx.author.discriminator}.",
        )
        embed = nextcord.Embed()
        embed.colour = nextcord.Colour.green()
        embed.add_field(
            name="Disassociation",
            value=f"Your identity has been disassociated from your account.",
        )
        await ctx.reply(embed=embed)

    @staticmethod
    async def get_confirmation(
        ctx: commands.Context, message: nextcord.Message
    ) -> bool:
        """Get confirmation from user executing the command by reactions."""
        await message.add_reaction("✅")
        await message.add_reaction("❌")

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ["✅", "❌"]

        try:
            reaction, _ = await ctx.bot.wait_for(
                "reaction_add", check=check, timeout=30
            )
        except asyncio.TimeoutError:
            return False
        else:
            if reaction.emoji == "✅":
                return True
            elif reaction.emoji == "❌":
                return False

    @identity.command(name="restore_roles")
    @commands.has_permissions(view_audit_log=True)
    async def identity_restore_roles(self, ctx: commands.Context):
        """Restores VERIFIED_ROLE to users with a registered identity who were not granted it."""
        members_restored: List[nextcord.Member] = []
        identities = self.identities.find({})
        async with ctx.typing():
            while await identities.fetch_next:
                identity = identities.next_object()
                member: nextcord.Member = self.bot.get_guild(PRIMARY_GUILD).get_member(
                    identity["discord_id"]
                )
                if member is None:
                    await asyncio.sleep(1)
                    continue
                has_role = any(role.id == VERIFIED_ROLE for role in member.roles)
                if has_role:
                    await asyncio.sleep(1)
                    continue
                await member.add_roles(
                    self.bot.get_guild(PRIMARY_GUILD).get_role(VERIFIED_ROLE),
                    reason=f"Identity restored by {ctx.author.name}#{ctx.author.discriminator}.",
                )
                members_restored.append(member)
                await asyncio.sleep(1)
            embed = nextcord.Embed()
            embed.colour = nextcord.Colour.green()
            embed.add_field(
                name="Restore Roles",
                value=f"{len(members_restored)} roles restored to verified users.",
            )
            await ctx.send(embed=embed)

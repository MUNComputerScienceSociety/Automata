import discord
from discord.ext import commands

from Plugin import AutomataPlugin
from Globals import mongo_client


class PrivateChannels(AutomataPlugin):
    """Provides private channel creation and management services."""

    def __init__(self, manifest, bot: commands.Bot):
        super().__init__(manifest, bot)
        self.channels = mongo_client.automata.privatechannels_channels

    @commands.group()
    @commands.has_role("Verified MUN Account")
    async def privatechannel(self, ctx: commands.Context):
        """Manage private channels."""
        if not ctx.invoked_subcommand:
            await ctx.send("Invalid subcommand provided. Please use `!help privatechannel` for more help.")

    @privatechannel.command(name="create")
    async def privatechannel_create(self, ctx: commands.Context, name: str):
        """Create a new private channel."""
        channels = await self.channels.find({"creator": ctx.author.id}).to_list(10)
        if len(channels) > 5:
            await ctx.send("You already have the maximum number of private channels.")
            return
        if any(channel.name == name for channel in ctx.guild.channels):
            await ctx.send("A channel already exists with that name.")
            return
        channel = await ctx.guild.create_text_channel(
            name,
            overwrites={
                ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                ctx.author: discord.PermissionOverwrite(read_messages=True, manage_roles=True)
            },
            category=[c for c in ctx.guild.channels if c.id == 565681623199252480][0],
            reason=f"Created private channel for {ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})"
        )
        await self.channels.insert_one({
            "creator": ctx.author.id,
            "channel_id": channel.id,
            "channel_name": channel.name
        })
        await ctx.send("Channel created. You have been granted \"Manage Permissions\" permissions for the channel to enable the inviting of new users. ***DO NOT*** remove or modify the default permissions that were already set. Doing so will result in the deletion of your channel.")

    @privatechannel.command(name="delete")
    async def privatechannel_delete(self, ctx: commands.Context, name: str):
        """Delete a private channel."""
        channel = await self.channels.find_one({"channel_name": name})
        if channel is None:
            await ctx.send("That private channel does not exist.")
            return
        if channel["creator"] != ctx.author.id:
            await ctx.send("You are not the creator of that channel.")
            return
        await ctx.guild.get_channel(channel["channel_id"]).delete(reason=f"Deleted by owner ({ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id}))")
        await self.channels.delete_many({"channel_name": name})
        await ctx.send("Channel deleted.")

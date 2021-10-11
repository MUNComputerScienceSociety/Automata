from os import name
from discord import colour
from discord.ext import commands
from discord.ext.commands import context
from Globals import ANNOUNCEMENT_CHANNEL

from Plugin import AutomataPlugin
import discord

class Announce(AutomataPlugin):
    """Announcement feature for a better announcements formatting"""

    @commands.command()
    @commands.has_permissions(view_audit_log=True)
    async def announce(self, ctx: commands.Context):
        """
        Send an embed in #announcements with an @-everyone ping with the current message content.
        Before the message is posted it is previewed in the current channel, with a reaction the author can invoke for it to be posted properly.
        You can add up to one image by uploading an image with the message.
        """

        message = ctx.message
        announcement_channel = await ctx.bot.fetch_channel(ANNOUNCEMENT_CHANNEL)
        announcement_message = " ".join(message.content.split(' ')[1: len(ctx.message.content)])

        embed = discord.Embed(
            colour = discord.Color.blue()
        )

        embed.set_author(name=message.author.name, icon_url=message.author.avatar_url)
        embed.set_footer(text="MUN Computer Science Society", icon_url=message.guild.icon_url)

        if len(announcement_message) > 1:
            embed.add_field(name="Announcement", value=announcement_message, inline=False)

        if len(message.attachments) > 0:
            attachment = message.attachments[0]
            embed.set_image(url=attachment.url)

        announcement_message = await ctx.send(embed = embed)

        await announcement_message.add_reaction("✅")

        def check(reaction, user):
            return user == message.author and str(reaction.emoji) == "✅" and reaction.message == announcement_message

        try:
            reaction, user = await ctx.bot.wait_for('reaction_add', check=check)
        except:
            await ctx.send('Discarded')
        else:
            await announcement_channel.send(
                embed = embed,
                content = "@everyone"
            )
            await ctx.send("Announcement Sent ✅")

        

from os import name
from discord import colour
from discord.ext import commands

from Plugin import AutomataPlugin
import discord

class Announce(AutomataPlugin):
    """Announcement feature for a better announcements formmating, hopefully.."""

    @commands.command()
    @commands.has_permissions(view_audit_log=True)
    async def announce(self, ctx: commands.Context):
        """Send an embed with everyone ping of the current message content. You can add up to one image by uploading an image with the message."""

        message = ctx.message
        announcement_message = " ".join(message.content.split(' ')[1: len(ctx.message.content)])

        embed = discord.Embed(
            colour = discord.Color.blue()
        )

        embed.set_author(name= message.author.name, icon_url=message.author.avatar_url)
        embed.set_footer(text="MUN Computer Science Society", icon_url=message.guild.icon_url)

        if len(announcement_message) > 1:
            embed.add_field(name="Announcement", value=announcement_message, inline=False)

        if len(message.attachments) > 0:
            attachment = message.attachments[0]
            embed.set_image(url=attachment.url)

        await ctx.send(embed = embed, content="@everyone")

        await message.delete()
        

import io
from typing import Any, Mapping, Optional

import discord
from discord.ext import commands

type CommandContext = commands.Context[commands.Bot]


class Plugin(commands.Cog):
    bot: commands.Bot

    def __init__(self, bot: commands.Bot):
        self.bot = bot


async def send_code_block_maybe_as_file(ctx: CommandContext, text: str):
    """
    Sends a code block to the current context.

    If it's too long to fit in a single message, it will
    instead be sent as a file.
    """
    if len(text) > 2000:
        file = io.StringIO()
        file.writelines(text)
        file.seek(0)

        await ctx.send(file=discord.File(file, filename="agenda.md"))
    else:
        await ctx.send(f"```{text}```")


class CustomHelp(commands.DefaultHelpCommand):
    """Custom help command"""

    async def send_bot_help(
        self,
        mapping: Mapping[Optional[commands.Cog], list[commands.Command[Any, Any, Any]]],
    ):
        """Shows a list of commands"""
        embed = discord.Embed(title="Commands Help")
        embed.colour = discord.Colour.blurple()
        for cog, commands in mapping.items():
            command_signatures = [self.get_command_signature(c) for c in commands]
            if command_signatures:
                cog_name = getattr(cog, "qualified_name", "No Category")
                embed.add_field(
                    name=cog_name, value="\n".join(command_signatures), inline=False
                )
        channel = self.get_destination()
        await channel.send(embed=embed)

    async def send_command_help(self, command: commands.Command[Any, Any, Any]):
        """Shows how to use each command"""
        embed_command = discord.Embed(
            title=self.get_command_signature(command), description=command.help
        )
        embed_command.colour = discord.Colour.green()
        channel = self.get_destination()
        await channel.send(embed=embed_command)

    async def send_group_help(self, group: commands.Group[Any, Any, Any]):
        """Shows how to use each group of commands"""
        embed_group = discord.Embed(
            title=self.get_command_signature(group), description=group.short_doc
        )
        for c in group.walk_commands():
            embed_group.add_field(name=c, value=c.short_doc, inline=False)
        embed_group.colour = discord.Colour.yellow()
        channel = self.get_destination()
        await channel.send(embed=embed_group)

    async def send_cog_help(self, cog: commands.Cog):
        """Shows how to use each category"""
        embed_cog = discord.Embed(title=cog.qualified_name, description=cog.description)
        comms = cog.get_commands()
        for c in comms:
            embed_cog.add_field(name=c, value=c.short_doc, inline=False)
        embed_cog.colour = discord.Colour.green()
        channel = self.get_destination()
        await channel.send(embed=embed_cog)

    async def send_error_message(self, error: str):
        """Shows if command does not exist"""
        embed_error = discord.Embed(title="Error", description=error)
        embed_error.colour = discord.Colour.red()
        channel = self.get_destination()
        await channel.send(embed=embed_error)

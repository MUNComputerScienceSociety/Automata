import logging
from typing import Any, cast

import discord
from discord.ext import commands

import automata.plugins as plugins
from automata.config import config
from automata.utils import CommandContext, CustomHelp

intents = discord.Intents.default()
intents.message_content = True
intents.members = config.member_intents_enabled


class Automata(commands.Bot):
    async def setup_hook(self) -> None:
        for plugin in plugins.enabled_plugins:
            await self.add_cog(plugin(self))


bot = Automata(
    command_prefix="!",
    description="A custom, multi-purpose moderation bot for the MUN Computer Science Society Discord server.",
    intents=intents,
    help_command=CustomHelp(),
)

logger = logging.getLogger(__name__)


@bot.event
async def on_message(message: discord.Message):
    if isinstance(message.channel, discord.DMChannel):
        name = message.author.name
    else:
        channel = cast(discord.TextChannel, message.channel)
        name = channel.name

    logger.info(f"[{name}] {message.author.name}: {message.content}")

    await bot.process_commands(message)


if config.sentry_dsn:

    @bot.event
    async def on_error(event: str, *args: Any, **kwargs: Any):
        raise

    @bot.event
    async def on_command_error(ctx: CommandContext, exception: commands.CommandError):
        raise exception


__all__ = ["bot"]

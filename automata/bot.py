import logging
from typing import cast

import discord
from discord.ext import commands

from automata.config import config

intents = discord.Intents.default()
intents.message_content = True
intents.members = config.member_intents_enabled

bot = commands.Bot(
    command_prefix="!",
    description="A custom, multi-purpose moderation bot for the MUN Computer Science Society Discord server.",
    intents=intents,
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


__all__ = ["bot"]

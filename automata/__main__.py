import logging

from automata.bot import bot
from automata.config import config

IGNORED_LOGGERS = [
    "asyncio",
    "discord.client",
    "discord.gateway",
    "discord.gateway",
    "discord.http",
    "discord.state",
    "websockets.protocol",
]

# Configure logger and silence ignored loggers
logging.basicConfig(
    format="{%(asctime)s} (%(name)s) [%(levelname)s]: %(message)s",
    datefmt="%x, %X",
    level=logging.DEBUG,
)

for logger in IGNORED_LOGGERS:
    logging.getLogger(logger).setLevel(logging.WARNING)

bot.run(config.token)

import logging

import sentry_sdk

from automata.bot import bot
from automata.config import config

IGNORED_LOGGERS = [
    "asyncio",
    "discord.client",
    "discord.gateway",
    "discord.gateway",
    "discord.http",
    "discord.state",
    "httpcore.connection",
    "httpcore.http11",
    "httpx",
    "pymongo.command",
    "pymongo.connection",
    "pymongo.serverSelection",
    "pymongo.topology",
    "urllib3",
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

if config.sentry_dsn:
    sentry_sdk.init(config.sentry_dsn)

bot.run(config.token)

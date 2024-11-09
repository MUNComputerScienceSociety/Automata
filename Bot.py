import logging
import os
from pathlib import Path

import discord
import motor.motor_asyncio
from discord.ext import commands
from dotenv import load_dotenv
from jigsaw.PluginLoader import PluginLoader

load_dotenv()

from Globals import (
    DISABLED_PLUGINS,
    ENABLED_PLUGINS,
    MONGO_ADDRESS,
)
from Plugin import AutomataPlugin
from Utils import CustomHelp

IGNORED_LOGGERS = [
    "discord.client",
    "discord.gateway",
    "discord.state",
    "discord.gateway",
    "discord.http",
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

logger = logging.getLogger("Automata")

AUTOMATA_TOKEN = os.getenv("AUTOMATA_TOKEN", None)

if not AUTOMATA_TOKEN:
    logger.error(
        "AUTOMATA_TOKEN environment variable not set, have you created a .env file and populated it yet?"
    )
    exit(1)

intents = discord.Intents.default()
intents.message_content = True
intents.members = os.getenv("AUTOMATA_MEMBER_INTENTS_ENABLED", "True") == "True"


class Automata(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, intents=intents, **kwargs)

    async def setup_hook(self) -> None:
        self.database = motor.motor_asyncio.AsyncIOMotorClient(MONGO_ADDRESS)
        self.loop.create_task(self.enable_plugins())

    async def enable_plugins(self) -> None:
        for plugin in loader.get_all_plugins():
            if plugin["plugin"]:
                await plugin["plugin"].enable()


bot = Automata(
    command_prefix="!",
    help_command=CustomHelp(),
    description="A custom, multi-purpose moderation bot for the MUN Computer Science Society Discord server.",
)


@bot.command()
async def plugins(ctx: commands.Context):
    """Lists all enabled plugins."""
    embed = discord.Embed()
    embed.colour = discord.Colour.blurple()

    for plugin in loader.get_all_plugins():
        if plugin["plugin"]:
            embed.add_field(
                name=plugin["manifest"]["name"],
                value="{}\nVersion: {}\nAuthor: {}".format(
                    plugin["plugin"].__doc__.rstrip(),
                    plugin["manifest"]["version"],
                    plugin["manifest"]["author"],
                ),
            )

    await ctx.send(embed=embed)


plugins_dir = Path("./plugins")
mounted_plugins_dir = Path("./mounted_plugins")
mounted_plugins_dir.mkdir(exist_ok=True)

loader = PluginLoader(
    plugin_paths=(str(plugins_dir), str(mounted_plugins_dir)),
    plugin_class=AutomataPlugin,
)
loader.load_manifests()

num_of_disabled = 0

for plugin in loader.get_all_plugins():
    manifest = plugin["manifest"]
    if len(ENABLED_PLUGINS) > 0:
        if manifest["main_class"] in ENABLED_PLUGINS:
            loader.load_plugin(manifest, bot)
        else:
            num_of_disabled += 1
    else:
        if manifest["main_class"] not in DISABLED_PLUGINS:
            loader.load_plugin(manifest, bot)
        else:
            logger.info(f"{manifest['name']} disabled.")
            num_of_disabled += 1

logger.info(f"{num_of_disabled} plugins disabled.")


bot.run(AUTOMATA_TOKEN)

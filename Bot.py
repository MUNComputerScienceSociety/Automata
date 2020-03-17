from dotenv import load_dotenv

load_dotenv()

import os
import logging
import traceback
import contextlib
import sys
from pathlib import Path
from io import StringIO

from jigsaw.PluginLoader import PluginLoader
import discord
from discord.ext import commands
from prometheus_async.aio.web import start_http_server

from Plugin import AutomataPlugin

from Globals import DISABLED_PLUGINS

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

bot = commands.Bot(
    "!",
    description="A custom, multi-purpose moderation bot for the MUN Computer Science Society Discord server.",
)


@bot.event
async def on_message(message):
    # Log messages
    if isinstance(message.channel, discord.DMChannel):
        name = message.author.name
    else:
        name = message.channel.name
    logger.info(f"[{name}] {message.author.name}: {message.content}")
    await bot.process_commands(message)


@bot.event
async def on_ready():
    # When the bot is ready, start the prometheus client
    await start_http_server(port=9000)


if os.getenv("SENTRY_DSN", None):

    @bot.event
    async def on_error(event, *args, **kwargs):
        raise

    @bot.event
    async def on_command_error(ctx, exception):
        raise exception


@contextlib.contextmanager
def stdioreader():
    old = (sys.stdout, sys.stderr)
    stdout = StringIO()
    stderr = StringIO()
    sys.stdout = stdout
    sys.stderr = stderr
    yield stdout, stderr
    sys.stdout = old[0]
    sys.stderr = old[1]


@bot.command(name="eval")
@commands.is_owner()
async def eval_code(ctx: commands.Context, code: str):
    """Evaluates code for debugging purposes."""
    try:
        result = f"```\n{eval(code)}\n```"
        colour = discord.Colour.green()
    except:
        result = f"```py\n{traceback.format_exc(1)}```"
        colour = discord.Colour.red()

    result.replace("\\", "\\\\")

    embed = discord.Embed()
    embed.add_field(name=code, value=result)
    embed.colour = colour

    await ctx.send(embed=embed)


@bot.command(name="exec")
@commands.is_owner()
async def exec_code(ctx: commands.Context, code: str):
    """Executes code for debugging purposes."""
    with stdioreader() as (out, err):
        try:
            exec(code)
            result = f"```\n{out.getvalue()}\n```"
            colour = discord.Colour.green()
        except:
            result = f"```py\n{traceback.format_exc(1)}```"
            colour = discord.Colour.red()

    result.replace("\\", "\\\\")

    embed = discord.Embed()
    embed.add_field(name=code, value=result)
    embed.colour = colour

    await ctx.send(embed=embed)


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

for plugin in loader.get_all_plugins():
    manifest = plugin["manifest"]
    if not manifest["main_class"] in DISABLED_PLUGINS:
        loader.load_plugin(manifest, bot)
    else:
        logger.info(f"{manifest['name']} disabled.")

bot.run(AUTOMATA_TOKEN)

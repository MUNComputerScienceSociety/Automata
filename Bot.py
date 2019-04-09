import os
import logging
import traceback
import contextlib
import sys
from io import StringIO

from jigsaw.PluginLoader import PluginLoader
import discord
from discord.ext import commands

from Plugin import AutomataPlugin

import Globals

IGNORED_LOGGERS = [
    "discord.client",
    "discord.gateway",
    "discord.state",
    "discord.gateway",
    "discord.http",
    "websockets.protocol"
]

# Configure logger and silence ignored loggers
logging.basicConfig(format="{%(asctime)s} (%(name)s) [%(levelname)s]: %(message)s",
                    datefmt="%x, %X",
                    level=logging.DEBUG)

for logger in IGNORED_LOGGERS:
    logging.getLogger(logger).setLevel(logging.WARNING)

logger = logging.getLogger("Automata")

bot = commands.Bot("!", description="A custom, multi-purpose moderation bot for the MUN Computer Science Society Discord server.")


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
        embed.add_field(
            name=plugin["manifest"]["name"],
            value="{}\nVersion: {}\nAuthor: {}".format(
                plugin['plugin'].__doc__.rstrip(),
                plugin['manifest']['version'],
                plugin['manifest']['author']
            )
        )

    await ctx.send(embed=embed)


loader = PluginLoader(
    plugin_paths=("/app/plugins", "/app/mounted_plugins"),
    plugin_class=AutomataPlugin
)
loader.load_manifests()
loader.load_plugins(bot)
loader.enable_all_plugins()

bot.run(os.environ["AUTOMATA_TOKEN"])

from dotenv import load_dotenv

from Utils import CustomHelp

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
from typing import Optional, Literal

from Globals import (
    DISABLED_PLUGINS,
    ENABLED_PLUGINS,
    PRIMARY_GUILD,
)

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
        await self.enable_plugins()

    async def enable_plugins(self) -> None:
        for plugin in loader.get_all_plugins():
            if plugin["plugin"]:
                await plugin["plugin"].enable()


bot = Automata(
    command_prefix="!",
    help_command=CustomHelp(),
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


@bot.command()
@commands.guild_only()
@commands.has_permissions(view_audit_log=True)
async def sync(
    ctx: commands.Context,
    guilds: commands.Greedy[discord.Object],
    spec: Optional[Literal["~", "*", "^"]] = None,
) -> None:
    """Sync application commands to guild(s).
    `~` - sync current guild application commands.
    `*` - Copy all global application commands to current guild and sync.
    `^` - Clear all application commands from current guild and sync.
    `` - Sync all guilds application commands globally.
    guilds - Sync application commands to guild(s).
    """
    if not guilds:
        if spec == "~":
            # sync current guild
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "*":
            # copies all global app commands to current guild and syncs
            ctx.bot.tree.copy_global_to(guild=ctx.guild)
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "^":
            # clears all commands from the current guild target and syncs (removes guild commands)
            ctx.bot.tree.clear_commands(guild=ctx.guild)
            await ctx.bot.tree.sync(guild=ctx.guild)
            synced = []
        else:
            # global sync
            synced = await ctx.bot.tree.sync()
        await ctx.send(
            f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
        )
        return
    # syncs guilds with id 1 and 2
    ret = 0
    for guild in guilds:
        try:
            await ctx.bot.tree.sync(guild=guild)
        except discord.HTTPException:
            pass
        else:
            ret += 1
    await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")


bot.run(AUTOMATA_TOKEN)

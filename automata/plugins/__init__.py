from discord.ext import commands

from automata.config import config

from .lmgtfy import LMGTFY
from .number_facts import NumberFacts

all_plugins: list[type[commands.Cog]] = [LMGTFY, NumberFacts]

enabled_plugins = [
    plugin for plugin in all_plugins if config.should_enable_plugin(plugin)
]

__all__ = ["enabled_plugins"]

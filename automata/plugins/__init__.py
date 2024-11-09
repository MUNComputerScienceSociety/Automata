from discord.ext import commands

from automata.config import config
from automata.utils import Plugin

from .agenda import Agenda
from .binary import Binary
from .brainf import Brainf
from .executive_docs import ExecutiveDocs
from .faq import FAQ
from .fortune_cookie import FortuneCookie
from .instant_answer import InstantAnswer
from .lmgtfy import LMGTFY
from .man import Man
from .number_facts import NumberFacts
from .starboard import Starboard

all_plugins: list[type[Plugin]] = [
    Agenda,
    Binary,
    Brainf,
    ExecutiveDocs,
    FAQ,
    FortuneCookie,
    InstantAnswer,
    LMGTFY,
    Man,
    NumberFacts,
    Starboard,
]

enabled_plugins = [
    plugin for plugin in all_plugins if config.should_enable_plugin(plugin)
]

__all__ = ["enabled_plugins"]

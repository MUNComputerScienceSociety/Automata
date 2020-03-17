import logging

from jigsaw import JigsawPlugin

from discord.ext.commands import Cog

logger = logging.getLogger("Automata - Plugin")


class AutomataPlugin(JigsawPlugin, Cog):
    def __init__(self, manifest, bot):
        JigsawPlugin.__init__(self, manifest)
        Cog.__init__(self)
        self.bot = bot
        self.enabled = True

    def enable(self):
        if hasattr(self, "bot"):
            self.bot.add_cog(self)
        else:
            self.enabled = False
            logger.info(f"{self.__class__.__name__} disabled.")

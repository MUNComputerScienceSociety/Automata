from jigsaw import JigsawPlugin

from nextcord.ext.commands import Cog, Bot


class AutomataPlugin(JigsawPlugin, Cog):
    def __init__(self, manifest, bot: Bot):
        JigsawPlugin.__init__(self, manifest)
        Cog.__init__(self)
        self.bot = bot

    def enable(self):
        self.bot.add_cog(self)

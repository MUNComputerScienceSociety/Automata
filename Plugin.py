from jigsaw import JigsawPlugin

from nextcord.ext.commands import Cog


class AutomataPlugin(JigsawPlugin, Cog):
    def __init__(self, manifest, bot):
        JigsawPlugin.__init__(self, manifest)
        Cog.__init__(self)
        self.bot = bot

    def enable(self):
        self.bot.add_cog(self)

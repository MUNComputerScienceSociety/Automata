from jigsaw import JigsawPlugin

from discord.ext.commands import Cog, Bot


class AutomataPlugin(JigsawPlugin, Cog):
    def __init__(self, manifest, bot: Bot):
        JigsawPlugin.__init__(self, manifest)
        Cog.__init__(self)
        self.bot = bot

    async def enable(self):
        await self.bot.add_cog(self)

from jigsaw import JigsawPlugin


class AutomataPlugin(JigsawPlugin):

    def __init__(self, manifest, bot):
        super().__init__(manifest)
        self.bot = bot

    def enable(self):
        self.bot.add_cog(self)

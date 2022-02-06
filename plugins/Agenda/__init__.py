from nextcord.ext import commands

from Plugin import AutomataPlugin
from Globals import mongo_client

class Agenda(AutomataPlugin):
    """Handles tracking agenda items, and exporting them as markdown"""

    def __init__(self, manifest, bot: commands.Bot):
        super().__init__(manifest, bot)

        self.agenda_items = mongo_client.automata.agenda_items

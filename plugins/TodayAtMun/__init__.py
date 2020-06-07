import discord
from os import path
from discord.ext import commands
from plugins.TodayAtMun.Month import month
from datetime import datetime


from Plugin import AutomataPlugin


class TodayAtMun(AutomataPlugin):
    """
        Provides Significant Dates on the Mun Calendar
    """

    def __init__(self, manifest, bot):
        super().__init__(manifest, bot)
        with open(path.join(self.manifest["path"], "diary.txt"), "r") as f:
            self.info = f

    @commands.command()
    async def getCurrDate(self, ctx):
        date = str(datetime.now().strftime("%Y-%#m-%#d"))

        dice = date.split("-")

        currYear = dice[0]
        currMonth = int(dice[1])
        currDay = dice[2]

        lookUp = f"{month[currMonth]} {currDay}, {currYear}"

        await ctx.send(lookUp)

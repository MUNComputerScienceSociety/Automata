import discord
from os import path
from discord.ext import commands
from plugins.TodayAtMun.Month import month
from datetime import datetime
from datetime import timedelta
from json import load
from Plugin import AutomataPlugin
from Bot import bot


class TodayAtMun(AutomataPlugin):
    """
        Provides Brief Info Of Significant Dates on the Mun Calendar
    """

    def __init__(self, manifest, bot):
        super().__init__(manifest, bot)
        self.date = None
        with open(path.join(self.manifest["path"], "diary.json"), "r") as f:
            self.info = load(f)

    def set_current_date(self):
        # self.date = str(datetime.now().strftime("%Y-%#m-%#d-%A")).split("-")
        self.date = datetime.now().strftime("%Y-%#m-%#d-%A")

    def format_date(self):
        """ 
        Provides Current Date formatted to Muns style.
            params: none
            returns: string of the current day
        """
        temp = self.date.split("-")
        currYear = temp[0]
        currMonth = int(temp[1])
        currDay = temp[2]
        currDayOfWeek = temp[3]

        return f"{month[currMonth]} {currDay}, {currYear}, {currDayOfWeek}"

    def nextDay(self):
        self.date += timedelta(days=1)
        print(self.date)
        return self.date

    @commands.command()
    async def today(self, ctx):
        """ Provides the significant event on the mun calendar """
        self.set_current_date()
        self.date = self.format_date()
        print(f"Today is: {self.date}.")
        # Appears Sunday is never in the Mun diary ( could change )
        if self.date.endswith("Sunday"):
            await ctx.send("Nothing on Sundays")
        else:
            for key in self.info:
                if key == self.date:
                    embed = discord.Embed(
                        title=self.date,
                        description=f"{key}",
                        color=discord.Colour.red(),
                    )
                    await ctx.send(embed)
                    return
            self.nextDay()

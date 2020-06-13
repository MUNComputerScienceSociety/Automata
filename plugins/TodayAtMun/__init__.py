import discord
from discord.ext import commands
from plugins.TodayAtMun.Month import month
from datetime import datetime
from datetime import timedelta
from json import load
from Plugin import AutomataPlugin
from Bot import bot
from plugins.TodayAtMun.diary_parser import diary_parser
from pathlib import Path


class TodayAtMun(AutomataPlugin):
    """
        Provides Brief Info Of Significant Dates on the Mun Calendar
    """

    def __init__(self, manifest, bot):
        super().__init__(manifest, bot)
        self.result = ""
        path = Path(__file__).parent
        file_name = path / "diary.json"
        with open(file_name, "r") as f:
            self.info = load(f)
        self.set_current_date()

    def set_current_date(self):
        """ Current Day, Month, Hour, second """
        self.date = datetime.now()

    def format_date(self, date):
        """Provides Current Date formatted to Muns style."""
        temp = date.strftime("%Y-%#m-%#d-%A").split("-")
        currYear = temp[0]
        currMonth = int(temp[1])
        currDay = temp[2]
        currDayOfWeek = temp[3]

        return f"{month[currMonth]} {currDay}, {currYear}, {currDayOfWeek}"

    def nextDay(self):
        """Increases Day By One """
        self.date = self.date + timedelta(days=1)
        return self.date

    def findEvent(self, date):
        """ Provides the significant event on the mun calendar """
        self.fdate = self.format_date(self.date)
        for key in self.info:
            if key == self.fdate:
                self.infoDay = self.info[key]
                return

        self.findEvent(self.nextDay())

    @commands.command()
    async def today(self, ctx, arg=None):
        """ 
        Sends quick update on Muns Next Calendar Date on the Uni Diary
            
        args:
            reset - resets the data from Muns Diary.
            "" - default to the function
                
        """
        if arg == "reset":
            diary_parser()
            await ctx.send("Data Reset.")
            return

        self.set_current_date()
        self.findEvent(self.date)
        embed = discord.Embed(
            title=f"{self.format_date(self.date)}",
            description=f"```{self.infoDay}```",
            url="https://www.mun.ca/regoff/calendar/sectionNo=GENINFO-0086",
            colour=discord.Colour.orange(),
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def varietyToday(self, ctx, arg=1):
        """
        Sends (n) amounts of dates coming up on the univsersity diary
        """
        pass
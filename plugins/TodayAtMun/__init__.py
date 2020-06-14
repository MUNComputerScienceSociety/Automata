import discord
from discord.ext import commands
from Plugin import AutomataPlugin
from Bot import bot
from plugins.TodayAtMun.diary_parser import diary_parser
from plugins.TodayAtMun.today import Today


class TodayAtMun(AutomataPlugin):
    """
        Provides Brief Info Of Significant Dates on the Mun Calendar
    """

    def __init__(self, manifest, bot):
        super().__init__(manifest, bot)
        self.result = ""
        self.ins_Today = Today()
        self.ins_Today.set_current_date()

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

        self.ins_Today.set_current_date()
        self.ins_Today.findEvent(self.ins_Today.date)
        embed = discord.Embed(
            title=f"{self.ins_Today.format_date(self.ins_Today.date)}",
            description=f"```{self.ins_Today.infoDay}```",
            url="https://www.mun.ca/regoff/calendar/sectionNo=GENINFO-0086",
            colour=discord.Colour.orange(),
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def varietyToday(self, ctx, arg=1):
        """
        Sends (n) amounts of dates coming up on the univsersity diary
        """
        self.ins_Today.set_current_date()
        self.ins_Today.findEvent(self.date)
        self.ins_Today.goToEvent()
        self.set = iter(self.info)
        for i in range(arg):
            setOfDates = next(self.set)
            await ctx.send(setOfDates)

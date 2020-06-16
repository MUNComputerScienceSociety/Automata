import discord
from discord.ext import commands

from Bot import bot
from Plugin import AutomataPlugin
from plugins.TodayAtMun.diary_parser import diary_parser
from plugins.TodayAtMun.today import Today


class TodayAtMun(AutomataPlugin):
    def __init__(self, manifest, bot):
        super().__init__(manifest, bot)
        self.Tod = Today()

    @commands.group()
    async def today(self, ctx):
        """ Provides Brief Info Of Significant Dates on the Mun Calendar"""
        if not ctx.invoked_subcommand:
            await ctx.send("Please Provide Subcommand e.g !today [soon]")

    @today.command(name="next")
    async def today_next(self, ctx):
        # Sends quick update on Muns Next Calendar Date on the Uni Diary
        self.Tod.set_current_date()
        self.Tod.findEvent(self.Tod.date)
        embed = discord.Embed(
            title=f"{self.Tod.format_date(self.Tod.date)}",
            description=f"```{self.Tod.infoDay}``` ( !today later ) to get next event",
            url="https://www.mun.ca/regoff/calendar/sectionNo=GENINFO-0086",
            colour=discord.Colour.orange(),
        )
        await ctx.send(embed=embed)

    @today.command(name="reset")
    async def today_reset(self, ctx):
        # Re-Parses data from Mun Diary.
        diary_parser()
        await ctx.send("Data Reset!")

    @today.command(name="later")
    async def today_after(self, ctx):
        # Sends next date coming up on the univsersity diary
        self.Tod.set_current_date()
        self.Tod.findEvent(self.Tod.date)
        self.Tod.nextDay()
        self.Tod.next_Event(self.Tod.date)
        embed = discord.Embed(
            title=f"Next Important Date: {self.Tod.fdate}",
            description=f"```{self.Tod.thisDate}```",
            url="https://www.mun.ca/regoff/calendar/sectionNo=GENINFO-0086",
            colour=discord.Colour.red(),
        )
        await ctx.send(embed=embed)

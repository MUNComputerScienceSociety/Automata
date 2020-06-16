import discord
from discord.ext import commands

from Bot import bot
from Plugin import AutomataPlugin
from plugins.TodayAtMun.DiaryParser import DiaryParser
from plugins.TodayAtMun.Today import Today


class TodayAtMun(AutomataPlugin):
    def __init__(self, manifest, bot):
        super().__init__(manifest, bot)
        self.parse = DiaryParser()
        self.tod = Today(self.parse.diary)

    @commands.group()
    async def today(self, ctx):
        """ Provides brief info of significant dates on the Mun calendar"""
        if not ctx.invoked_subcommand:
            await ctx.send("Please Provide Subcommand e.g !today [next]")

    @today.command(name="next")
    async def today_next(self, ctx):
        """Sends quick update on Muns next calendar date on the uni diary"""
        self.tod.set_current_date()
        self.tod.find_event(self.tod.date)
        embed = discord.Embed(
            title=f"{self.tod.format_date(self.tod.date)}",
            description=f"```{self.tod.infoDay}``` ( !today later ) to get next event",
            url="https://www.mun.ca/regoff/calendar/sectionNo=GENINFO-0086",
            colour=discord.Colour.orange(),
        )
        await ctx.send(embed=embed)

    @today.command(name="reset")
    async def today_reset(self, ctx):
        """Re-Parses data from Mun Diary."""
        DiaryParser()
        await ctx.send("Data Reset!")

    @today.command(name="later")
    async def today_after(self, ctx):
        """Sends next date coming up on the univsersity diary"""
        self.tod.set_current_date()
        self.tod.find_event(self.tod.date)
        self.tod.next_day()
        self.tod.next_event(self.tod.date)
        embed = discord.Embed(
            title=f"Next Important Date: {self.tod.fdate}",
            description=f"```{self.tod.thisDate}```",
            url="https://www.mun.ca/regoff/calendar/sectionNo=GENINFO-0086",
            colour=discord.Colour.red(),
        )
        await ctx.send(embed=embed)

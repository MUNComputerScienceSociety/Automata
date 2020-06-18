import discord
from discord.ext import commands
import typing

from Bot import bot
from Plugin import AutomataPlugin
from plugins.TodayAtMun.DiaryParser import DiaryParser
from plugins.TodayAtMun.Today import Today


class TodayAtMun(AutomataPlugin):
    def __init__(self, manifest, bot: commands.Bot):
        super().__init__(manifest, bot)
        self.parse = DiaryParser()
        self.tod = Today(self.parse.diary)

    @commands.group()
    async def today(self, ctx: commands.Context):
        """ Provides brief info of significant dates on the Mun calendar"""
        if not ctx.invoked_subcommand:
            await ctx.send(
                "Please Provide Subcommand e.g !today [next] \n ( !help today ) for more."
            )

    @today.command(name="next")
    async def today_next(self, ctx: commands.Context):
        """Sends next upcoming date on the mun calendar"""
        self.tod.set_current_date()
        self.tod.find_event(self.tod.date)
        embed = discord.Embed(
            title=f"{self.tod.fdate}",
            description=f"```{self.tod.info_day}``` ( !today later ) to get next event",
            url=self.parse.DATA_SOURCE,
            colour=discord.Colour.orange(),
        )
        await ctx.send(embed=embed)

    @today.command(name="later")
    async def today_after(self, ctx: commands.Context):
        """Sends following date after the next upcoming date on the mun calendar"""
        self.tod.set_current_date()
        self.tod.find_event(self.tod.date)
        self.tod.next_day()
        self.tod.next_event(self.tod.date)
        embed = discord.Embed(
            title=f"Next Important Date: {self.tod.fdate}",
            description=f"```{self.tod.this_date}```",
            url=self.parse.DATA_SOURCE,
            colour=discord.Colour.red(),
        )
        await ctx.send(embed=embed)

    @today.command(name="date")
    async def today_date(self, ctx: commands.Context):
        """ Returns current date now """
        self.tod.set_current_date()
        await ctx.send(self.tod.date)

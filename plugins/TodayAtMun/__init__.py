import discord
from discord.ext import commands

from Bot import bot
from Plugin import AutomataPlugin
from plugins.TodayAtMun.DiaryParser import DiaryParser
from plugins.TodayAtMun.Today import Today

class TodayAtMun(AutomataPlugin):
    """Provides a utility for MUN diary lookup specifically significant dates."""

    def __init__(self, manifest, bot: commands.Bot):
        super().__init__(manifest, bot)
        self.parse = DiaryParser()
        self.today_fun = Today(self.parse.diary)

    @commands.group()
    async def today(self, ctx: commands.Context):
        """Provides brief info of significant dates on the MUN calendar."""
        if not ctx.invoked_subcommand:
            await ctx.send(
                "Please provide subcommand e.g !today [next] \n ( !help today ) for more."
            )

    @today.command(name="next")
    async def today_next(self, ctx: commands.Context):
        """Sends next upcoming date on the MUN calendar."""
        self.today_fun.set_current_date()
        self.today_fun.find_event(self.today_fun.date)
        embed = discord.Embed(
            title=self.today_fun.formatted_date,
            description=f"```{self.today_fun.info_day}``` ( !today later ) to get next event",
            url=self.parse.DATA_SOURCE,
            colour=discord.Colour.orange(),
        )
        await ctx.send(embed=embed)

    @today.command(name="later")
    async def today_after(self, ctx: commands.Context):
        """Sends the event after the 'next' event."""
        self.today_fun.set_current_date()
        self.today_fun.find_event(self.today_fun.date)
        self.today_fun.next_day()
        self.today_fun.next_event(self.today_fun.date)
        embed = discord.Embed(
            title=f"Following Important Date: {self.today_fun.formatted_date}",
            description=f"```{self.today_fun.this_date}```",
            url=self.parse.DATA_SOURCE,
            colour=discord.Colour.red(),
        )
        await ctx.send(embed=embed)

    @today.command(name="date")
    async def today_date(self, ctx: commands.Context):
        """Sends the current date at that instance."""
        self.today_fun.set_current_date()
        await ctx.send(self.today_fun.format_date(self.today_fun.date))

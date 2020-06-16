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

    @commands.group()
    async def today(self, ctx):
        if not ctx.invoked_subcommand:
            await ctx.send("Please Provide Subcommand e.g !today [soon]")

    @today.command(name="soon")
    async def today_soon(self, ctx):
        """Sends quick update on Muns Next Calendar Date on the Uni Diary"""
        self.ins_Today.set_current_date()
        self.ins_Today.findEvent(self.ins_Today.date)
        embed = discord.Embed(
            title=f"{self.ins_Today.format_date(self.ins_Today.date)}",
            description=f"```{self.ins_Today.infoDay}```",
            url="https://www.mun.ca/regoff/calendar/sectionNo=GENINFO-0086",
            colour=discord.Colour.orange(),
        )
        await ctx.send(embed=embed)

    @today.command(name="reset")
    async def today_reset(self, ctx):
        """Re-Parses data from Mun Diary."""
        diary_parser()
        await ctx.send("Data Reset!")
        return

    @today.command(name="next")
    async def varietyToday(self, ctx):
        """
        Sends (n) amounts of dates coming up on the univsersity diary
        """
        self.ins_Today.set_current_date()
        self.ins_Today.findEvent(self.ins_Today.date)
        self.ins_Today.nextDay()
        self.ins_Today.next_Event(self.ins_Today.date)
        embed = discord.Embed(
            title=f"Next Important Date: {self.ins_Today.fdate}",
            description=f"```{self.ins_Today.thisDate}```",
            url="https://www.mun.ca/regoff/calendar/sectionNo=GENINFO-0086",
            colour=discord.Colour.orange(),
        )
        await ctx.send(embed=embed)

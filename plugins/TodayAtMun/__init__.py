import discord
from discord.ext import commands

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
            description=f"`{self.today_fun.diary[self.today_fun.key]} ( !today later ) to get next event`",
            url=self.parse.DATA_SOURCE,
            colour=discord.Colour.dark_green(),
        )
        embed.set_footer(
            text="\u200b",
            icon_url="https://raw.githubusercontent.com/MUNComputerScienceSociety/csclub-homepage/master/listing_cs_logo.png",
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
            description=f"`{self.today_fun.this_date}`",
            url=self.parse.DATA_SOURCE,
            colour=discord.Colour.dark_green(),
        )
        embed.set_footer(
            text="\u200b",
            icon_url="https://raw.githubusercontent.com/MUNComputerScienceSociety/csclub-homepage/master/listing_cs_logo.png",
        )
        await ctx.send(embed=embed)

    @today.command(name="date")
    async def today_date(self, ctx: commands.Context):
        """Sends the current date at that instance."""
        self.today_fun.set_current_date()
        await ctx.send(self.today_fun.format_date(self.today_fun.date))

    @today.command(name="nextfive")
    async def today_nextfive(self, ctx: commands.Context):
        """Sends the next five events coming up in MUN diary."""
        self.today_fun.set_current_date()
        self.today_fun.package_of_events(self.today_fun.date, 5)
        self.date_context_embed = discord.Embed(
            title=f"__**Showing next five upcoming events in MUN diary from {self.today_fun.first_event} to {self.today_fun.last_event}.**__",
            url=self.parse.DATA_SOURCE,
            color=discord.Colour.dark_green(),
        )
        for date, context in self.today_fun.packaged_items.items():
            self.date_context_embed.add_field(
                name=f"**{date}:**", value=f"`{context}.`", inline=False
            )
        self.date_context_embed.set_footer(
            text="\u200b",
            icon_url="https://raw.githubusercontent.com/MUNComputerScienceSociety/csclub-homepage/master/listing_cs_logo.png",
        )
        await ctx.send(embed=self.date_context_embed)

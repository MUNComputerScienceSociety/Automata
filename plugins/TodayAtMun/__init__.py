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

    @staticmethod
    def today_embed_template():
        """Provides initial embed attributes."""
        embed = discord.Embed()
        embed.colour = discord.Colour.dark_green()
        embed.set_footer(
            text="\u200b",
            icon_url="https://raw.githubusercontent.com/MUNComputerScienceSociety/csclub-homepage/master/listing_cs_logo.png",
        )
        return embed

    def today_is_next(self, date: str) -> str:
        """Provides an emoji indicator if the next event occurs on current day."""
        today_date = self.today_fun.format_date(self.today_fun.curr_date)
        if today_date == date:
            return ":red_circle:"
        return ""

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
        next_event_date = self.today_fun.format_date(self.today_fun.date)
        embed = self.today_embed_template()
        embed.add_field(
            name=f"{self.today_is_next(next_event_date)} {next_event_date}",
            value=f"`{self.today_fun.diary[self.today_fun.key]}.`\n( !today later ) to get next event.",
        )
        await ctx.send(embed=embed)

    @today.command(name="later")
    async def today_after(self, ctx: commands.Context):
        """Sends the event after the 'next' event."""
        self.today_fun.set_current_date()
        self.today_fun.find_event(self.today_fun.date)
        self.today_fun.next_day()
        self.today_fun.next_event(self.today_fun.date)
        embed = self.today_embed_template()
        embed.add_field(
            name=f"Following Important Date: {self.today_fun.formatted_date}",
            value=f"`{self.today_fun.this_date}`",
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
        embed = self.today_embed_template()
        embed.add_field(
            name=f"__**Showing next five upcoming events in MUN diary from {self.today_fun.first_event} to {self.today_fun.last_event}.**__",
            value="\u200b",
        )
        for date, context in self.today_fun.packaged_items.items():
            embed.add_field(
                name=f"{self.today_is_next(date)} **{date}**: ",
                value=f"`{context}.`",
                inline=False,
            )
        await ctx.send(embed=embed)

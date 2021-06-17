import asyncio
from random import choice

import discord
from discord.ext import commands, tasks
from Globals import DIARY_DAILY_CHANNEL, PRIMARY_GUILD, mongo_client
from Plugin import AutomataPlugin
from plugins.TodayAtMun.Diary import Diary
from plugins.TodayAtMun.DiaryParser import DiaryParser

MUN_LOGO = "https://www.cs.mun.ca/~csclub/assets/logos/others/mun-color.png"


class TodayAtMun(AutomataPlugin):
    """Provides a utility for MUN diary lookup specifically significant dates."""

    def __init__(self, manifest, bot: commands.Bot):
        super().__init__(manifest, bot)
        self.parse = DiaryParser()
        self.diary_util = Diary(self.parse.diary)

        self.posted_events = mongo_client.automata.mun_diary

        loop = asyncio.get_event_loop()
        self.check_for_new_event.start()

    @staticmethod
    def today_embed_template():
        """Provides initial embed attributes."""
        embed = discord.Embed()
        mun_colours = [0x822433, 0xFFFFFF, 0x838486]
        embed.colour = discord.Colour(choice(mun_colours))
        embed.set_footer(
            text="TodayAtMun", icon_url=MUN_LOGO,
        )
        return embed

    def time_delta_emojify(self) -> str:
        remaining_time = self.diary_util.time_delta_event(self.diary_util.date)
        emoji_delta = ""
        if remaining_time > 1:
            emoji_delta = f"⏳ {remaining_time} day(s)"
        elif 0 < remaining_time <= 1:
            emoji_delta = f"⌛ {remaining_time} day(s)"
        else:
            emoji_delta = "🔴"
        return emoji_delta

    def today_embed_next_template(self, next_event_date):
        embed = self.today_embed_template()
        embed.set_author(
            name=f"⏳ ~{self.diary_util.time_delta_event(self.diary_util.date)} days"
        )
        embed.add_field(
            name=f"{self.diary_util.today_is_next(next_event_date)} {next_event_date}",
            value=f"{self.diary_util.diary[self.diary_util.key]}.\n\n*( !diary later ) to see next following event.*",
            inline=False,
        )
        return embed

    @commands.group(aliases=["d"])
    async def diary(self, ctx: commands.Context):
        """Provides brief info of significant dates on the MUN calendar."""
        if not ctx.invoked_subcommand:
            await ctx.send(
                "Please provide subcommand e.g !diary [next] \n ( !help today ) for more."
            )

    @diary.command(name="next", aliases=["n"])
    async def today_next(self, ctx: commands.Context):
        """Sends next upcoming date on the MUN calendar."""
        self.diary_util.set_current_date()
        self.diary_util.find_event(self.diary_util.date)
        next_event_date = self.diary_util.format_date(self.diary_util.date)
        embed = self.today_embed_next_template(next_event_date)
        await ctx.send(embed=embed)

    @diary.command(name="later", aliases=["l"])
    async def today_after(self, ctx: commands.Context):
        """Sends the event after the 'next' event."""
        self.diary_util.set_current_date()
        self.diary_util.find_event(self.diary_util.date)
        self.diary_util.next_day()
        self.diary_util.next_event(self.diary_util.date)
        embed = self.today_embed_template()
        embed.add_field(
            name=f"Following Important Date: {self.diary_util.formatted_date}, ⌛ ~`{self.diary_util.time_delta_event(self.diary_util.date)}` days away.",
            value=f"{self.diary_util.this_date}",
            inline=False,
        )
        await ctx.send(embed=embed)

    @diary.command(name="date")
    async def today_date(self, ctx: commands.Context):
        """Sends the current date at that instance."""
        self.diary_util.set_current_date()
        await ctx.send(self.diary_util.format_date(self.diary_util.date))

    @diary.command(name="nextfive")
    async def today_nextfive(self, ctx: commands.Context):
        """Sends the next five events coming up in MUN diary."""
        self.diary_util.set_current_date()
        packaged_events = self.diary_util.package_of_events(
            self.diary_util.date, 5)
        embed = self.today_embed_template()
        embed.add_field(
            name=f"__**Showing next five upcoming events in MUN diary**__\n*{self.diary_util.first_event}* **-** *{self.diary_util.last_event}*",
            value="\u200b",
            inline=False,
        )
        for event, (date, context) in enumerate(packaged_events.items()):
            embed.add_field(
                name=f"{self.diary_util.today_is_next(date)} **{date}**:",
                value=f"{context}",
                inline=False,
            )
        await ctx.send(embed=embed)

    async def post_next_event(self, event):
        self.diary_util.set_current_date()
        self.diary_util.find_event(self.diary_util.date)
        next_event_date = self.diary_util.format_date(self.diary_util.date)
        next_embed = self.today_embed_next_template(next_event_date)
        await self.bot.get_guild(PRIMARY_GUILD).get_channel(DIARY_DAILY_CHANNEL).send(
            embed=next_embed
        )
        await self.posted_events.insert_one({"date": next_event_date})

    async def post_new_events(self):
        self.diary_util.set_current_date()
        self.diary_util.find_event(self.diary_util.date)
        next_event_date = self.diary_util.format_date(self.diary_util.date)
        retrieve_event = await self.posted_events.find_one({"date": next_event_date})

        if retrieve_event is None:
            await self.post_next_event(next_event_date)
            await asyncio.sleep(5)
        else:
            await self.update_event_msg()
            await asyncio.sleep(5)

    @tasks.loop(seconds=10)
    async def check_for_new_event(self):
        await self.post_new_events()

    @check_for_new_event.before_loop
    async def before_check_test(self):
        await self.bot.wait_until_ready()

    async def update_event_msg(self):
        channel = self.bot.get_guild(
            PRIMARY_GUILD).get_channel(DIARY_DAILY_CHANNEL)
        message = await channel.fetch_message(channel.last_message_id)
        message.embeds[0].set_author(
            name=self.time_delta_emojify()
        )
        await message.edit(embed=message.embeds[0])

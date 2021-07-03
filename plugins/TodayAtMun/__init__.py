import asyncio
from datetime import date, datetime, timedelta
from random import choice

import discord
from discord.ext import commands, tasks
from Globals import DIARY_DAILY_CHANNEL, PRIMARY_GUILD, mongo_client
from Plugin import AutomataPlugin
from plugins.TodayAtMun.DiaryUtil import DiaryUtil
from plugins.TodayAtMun.DiaryParser import DiaryParser

MUN_LOGO = "https://www.cs.mun.ca/~csclub/assets/logos/color-square-trans.png"
MUN_COLOUR_RED = 0x822433
MUN_COLOUR_WHITE = 0xFFFFFF
MUN_COLOUR_GREY = 0x838486


class TodayAtMun(AutomataPlugin):
    """Provides a utility for MUN diary lookup specifically significant dates."""

    def __init__(self, manifest, bot: commands.Bot):
        super().__init__(manifest, bot)
        self.parse = DiaryParser()
        self.diary_util = DiaryUtil(self.parse.diary)
        self.posted_events = mongo_client.automata.mun_diary
        self.check_for_new_event.start()

    @staticmethod
    def today_embed_template():
        """Provides initial embed attributes."""
        embed = discord.Embed()
        mun_colours = [MUN_COLOUR_RED, MUN_COLOUR_WHITE, MUN_COLOUR_GREY]
        embed.colour = discord.Colour(choice(mun_colours))
        embed.set_footer(
            text="TodayAtMun\t!help diary",
            icon_url=MUN_LOGO,
        )
        return embed

    def time_delta_emojify(self) -> str:
        remaining_time = DiaryUtil.time_delta_event(
            DiaryUtil.str_to_datetime(self.diary_util.key)
        )
        if remaining_time > 1:
            return f"⏳ {remaining_time} day(s)"
        elif 0 < remaining_time <= 1:
            return f"⌛ {remaining_time} day"
        else:
            return "🔴"

    def today_embed_next_template(self, next_event_date: datetime) -> discord.Embed:
        embed = self.today_embed_template()
        embed.set_author(
            name=f"⏳ ~{self.diary_util.time_delta_event(self.diary_util.str_to_datetime(next_event_date))} days"
        )
        embed.add_field(
            name=f"{self.diary_util.today_is_next(next_event_date)} {next_event_date}",
            value=f"{self.diary_util.diary[self.diary_util.key]}.",
            inline=False,
        )
        return embed

    @commands.group(aliases=["d", "today"])
    async def diary(self, ctx: commands.Context):
        """Provides brief info of significant dates on the MUN calendar."""
        await ctx.trigger_typing()
        if ctx.invoked_subcommand is None:
            await ctx.reply(content="Invalid command, check !help diary for more.")

    @diary.command(name="next", aliases=["n"])
    async def today_next(self, ctx: commands.Context):
        """Sends next upcoming date on the MUN calendar."""
        self.diary_util.set_current_date()
        self.diary_util.find_event(self.diary_util.date)
        embed = self.today_embed_next_template(self.diary_util.key)
        await ctx.reply(embed=embed)

    @diary.command(name="later", aliases=["l"])
    async def today_after(self, ctx: commands.Context):
        """Sends the event after the 'next' event."""
        self.diary_util.find_following_event()
        embed = self.today_embed_template()
        embed.add_field(
            name=f"{self.diary_util.key}, ⌛ ~`{DiaryUtil.time_to_dt_delta(self.diary_util.key)}` days away.",
            value=f"{self.diary_util.this_date}",
            inline=False,
        )
        await ctx.reply(embed=embed)

    @diary.command(name="date")
    async def today_date(self, ctx: commands.Context):
        """Sends the current date at that instance."""
        self.diary_util.set_current_date()
        await ctx.reply(self.diary_util.format_date(self.diary_util.date))

    @diary.command(name="bundle", aliases=["b", "nextfive"])
    async def today_bundle(self, ctx: commands.Context, events:int = 5):
        """Sends the next n number of events coming up in MUN diary."""
        self.diary_util.set_current_date()
        packaged_events = self.diary_util.package_of_events(
            self.diary_util.date, events
        )
        packaged_keys = list(packaged_events.keys())
        embed = self.today_embed_template()
        embed.add_field(
            name=f"__**Showing next five upcoming events in MUN diary**__\n*{packaged_keys[0]}* **-** *{packaged_keys[len(packaged_keys)-1]}*",
            value="\u200b",
            inline=False,
        )
        for _, (date, context) in enumerate(packaged_events.items()):
            embed.add_field(
                name=f"{self.diary_util.today_is_next(date)} **{date}**:",
                value=f"{context}",
                inline=False,
            )
        await ctx.send(embed=embed)
    
    @today_bundle.error
    async def today_next_bundle_handler(self, ctx, error):
        error = getattr(error, 'original', error)
        if isinstance(error, commands.BadArgument):
            await ctx.reply("Invalid use of bundle, must use a number instead. Of ")

    async def post_next_event(self, event: str):
        self.diary_util.set_current_date()
        self.diary_util.find_event(self.diary_util.date)
        next_embed = self.today_embed_next_template(self.diary_util.key)
        await self.bot.get_guild(PRIMARY_GUILD).get_channel(DIARY_DAILY_CHANNEL).send(
            embed=next_embed
        )
        await self.posted_events.insert_one({"date": event})

    async def post_new_events(self):
        self.diary_util.set_current_date()
        self.diary_util.find_event(self.diary_util.date)
        next_event_date = self.diary_util.key
        retrieve_event = await self.posted_events.find_one({"date": next_event_date})

        if retrieve_event is None:
            await self.post_next_event(next_event_date)
        else:
            await self.update_event_msg()
        await asyncio.sleep(5)

    @tasks.loop(hours=6)
    async def check_for_new_event(self):
        await self.post_new_events()

    @check_for_new_event.before_loop
    async def before_check_test(self):
        await self.bot.wait_until_ready()

    @diary.command("reset")
    @commands.has_permissions(view_audit_log=True)
    async def reset_recurrent_events(self, ctx):
        """Executive Use Only: Resets automated event postings"""
        await mongo_client.automata.drop_collection("mun_diary")
        await mongo_client.automata.mun_diary.insert_one({"data": "foo"})
        self.check_for_new_event.restart()

    async def update_event_msg(self):
        channel = self.bot.get_guild(PRIMARY_GUILD).get_channel(DIARY_DAILY_CHANNEL)
        message = await channel.fetch_message(channel.last_message_id)
        message.embeds[0].set_author(name=self.time_delta_emojify())
        edit_time = DiaryUtil.get_current_date().strftime("%Y%m%d%H%M%S")
        message.embeds[0].set_footer(
            text=f"Last update: {edit_time}", icon_url=MUN_LOGO
        )
        await message.edit(embed=message.embeds[0])

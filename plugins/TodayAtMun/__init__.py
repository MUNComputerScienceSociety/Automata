import asyncio
from random import choice
from typing import Optional

import httpx
import mechanicalsoup
from bs4 import BeautifulSoup
from discord import ApplicationCheckFailure
from Globals import DIARY_DAILY_CHANNEL, GENERAL_CHANNEL, PRIMARY_GUILD, mongo_client
from nextcord import (
    ApplicationError,
    Colour,
    Embed,
    Interaction,
    SlashOption,
    slash_command,
    Message
)
from nextcord.ext import application_checks, commands, tasks
from Plugin import AutomataPlugin
from plugins.TodayAtMun.DiaryUtil import DiaryUtil

MUN_CSS_LOGO = "https://www.cs.mun.ca/~csclub/assets/logos/color-square-trans.png"
MUN_COLOUR_RED = 0x822433
MUN_COLOUR_WHITE = 0xFFFFFF
MUN_COLOUR_GREY = 0x838486
DIARY_DATA_SOURCE = "https://www.mun.ca/regoff/calendar/sectionNo=GENINFO-0086"
EXAMS_DATA_SOURCE = "https://selfservice.mun.ca/direct/swkgexm.P_Query_Exam?p_term_code=202102&p_internal_campus_code=CAMP_STJ&p_title=STJ_WINT"


class TodayAtMun(AutomataPlugin):
    """Provides a utility for MUN diary lookup specifically significant dates."""

    def __init__(self, manifest, bot: commands.Bot):
        super().__init__(manifest, bot)
        self.parse = TodayAtMun.parse_diary()
        self.diary_util = DiaryUtil(self.parse)
        self.posted_events = mongo_client.automata.mun_diary
        self.check_for_new_event.start()
        self.days_till_next_event = -1

    @staticmethod
    def diary_embed_template():
        """Provides initial embed attributes."""
        embed = Embed()
        mun_colours = [MUN_COLOUR_RED, MUN_COLOUR_WHITE, MUN_COLOUR_GREY]
        embed.colour = Colour(choice(mun_colours))
        embed.set_footer(
            text="TodayAtMun ● !help TodayAtMun",
            icon_url=MUN_CSS_LOGO,
        )
        return embed

    def diary_embed_next_template(self, next_event_date: str) -> Embed:
        embed = self.diary_embed_template()
        embed.set_author(
            name=f"⏳ ~{self.diary_util.delta_event_time(self.diary_util.str_to_datetime(next_event_date))} day(s)"
        )
        embed.add_field(
            name=f"{self.diary_util.today_is_next(next_event_date)} {next_event_date}",
            value=f"{self.diary_util.diary[self.diary_util.key]}.",
            inline=False,
        )
        return embed

    @slash_command(guild_ids=[PRIMARY_GUILD])
    async def diary(self, interaction: Interaction):
        """Provides brief info of significant dates on the MUN calendar."""
        pass

    @diary.subcommand(name="next")
    async def diary_next(self, interaction: Interaction):
        """Sends next upcoming date on the MUN calendar."""
        self.diary_util.set_current_date()
        self.diary_util.find_event(self.diary_util.date)
        embed = self.diary_embed_next_template(self.diary_util.key)
        await interaction.response.send_message(embed=embed)

    @diary.subcommand(name="after")
    async def diary_after(self, interaction: Interaction):
        """Sends the event after the 'next' event."""
        self.diary_util.find_following_event()
        embed = self.diary_embed_template()
        embed.add_field(
            name=f"{self.diary_util.key}, ⌛ ~`{DiaryUtil.time_to_dt_delta(self.diary_util.key)}` days away.",
            value=f"{self.diary_util.event_desc}",
            inline=False,
        )
        await interaction.response.send_message(embed=embed)

    @diary.subcommand(name="date")
    async def diary_date(self, interaction: Interaction):
        """Sends the current date at that instance."""
        self.diary_util.set_current_date()
        await interaction.response.send_message(
            self.diary_util.format_date(self.diary_util.date)
        )

    @diary.subcommand(name="bundle")
    async def diary_bundle(
        self,
        interaction: Interaction,
        events: Optional[int] = SlashOption(
            name="picker",
            choices={"one": 1, "two": 2, "three": 3, "four": 4, "five": 5},
            required=False,
            description="How many diary events to bundle.",
        ),
    ):
        """Sends the next n number of events coming up in MUN diary."""
        self.diary_util.set_current_date()
        packaged_events = self.diary_util.package_of_events(
            self.diary_util.date, events
        )
        packaged_keys = list(packaged_events.keys())
        first_event_date = packaged_keys[0]
        last_event_data = packaged_keys[-1]
        bundle_size = len(packaged_events)
        embed = self.diary_embed_template()
        embed.add_field(
            name=f"__**Showing next {bundle_size} upcoming events in MUN diary**__",
            value=f"*{first_event_date}* **-** *{last_event_data}*",
            inline=False,
        )
        for _, (date, context) in enumerate(packaged_events.items()):
            embed.add_field(
                name=f"{self.diary_util.today_is_next(date)} **{date}**:",
                value=f"{context}",
                inline=False,
            )
        await interaction.response.send_message(embed=embed)

    async def post_next_event(self, channel: int) -> Message:
        date = DiaryUtil.get_current_time()
        self.diary_util.find_event(date)
        next_embed = self.diary_embed_next_template(self.diary_util.key)
        return (
            await self.bot.get_guild(PRIMARY_GUILD)
            .get_channel(channel)
            .send(embed=next_embed)
        )

    async def notify_new_event(self, message_link: Message):
        embed = self.diary_embed_template()
        embed.add_field(
            name="**📅 New MUN Calendar Event**",
            value=f"[**Click to view**]({message_link})",
            inline=False,
        )
        await self.bot.get_guild(PRIMARY_GUILD).get_channel(GENERAL_CHANNEL).send(
            embed=embed
        )

    async def post_new_events(self):
        date = DiaryUtil.get_current_time()
        next_event_date = self.diary_util.find_event(date)
        retrieve_event = await self.posted_events.find_one({"date": next_event_date})

        if retrieve_event is None:
            posted_message_id = await self.post_next_event(DIARY_DAILY_CHANNEL)
            await self.posted_events.insert_one({"date": next_event_date})
            await self.notify_new_event(posted_message_id.jump_url)
        else:
            await self.update_event_msg(next_event_date)
        await asyncio.sleep(5.0)

    @tasks.loop(hours=1.0)
    async def check_for_new_event(self):
        await self.post_new_events()

    @check_for_new_event.before_loop
    async def before_check_test(self):
        await self.bot.wait_until_ready()

    @diary.subcommand(name="restart")
    @application_checks.has_permissions(view_audit_log=True)
    async def reset_recurrent_events(self, interaction: Interaction):
        """Executive Use Only: Resets automated event posting."""
        await mongo_client.automata.drop_collection("mun_diary")
        await mongo_client.automata.mun_diary.insert_one({"date": "init"})
        self.check_for_new_event.restart()
        await interaction.response.send_message(
            "Restarted Mun Calendar event loop, cleared records from DB."
        )

    @diary.subcommand(name="refresh")
    @application_checks.has_permissions(view_audit_log=True)
    async def refresh_diary(self, interaction: Interaction):
        """Executive Use Only: Refreshes the MUN calendar data."""
        self.parse = TodayAtMun.parse_diary()
        self.diary_util = DiaryUtil(self.parse)
        await interaction.response.send_message("MUN calendar refreshed.")

    @refresh_diary.error
    @reset_recurrent_events.error
    async def command_invocation_error(
        self, interaction: Interaction, error: ApplicationCheckFailure
    ):
        if isinstance(error, application_checks.ApplicationMissingPermissions):
            await interaction.response.send_message(
                "Invalid permissions to invoke this command."
            )

    async def update_event_msg(self, next_event_date: str):
        diary_daily_channel = self.bot.get_guild(PRIMARY_GUILD).get_channel(
            DIARY_DAILY_CHANNEL
        )
        message = await diary_daily_channel.fetch_message(
            diary_daily_channel.last_message_id
        )
        if (
            next_date_delta := self.diary_util.time_to_dt_delta(next_event_date)
        ) != self.days_till_next_event:
            self.days_till_next_event = next_date_delta
            await self.post_next_event(GENERAL_CHANNEL)
        message.embeds[0].set_author(
            name=self.diary_util.time_delta_emojify(next_event_date)
        )
        edit_time = DiaryUtil.get_current_time("Canada/Newfoundland").strftime(
            "%-I:%M %p %Z %a %b %-d, %Y"
        )
        message.embeds[0].set_footer(
            text=f"Last update: {edit_time}", icon_url=MUN_CSS_LOGO
        )
        await message.edit(embed=message.embeds[0])

    @slash_command(guild_ids=[PRIMARY_GUILD])
    async def exam(
        self,
        interaction: Interaction,
        subj: str = SlashOption(
            description="Subject to filter by, such as 'COMP'", required=True
        ),
        course_num: str = SlashOption(
            description="Course Number to filter by, such as 1001", required=False
        ),
        sec_numb: str = SlashOption(
            description="Section Number to filter, such as 003", required=False
        ),
        crn: str = SlashOption(description="Crn Number to filter by.", required=False),
    ) -> None:
        """Provides Exam Info for current semester
        Usage: !exam <subject> <course_number> <section_number> <crn>
        Example: !exam COMP 1003
        """
        sched_heading, table_heading, exams_parsed = TodayAtMun.get_exams(
            subj, course_num, sec_numb, crn
        )
        embed = self.diary_embed_template()
        embed.title = sched_heading
        embed.add_field(name=table_heading, value="\u200b", inline=False)
        for exam in exams_parsed:
            embed.add_field(name=" | ".join(exam), value="\u200b", inline=False)
        await interaction.response.send_message(embed=embed)

    @exam.error
    async def exam_handler(self, interaction: Interaction, error: ApplicationError):
        error = getattr(error, "original", error)
        await interaction.response.send_message(error)

    @staticmethod
    def parse_diary() -> dict[str, str]:
        diary = {}
        resp = httpx.get(DIARY_DATA_SOURCE)
        mun_request = resp.text
        soup = BeautifulSoup(mun_request, "html.parser")
        dates_in_diary = soup.find_all("td", attrs={"align": "left"})
        description_of_date = soup.find_all("td", attrs={"align": "justify"})

        for left_item, right_item in zip(dates_in_diary, description_of_date):
            right_item_parse = right_item.get_text().split()
            try:
                diary[left_item.find("p").get_text().strip("\n\t")] = " ".join(
                    right_item_parse
                )
            except AttributeError:
                diary[left_item.find("li").get_text().strip("\n\t")] = " ".join(
                    right_item_parse
                )
        return diary

    @staticmethod
    def submit_form(
        subj: str = "", course_num: str = "", sec_numb: str = "", crn: str = ""
    ) -> BeautifulSoup:
        browser = mechanicalsoup.StatefulBrowser(
            soup_config={"features": "html.parser"}
        )
        browser.open(EXAMS_DATA_SOURCE)
        browser.select_form('form[method="post"]')

        browser["p_subj_code"] = subj
        browser["p_crse_numb"] = course_num
        browser["p_seq_numb"] = sec_numb
        browser["p_crn"] = crn

        browser.submit_selected()
        return browser.page

    @staticmethod
    def parse_sched_heading(page) -> str:
        return page.find("div", class_="infotextdiv").find("b").get_text().strip()

    @staticmethod
    def parse_headings(page: BeautifulSoup) -> str:
        return " | ".join(
            f"{heading.get_text()}"
            for heading in page.find_all("td", class_="dbheader")
        )

    @staticmethod
    def parse_form(page: BeautifulSoup) -> list[str]:
        exam_context = []
        exams = []
        for data_cell, course in enumerate(
            page.find_all("td", class_="dbdefault"), start=1
        ):
            exam_context.append(course.get_text())
            if data_cell % 6 == 0:
                exams.append(exam_context)
                exam_context = []
        return exams

    @staticmethod
    def get_exams(
        subj: str = "",
        course_num: str = "",
        sec_numb: str = "",
        crn: str = "",
    ) -> tuple[str, str, list[str]]:
        """Provides exam info - schedule brief, table heading and exam details."""
        page = TodayAtMun.submit_form(subj, course_num, sec_numb, crn)
        sched_heading = TodayAtMun.parse_sched_heading(page)
        headings = TodayAtMun.parse_headings(page)
        exams = TodayAtMun.parse_form(page)
        return sched_heading, headings, exams

from discord.ext import commands
import discord

from Plugin import AutomataPlugin
from plugins.Course.calendarScraper import CalendarScraper
from plugins.Course.bannerScraper import BannerScraper
from plugins.Course.peopleScraper import PeopleScraper
from plugins.Course.rmpScraper import RMPScraper

colors = [discord.Colour.blue(), discord.Colour.red(), discord.Colour.green(), 0]


class Course(AutomataPlugin):
    """Provides info on a CS course and its listings for the current semester"""

    def __init__(self, manifest, bot):
        super().__init__(manifest, bot)

    async def cog_load(self):
        self.banner_cache = self.bot.database.automata.banner_scraper_cache
        self.calendar_scraper = CalendarScraper(604800, self.banner_cache)  # 1 week cache lifetime
        await self.calendar_scraper.setup_cache(604800)
        self.people_scraper = PeopleScraper(604800, self.banner_cache)  # 1 week cache lifetime
        await self.people_scraper.setup_cache(604800)
        self.rmp_scraper = RMPScraper(604800, self.banner_cache)  # 1 week cache lifetime
        await self.rmp_scraper.ensure_collection_expiry(604800)
        self.banner_scraper = BannerScraper(604800, self.banner_cache)  # 1 week cache lifetime
        await self.banner_scraper.setup_cache(604800)

    @commands.command()
    async def course(self, ctx: commands.Context, course_ID):
        """Replies with info on a CS course when given the courses number/ID"""
        # Get the course name and info from the calendar
        (
            course_name,
            course_info,
        ) = await self.calendar_scraper.get_name_and_info_from_ID(course_ID)
        # If there is no name, tell the user that the course doesn't exist
        if not course_name:
            await ctx.send("That course doesn't exist!")
            return

        # Get the profs that are teaching the course this semester and the campuses where it's being taught
        instructor_data = await self.banner_scraper.get_profs_from_course(course_ID)
        campuses = list(instructor_data.keys())

        # Get the year/level of the course
        course_year = int(course_ID[0])

        # Set up the initial embed for the message
        embed = discord.Embed(
            title=(f"COMP {course_ID}: {course_name}"),
            color=colors[course_year - 1],
        )

        # If nobody is teaching the course this semester tell the user
        if not campuses:
            embed.description = (
                f"{course_info}\n\n**Nobody** is teaching this course this semester"
            )
            await ctx.send(embed=embed)
            return

        # If this is a course without an insturctor, send the embed with just the course description
        if not instructor_data[campuses[0]]:
            embed.description = course_info
            await ctx.send(embed=embed)
            return

        embed.description = (
            f"{course_info}\n\nProfessor(s) teaching this course this semester:\n"
        )

        # For each campus
        for i in range(len(campuses)):
            prof_strings = []
            # For each prof
            for j in range(len(instructor_data[campuses[i]])):
                prof_string = ""
                prof_name = ""
                rmp_string = ""
                # Get their info using the dumb Banner name
                prof_info = await self.people_scraper.get_prof_info_from_name(
                    instructor_data[campuses[i]][j]
                )
                # If we couldn't get any info
                if not prof_info:
                    # Try to find an RMP profile using the dumb Banner name
                    (
                        rmp_string,
                        rmp_name,
                    ) = await self.rmp_scraper.get_rating_from_prof_name(
                        instructor_data[campuses[i]][j]
                    )
                    # If there is an RMP profile
                    if rmp_string:
                        prof_name = rmp_name
                        # If there's no RMP profile either
                    else:
                        prof_name = instructor_data[campuses[i]][j]
                    prof_string = f"**{prof_name}** (Not a listed MUN Prof) "
                # If we found the profs info in the first place
                else:
                    # Get the correct name and then get try to find the RMP profile using it
                    prof_name = f"{prof_info['fname']} {prof_info['lname']}"
                    (
                        rmp_string,
                        rmp_name,
                    ) = await self.rmp_scraper.get_rating_from_prof_name(prof_name)
                    prof_string = f"{prof_info['title']} **{prof_name}** "
                # Let the user know if a profile cannot be found, otherwise add the score to the prof string
                prof_string += (
                    " - No profile on Rate My Prof\n"
                    if rmp_string == None
                    else " - Rate My Prof Score: " + rmp_string + "\n"
                )
                prof_strings.append(prof_string)
            # Add a field containing the campus name and all of the prof strings
            embed.add_field(
                name="__" + campuses[i] + "__",
                value="\n".join(prof_strings),
                inline=False,
            )

        # Send the message
        await ctx.send(embed=embed)

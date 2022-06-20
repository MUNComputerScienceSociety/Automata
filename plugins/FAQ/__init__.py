import discord
from discord.ext import commands

from Plugin import AutomataPlugin

# Colors
COLOR_SCIENCE = 0x98FB98
COLOR_ARTS = 0x9898FB
COLOR_ADMIN = 0xFFFF00

# Degree Types
SCIENCE = ("BSC", "B.SC", "SCIENCES", "SCIENCE")
ARTS = ("BA", "B.A", "ART", "ARTS")


class FAQ(AutomataPlugin):
    """Commands to answer some Frequently Asked Questions"""

    async def create_embed_science(self):
        """Returns the embed."""
        embed_science = discord.Embed(
            title="B.Sc Sample First Year",
            url="https://www.mun.ca/undergrad/first-year-information/sample-first-year---st-johns-campus/science/computer-science/",
            description="Students pursuing a bachelor of science with a major in computer science, visual computing and games or smart systems will normally take the following courses in their first year:",
            color=COLOR_SCIENCE,
        )
        embed_science.add_field(
            name=f"**Fall Semester**",
            value=f"> Mathematics 1090 or 1000\n> Computer Science 1001\n> science elective\n> English 1090\n> elective\n",
            inline=False,
        )
        embed_science.add_field(
            name=f"**Winter Semester**",
            value=f"> Mathematics 1000 or 1001\n> Computer Science 1002\n> Computer Science 1003\n> CRW Course\n> science elective\n",
            inline=False,
        )
        embed_science.add_field(
            name=f"What is a science elective?",
            value=f"_A science elective is any course from the subjects listed [here](https://www.mun.ca/science/students/majors.php)_",
            inline=False,
        )
        embed_science.add_field(
            name=f"What is an elective?",
            value=f"_An elective is any course from any subject_",
            inline=False,
        )
        embed_science.add_field(
            name=f"What is a CRW course?",
            value=f"_A CRW course is any course from the list [here](https://www.mun.ca/hss/programs/undergraduate/crw\_course\_list.php)_",
            inline=False,
        )
        embed_science.set_footer(
            text="Students who have not completed Computer Science 1003 in their first year will not be able to register for Computer Science 2001/2/3 in the fall of their second year."
        )

        return embed_science

    async def create_embed_arts(self):
        """Returns the embed."""
        embed_arts = discord.Embed(
            title="B.A Sample First Year",
            url="https://www.mun.ca/undergrad/first-year-information/sample-first-year---st-johns-campus/science/computer-science/",
            description="Students pursuing a bachelor of arts with a major in computer science will normally take the following courses in their first year::",
            color=COLOR_ARTS,
        )
        embed_arts.add_field(
            name=f"**Fall Semester**",
            value=f"> English 1090\n> Mathematics 1090 or 1000\n> Computer Science 1001\n> Language Study (LS) course\n> elective (Breathe of Knowledge encouraged)\n",
            inline=False,
        )
        embed_arts.add_field(
            name=f"**Winter Semester**",
            value=f"> CRW course\n> Mathematics 1000 or 1001\n> Computer Science 1002\n> Computer Science 1003\n> LS course\n",
            inline=False,
        )
        embed_arts.add_field(
            name=f"What is a Breadth of Knowledge and Language Study elective?",
            value=f'_"More information about [Breadth of Knowledge](https://www.mun.ca/regoff/calendar/sectionNo=ARTS-0109#ARTS-8192) and [Language Study](https://www.mun.ca/regoff/calendar/sectionNo=ARTS-0109#ARTS-8196)_',
            inline=False,
        )
        embed_arts.set_footer(
            text="Students who have not completed Computer Science 1003 in their first year will not be able to register for Computer Science 2001/2/3 in the fall of their second year."
        )

        return embed_arts

    @commands.command()
    async def sample(self, ctx: commands.Context, degree: str = "blank"):
        """Replies with a sample of the courses you need for your first year.

        Takes type of degree as argument.
        """

        if degree.upper() in SCIENCE:
            embed = await self.create_embed_science()
            await ctx.send(embed=embed)

        elif degree.upper() in ARTS:
            embed = await self.create_embed_arts()
            await ctx.send(embed=embed)

        else:
            # No type of degree was specified
            valid_args = SCIENCE + ARTS
            args_str = ", ".join(valid_args)
            await ctx.send(
                "Specify the type of degree (Valid arguments: " + args_str + ")"
            )

    @commands.command()
    async def admission(self, ctx: commands.Context):
        """Replies with some FAQ about studying CS at MUN."""
        embed_admission = discord.Embed(
            title="Frequently Asked Questions",
            url="https://www.mun.ca/computerscience/ugrad/FAQ.php",
            description="Some FAQ about studying Computer Science at MUN:",
            color=COLOR_ADMIN,
        )
        embed_admission.add_field(
            name=f"**How do I get to study CS at MUN?**",
            value=f"After admission to the university you need to complete the required courses\n> 1. COMP 1001 and COMP 1002\n> 2. 6 credit hours in a [CRW](https://www.mun.ca/regoff/calendar/sectionNo=ARTS-0109#ARTS-8194) course, including 3 credit hours in English\n> 3. MATH 1000 and 1001 (or 1090 and 1000)\n> 3. 6 credit hours in other courses",
            inline=False,
        )
        embed_admission.add_field(
            name=f"**How do I apply to the major?**",
            value=f"In February of each year an online application form will be available on the [Admissions](https://www.mun.ca/computerscience/ugrad/UGProgram/admissions.php) page. This form must be submitted prior to June 1.",
            inline=False,
        )
        embed_admission.add_field(
            name=f"**What is the minimum required average for acceptance?**",
            value=f"Students who fulfill the eligibility requirements compete for a limited number of available spaces. Selection is based on academic performance, normally cumulative average and performance in recent courses.  For 2022 applications, students must also have a mean grade of at least 65% in Computer Science 1001 and 1002. Starting Fall 2021 students need an average of 65% in COMP 1001 and COMP 1002 to get in the major",
            inline=False,
        )

        await ctx.send(embed=embed_admission)

        # ( ͡° ͜ʖ ͡°)

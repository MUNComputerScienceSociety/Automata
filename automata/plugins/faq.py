import discord
from discord.ext import commands

from automata.utils import CommandContext

# Colors
COLOR_SCIENCE = 0x98FB98
COLOR_ARTS = 0x9898FB
COLOR_ADMIN = 0xFFFF00

# Degree Types
SCIENCE = ("BSC", "B.SC", "SCIENCES", "SCIENCE")
ARTS = ("BA", "B.A", "ART", "ARTS")


class FAQ(commands.Cog):
    """Commands to answer some Frequently Asked Questions"""

    async def create_embed_science(self) -> discord.Embed:
        """Returns the embed."""
        embed_science = discord.Embed(
            title="B.Sc Sample First Year",
            url="https://www.mun.ca/undergrad/first-year-information/sample-first-year---st-johns-campus/science/computer-science/",
            description="Students pursuing a bachelor of science with a major in computer science will normally take the following courses in their first year:",
            color=COLOR_SCIENCE,
        )
        embed_science.add_field(
            name="**Fall Semester**",
            value="> Mathematics 1090 or 1000\n> Computer Science 1001\n> elective\n> English 1090\n> elective\n",
            inline=False,
        )
        embed_science.add_field(
            name="**Winter Semester**",
            value="> Mathematics 1000 or 1001\n> Computer Science 1002\n> Computer Science 1003 or elective\n> CRW Course\n> elective\n",
            inline=False,
        )
        embed_science.add_field(
            name="What is an elective?",
            value="_Electives can be in any subject, including science courses._",
            inline=False,
        )
        embed_science.add_field(
            name="What is a CRW course?",
            value="_CRW courses are Critical Reading and Writing courses_",
            inline=False,
        )
        embed_science.set_footer(
            text="Students who have not completed Computer Science 1003 in their first year will not be able to register for Computer Science 2001/2/3 in the fall of their second year."
        )

        return embed_science

    async def create_embed_arts(self) -> discord.Embed:
        """Returns the embed."""
        embed_arts = discord.Embed(
            title="B.A Sample First Year",
            url="https://www.mun.ca/undergrad/first-year-information/sample-first-year---st-johns-campus/science/computer-science/",
            description="Students pursuing a bachelor of arts with a major in computer science will normally take the following courses in their first year::",
            color=COLOR_ARTS,
        )
        embed_arts.add_field(
            name="**Fall Semester**",
            value="> English 1090\n> Mathematics 1090 or 1000\n> Computer Science 1001\n> Language Study (LS) course\n> elective (Breathe of Knowledge encouraged) or [minor program](https://www.mun.ca/regoff/calendar/sectionNo=ARTS-0109#ARTS-4701) course\n",
            inline=False,
        )
        embed_arts.add_field(
            name="**Winter Semester**",
            value="> CRW course\n> Mathematics 1000 or 1001\n> Computer Science 1002\n> Computer Science 1003 or elective\n> LS course\n",
            inline=False,
        )
        embed_arts.add_field(
            name="What is a Breadth of Knowledge and Language Study elective?",
            value='_"More information about [Breadth of Knowledge](https://www.mun.ca/regoff/calendar/sectionNo=ARTS-0109#ARTS-8192) and [Language Study](https://www.mun.ca/regoff/calendar/sectionNo=ARTS-0109#ARTS-8196)_',
            inline=False,
        )
        embed_arts.set_footer(
            text="Students who have not completed Computer Science 1003 in their first year will not be able to register for Computer Science 2001/2/3 in the fall of their second year."
        )

        return embed_arts

    @commands.command()
    async def sample(self, ctx: CommandContext, degree: str = "blank"):
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
    async def admission(self, ctx: CommandContext):
        """Replies with some FAQ about studying CS at MUN."""
        embed_admission = discord.Embed(
            title="Frequently Asked Questions",
            url="https://www.mun.ca/computerscience/ugrad/FAQ.php",
            description="Some FAQ about studying Computer Science at MUN:",
            color=COLOR_ADMIN,
        )
        embed_admission.add_field(
            name="**How do I get to study CS at MUN?**",
            value="After admission to the university you need to complete the required courses\n> 1. COMP 1001 and COMP 1002\n> 2. 6 credit hours in a [CRW](https://www.mun.ca/regoff/calendar/sectionNo=ARTS-0109#ARTS-8194) course, including 3 credit hours in English\n> 3. MATH 1000 and 1001 (or 1090 and 1000)\n> 3. 6 credit hours in other courses\nYou must also have a mean grade of at least 65% in Computer Science 1001 and 1002.",
            inline=False,
        )
        embed_admission.add_field(
            name="**How do I apply to the major?**",
            value="Students who wish to major in computer science must submit a completed [online application form](https://www.mun.ca/computerscience/undergraduates/programs/applying-for-admission/) on the [Department of Computer Science](https://www.mun.ca/computerscience/) website. The application form is available from Feb. 1 to June 1 for students applying for fall admission, and from Aug. 1 to Oct. 1 for students applying for winter admission",
            inline=False,
        )
        embed_admission.add_field(
            name="**What is the minimum required average for acceptance?**",
            value="Students who fulfill the eligibility requirements compete for a limited number of available spaces. Selection is based on academic performance, normally cumulative average and performance in recent courses.  For 2022 applications, students must also have a mean grade of at least 65% in Computer Science 1001 and 1002. Starting Fall 2021 students need an average of 65% in COMP 1001 and COMP 1002 to get in the major",
            inline=False,
        )

        await ctx.send(embed=embed_admission)

    @commands.command()
    async def DID(self, ctx: CommandContext):
        """Replies with informative information on DID."""
        await ctx.send(
            """DID and OSDD are mental health issues on the DSM5 list
Pluralkit is an accessibility bot so you know which alter you are talking to
https://did-research.org/comorbid/dd/osdd_udd/did_osdd
http://traumadissociation.com/osdd
Please read these articles before assuming someone is just roleplaying in a server"""
        )

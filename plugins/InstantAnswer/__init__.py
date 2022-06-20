import re
import httpx
from discord.ext import commands

from Plugin import AutomataPlugin


class InstantAnswer(AutomataPlugin):
    """Wrapper for Instant Answer API from DuckDuckGo"""

    @commands.command()
    async def ia(self, ctx, *, argument):
        """Replies with Instant Answer from DuckDuckGo"""

        output_template = (
            "**{subject}**: *Brought to you by **DuckDuckGo** Instant Answer API*\n\n"
            "```{abstractText}```\n"
            "**Source:** <{abstractUrl}> @ {abstractSource}"
        )

        subject = re.sub("[^ 0-9a-zA-Z]+", "", argument)
        url_template = "https://api.duckduckgo.com/?q={query}&format=json"
        url = url_template.format(query=subject.replace(" ", "+"))
        data = httpx.get(url).json()

        output = (
            "Sorry, no Instant Answer found."
            if data["AbstractURL"] == ""
            else output_template.format(
                subject=subject,
                abstractText=data["AbstractText"],
                abstractUrl=data["AbstractURL"],
                abstractSource=data["AbstractSource"],
            ).replace("``````", "")
        )

        await ctx.send(output)

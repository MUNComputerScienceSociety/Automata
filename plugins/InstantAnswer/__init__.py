import re
import httpx
from nextcord.ext import commands

from Plugin import AutomataPlugin


class InstantAnswer(AutomataPlugin):
    """Wrapper for Instant Answer API from DuckDuckGo"""

    @commands.command()
    async def ia(self, ctx, *, argument):
        """Replies with Instant Answer API from DuckDuckGo"""


        output_template = "**{subject}**: *Brought to you by **DuckDuckGo** Instant Answer API*\n\n" \
                          "{abstractText}\n" \
                          "**URL:** {abstractUrl}\n" \
                          "**Source:** {abstractSource}"

        url_template = "https://api.duckduckgo.com/?q={query}&format=json"
        url = url_template.format(query=re.sub('[^ 0-9a-zA-Z]+', '', argument).replace(" ", "+"))
        data = httpx.get(url).json()

        output = "Sorry, no Instant Answer found." \
            if data["AbstractURL"] == "" \
            else output_template.format(
                subject=argument,
                abstractText=data["AbstractText"],
                abstractUrl=data["AbstractURL"],
                abstractSource=data["AbstractSource"])

        await ctx.send(output)

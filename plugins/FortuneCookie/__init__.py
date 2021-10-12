from nextcord.ext import commands
import nextcord
import requests
from Plugin import AutomataPlugin

class FortuneCookie(AutomataPlugin):
    """A fortune cookie"""

    @commands.command()
    async def fortune(self, ctx: commands.Context):
        """Replies with a fortune cookie message"""

        response = requests.get("http://yerkee.com/api/fortune/computers").json()["fortune"]
        if len(response) > 6000:
            response = "I am too long"
        embed = nextcord.Embed(colour=nextcord.Colour.blue())
        embed.add_field(name="Your Fortune Cookie 🥠", value=response)
        message = await ctx.send(embed=embed)
        await message.add_reaction("🥠")
        
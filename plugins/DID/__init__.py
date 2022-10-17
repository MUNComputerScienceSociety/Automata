from nextcord.ext import commands

from Plugin import AutomataPlugin


class DID(AutomataPlugin):
    """Informative command regarding DID"""

    @commands.command()
    async def DID(self, ctx: commands.Context, number_of_times: int = 0):
        """Replies with a link"""

        if number_of_times == 0:
            await ctx.send(
                """DID and OSDD are mental health issues on the DSM5 list
Pluralkit is an accessibility bot so you know which alter you are talking to
https://did-research.org/comorbid/dd/osdd_udd/did_osdd
http://traumadissociation.com/osdd
Please read these articles before assuming someone is just roleplaying in a server"""
            )
        else:
            await ctx.send(f"HOLD UP! x{number_of_times}")

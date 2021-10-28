from nextcord.ext import commands

from Plugin import AutomataPlugin


class DID(AutomataPlugin):
    """IDK what goes here -Kanen"""

    @commands.command()
    async def DID(self, ctx: commands.Context, number_of_times: int = 0):
        """Replies with a link"""

        if number_of_times == 0:
            await ctx.send('DID and OSDD are mental health issues on the DSM5 list')
            await ctx.send('Pluralkit is an accessibility bot so you know which alter you are talking to')
            await ctx.send('https://did-research.org/comorbid/dd/osdd_udd/did_osdd')
            await ctx.send('http://traumadissociation.com/osdd')
            await ctx.send('Please read these articles before assuming someone is just roleplaying in a server')
        else:
            await ctx.send(f"HOLD UP! x{number_of_times}")
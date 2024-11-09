from discord import Colour, Embed
from discord.ext import commands

from Globals import AOC_LEADERBOARD_CHANNEL, PRIMARY_GUILD
from Plugin import AutomataPlugin

AOC_COLOUR = 0x01B204


class AOC(AutomataPlugin):
    """AOC 2021 Countdown"""

    @staticmethod
    def aoc_embed():
        aoc_embed = Embed()
        aoc_embed.colour = Colour(0x01B204)

        return aoc_embed

    @commands.command()
    @commands.has_role("Technology Officer")
    async def aoccountdown(self, ctx: commands.Context):
        countdown_embed = self.aoc_embed()
        countdown_embed.title = "Advent Of Count 2021 starts in <t:1638329400:R>"
        await (
            self.bot.get_guild(PRIMARY_GUILD)
            .get_channel(AOC_LEADERBOARD_CHANNEL)
            .send(embed=countdown_embed)
        )

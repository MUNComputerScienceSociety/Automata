import discord
import httpx
from discord.ext import commands

from automata.utils import CommandContext

API_BASE = "http://numbersapi.com/"


class NumberFacts(commands.Cog):
    """Numbers have a secret facts, check them out!"""

    @staticmethod
    async def fetch(api_path: str) -> httpx.Response:
        async with httpx.AsyncClient() as client:
            return await client.get(f"{API_BASE}{api_path}")

    async def message_embed(self, fact: str, number: str) -> discord.Embed:
        embed = discord.Embed(colour=discord.Colour.random())
        embed.add_field(name=f"A fact about number {number}", value=fact)
        embed.set_author(name="NFact")

        return embed

    @commands.command(aliases=["nfact"])
    async def numberfact(self, ctx: CommandContext, number: str = "random"):
        """Replies with a random fact of random or specified number
        EX.
        !nfact | a random number
        !nfact 42 | a fact about number 42
        """

        res = await self.fetch(number)
        fact = res.text

        nbr = fact.split(" ")[0]

        embed = await self.message_embed(fact, nbr)

        await ctx.send(embed=embed)

    @commands.command()
    async def yearfact(self, ctx: CommandContext, year: str = "random"):
        """
        Replies with a fact about a random or specific year
        """

        res = await self.fetch(f"{year}/year")
        fact = res.text

        nbr = fact.split(" ")[0]

        embed = await self.message_embed(fact, nbr)

        await ctx.send(embed=embed)

    @commands.command()
    async def datefact(self, ctx: CommandContext, date: str = "", month: str = ""):
        """
        Replies with a fact about a random or specific date
        !datefact DD MM
        """

        res = await self.fetch(f"{month}/{date}/date")

        if not date or not month:
            res = await self.fetch("random/date")

        fact = res.text

        nbr = " ".join(fact.split(" ")[0:2])
        embed = await self.message_embed(fact, nbr)

        await ctx.send(embed=embed)

    @commands.command()
    async def mathfact(self, ctx: CommandContext, number: str = "random"):
        """
        Numbers Trivia
        """

        res = await self.fetch(f"{number}/math")
        fact = res.text

        nbr = fact.split(" ")[0]

        embed = await self.message_embed(fact, nbr)

        await ctx.send(embed=embed)

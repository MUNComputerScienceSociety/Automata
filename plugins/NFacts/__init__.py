from os import name
from nextcord.ext import commands

import httpx
import nextcord
from Plugin import AutomataPlugin

API_BASE = "http://numbersapi.com/"
class NFacts(AutomataPlugin):
    """Numbers have a secret facts, check them out!"""

    

    @staticmethod
    async def fetch(api_path):
        async with httpx.AsyncClient() as client:
            return await client.get(f"{API_BASE}{api_path}")

class NumberFacts(AutomataPlugin):
    """Numbers have a secret facts, check them out!"""

    @commands.command(aliases=["nfact"])
    async def numberfact(self, ctx: commands.Context, number: str = "random"):
        """Replies with a random fact of random or specified number
        EX.
        !nfact | a random number
        !nfact 42 | a fact about number 42
        """

        res = await self.fetch(number)
        fact = res.text
        

        embed = nextcord.Embed(
            colour= nextcord.Colour.random()
        )

        nbr = fact.split(" ")[0]

        embed.add_field(name=f"A fact about number {nbr}", value=fact)
        embed.set_author(name="NumberFact", url= ctx.message.guild.icon.url)

        await ctx.send(
            embed = embed
        )

    @commands.command()
    async def yearfact(self, ctx: commands.Context, year: str = "random"):
        """
        Replies with a fact about a random or specific year
        """

        res = await self.fetch(f"{year}/year").text
        fact = res.text

        embed = nextcord.Embed(
            colour= nextcord.Colour.random()
        )

        nbr = fact.split(" ")[0]

        embed.add_field(name=f"A fact about the year {nbr}", value=fact)
        embed.set_author(name="NFact", url= ctx.message.guild.icon.url)

        await ctx.send(
            embed = embed
        )


    @commands.command()
    async def datefact(self, ctx: commands.Context, date: str = "", month: str = ""):
        """
        Replies with a fact about a random or specific date
        !datefact DD MM
        """

        res = await self.fetch(f"{month}/{date}/date")

        if (not date or not month):
            res = await self.fetch("random/date")

        fact = res.text
        

        embed = nextcord.Embed(
            colour= nextcord.Colour.random()
        )

        nbr = " ".join(fact.split(" ")[0: 2])
        embed.add_field(name=f"A fact about the date {nbr}", value=fact)
        embed.set_author(name="NFact", url= ctx.message.guild.icon.url)

        await ctx.send(
            embed = embed
        )

    @commands.command()
    async def mathfact(self, ctx: commands.Context, number: str = "random"):
        """
        Numbers Trivia
        """

        res = await self.fetch(f"{number}/math").text
        fact = res.text
        embed = nextcord.Embed(
            colour= nextcord.Colour.random()
        )

        nbr = fact.split(" ")[0]

        embed.add_field(name=f"A math fact about the number {nbr}", value=fact)
        embed.set_author(name="NFact", url= ctx.message.guild.icon.url)

        await ctx.send(
            embed = embed
        )





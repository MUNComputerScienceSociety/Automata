from os import name
from nextcord.ext import commands

import httpx
import nextcord
from Plugin import AutomataPlugin


class NFacts(AutomataPlugin):
    """Numbers have a secert facts, check them out!"""



    @commands.command()
    async def nfact(self, ctx: commands.Context, number: str = "random"):
        """Replies with a random fact of random or specified number
        EX.
        !nfact | a random number
        !nfact 42 | a fact about number 42
        """

        fact = httpx.get(f"http://numbersapi.com/{number}").text

        embed = nextcord.Embed(
            colour= nextcord.Colour.random()
        )

        nbr = fact.split(" ")[0]

        embed.add_field(name=f"A fact about number {nbr}", value=fact)
        embed.set_author(name="NFact", url= ctx.message.guild.icon.url)

        await ctx.send(
            embed = embed
        )

    @commands.command()
    async def yearfact(self, ctx: commands.Context, year: str = "random"):
        """
        Replies with a fact about a random or specific year
        """

        fact = httpx.get(f"http://numbersapi.com/{year}/year").text

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

        fact = httpx.get(f"http://numbersapi.com/{month}/{date}/date").text

        if (not date or not month):
            fact = httpx.get(f"http://numbersapi.com/random/date").text
        

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

        fact = httpx.get(f"http://numbersapi.com/{number}/math").text
        embed = nextcord.Embed(
            colour= nextcord.Colour.random()
        )

        nbr = fact.split(" ")[0]

        embed.add_field(name=f"A math fact about the number {nbr}", value=fact)
        embed.set_author(name="NFact", url= ctx.message.guild.icon.url)

        await ctx.send(
            embed = embed
        )





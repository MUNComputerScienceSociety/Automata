from discord.ext import commands
import discord

MAX = 9

from Plugin import AutomataPlugin

reactions = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"]


class Poll(AutomataPlugin):
    """A polling system"""

    @commands.command()
    async def poll(self, ctx: commands.Context, *, arg: str):
        """Sends a poll as an embed"""

        options = []
        lis = [
            discord.utils.escape_mentions(x.strip())
            for x in arg.split(",")
            if len(x.strip()) > 0
        ]
        question = lis[0]
        options = lis[1:]
        if len(question) > 256:
            await ctx.send("Poll question is too long")
        elif len(options) > MAX:
            await ctx.send(
                f"Max limit exceeded, please enter less than {MAX + 1} options"
            )
        else:
            embed = discord.Embed(colour=discord.Colour.blue())
            output = ""
            for num, option in enumerate(options):
                output += f"{num+1}) {option}\n"
            if len(output) > 1024:
                await ctx.send("Option length is too long")
            else:
                embed.add_field(name=question, value=output)
                message = await ctx.send(embed=embed)
                for reaction, option in zip(reactions, options):
                    await message.add_reaction(reaction)

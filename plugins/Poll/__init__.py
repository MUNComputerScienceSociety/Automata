from nextcord.ext import commands
import nextcord
MAX = 9

from Plugin import AutomataPlugin
reactions = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"]

class Poll(AutomataPlugin):
    """A polling system"""

    @commands.command()
    async def poll(self, ctx: commands.Context, *, arg: str):
        """Sends a poll as an embed"""

        options = []
        lis = [nextcord.utils.escape_mentions(x.strip()) for x in arg.split(",") if len(x.strip()) > 0]
        if len(lis) > MAX:
            await ctx.send(f"Max limit exceeded, please enter less than {MAX + 1} options")
        else:
            for item in lis:
                if item.islower():
                    options.append(item.capitalize())
                else:
                    options.append(item) 
            embed = nextcord.Embed(colour=nextcord.Colour.blue())
            output = ""
            for i in range(len(options)):
                output += f"{i+1}) {options[i]}\n"
            embed.add_field(name="Options", value=output)
            message = await ctx.send(embed=embed)
            for i in range(len(options)):
                await message.add_reaction(reactions[i])
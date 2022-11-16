from discord.ext import commands
from Plugin import AutomataPlugin
import discord
import matplotlib.pyplot as plt
import io 
from typing import List

def parseArguments(args: str) -> List[float]:
    """ Takes the arguments from barplot function 
        And converts it to a list of usable numbers. """
    
    if "," in args:
        temp = args.strip().split(",")
        return 
    else:
        temp =  args.strip().split()
    
    return list(map(float, temp))

class Chart(AutomataPlugin):
    """ A discord plugin for some chart related commands """

    @commands.command()
    async def barplot(self, ctx: commands.Context, *, args: str):
        """ Plots a bar chart """
        
        y: List[float] = parseArguments(args)
        x: List[int] = [i+1 for i in range(len(y))]

        # Plot
        plt.bar(x, y, label="Bars visualized")
        plt.legend(loc="upper right")
        
        # Get figure and save and load it in bytes
        fig = plt.gcf()
        buffer = io.BytesIO()
        fig.savefig(buffer, format="png")
        buffer.seek(0)
        
        # Close and clear plt data
        fig.clear()
        plt.close()

        picture = discord.File(buffer, "plot.png")

        await ctx.send(file=picture)
        buffer.close()


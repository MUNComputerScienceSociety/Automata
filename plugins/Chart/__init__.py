from discord.ext import commands
from Plugin import AutomataPlugin
import discord
import io 
from typing import List
import requests

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
        """ 
        Plots a bar chart 
        Fetch the barplot from an external API instead of using matplotlib internally
        """
        ENDPOINT = "https://funapi.onrender.com/api/barplot/"
        
        # Try parsing the data
        try:
            y: List[float] = parseArguments(args)
            y_str: List[str] = list(map(str, y))

            # Fetch request
            resp = requests.get(f'{ENDPOINT}?data={",".join(y_str)}')

            # Check if the the response is an actual image
            if resp.status_code == 200 and resp.headers["Content-Type"] == "image/png":
                # Create io buffer and image file
                buffer = io.BytesIO(resp.content)
                image = discord.File(buffer, "plot.png")

                await ctx.send(file=image)
                buffer.close()

            else:
                # Todo: Error
                pass
        
        except Exception:
            # Todo: Couldn't parse arguments
            pass
        


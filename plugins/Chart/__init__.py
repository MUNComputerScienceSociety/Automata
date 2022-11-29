from discord.ext import commands
from Plugin import AutomataPlugin
import discord
import io 
from typing import List
import requests
import datetime

# ==== UTIL FUNCTIONS =====
# TODO: Write unit tests

def parseArguments(args: str) -> List[str]:
    """ Takes the arguments from barplot function 
        And converts it to a list of string numbers. """
    
    if "," in args:
        temp = args.strip().split(",")
        return 
    else:
        temp =  args.strip().split()
    
    # Temp to ensure that all parameters are numbers
    temp = list(map(float, temp))
    return list(map(str, temp))

def getErrorEmbed(title="Error Title", message="Error Message") -> discord.Embed:
    """
    Generate an embed for error messages
    """
    emb = discord.Embed(
        title=message,
        timestamp=datetime.datetime.now(),
        colour = discord.Colour(0xEF440E)
    )
    emb.set_author(
        name=title,
        icon_url="https://i.imgur.com/UjdPxZw.png" # Potentially is not the safest. TODO: Find alternative solution
    )

    return emb

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

            # Fetch request
            resp = requests.get(f'{ENDPOINT}?data={",".join(y)}')

            # Check if the the response is an actual image
            if resp.status_code == 200 and resp.headers["Content-Type"] == "image/png":
                # Create io buffer and image file
                buffer = io.BytesIO(resp.content)
                image = discord.File(buffer, "plot.png")

                await ctx.send(file=image)
                buffer.close()

            else:
                # Todo: Error
                await ctx.send(embed=getErrorEmbed(title="API Error", message="An external API error occured."))
        
        except Exception:
            # Todo: Couldn't parse arguments
            await ctx.send(embed=getErrorEmbed(title="Invalid Usage", message="Please enter numeric parameters."))
        


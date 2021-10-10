from os import name
from discord import colour
from discord.ext import commands
import discord
import httpx
from Plugin import AutomataPlugin
from Globals import WEATHER_API_KEY

KEY = WEATHER_API_KEY
CALL_URI = f"http://api.weatherapi.com/v1/current.json?key={KEY}&q=A1B 3P7&aqi=no"

class Weather(AutomataPlugin):
    """A simple weather command to get the current weather cast."""

    @commands.command()
    async def weather(self, ctx: commands.Context):
        """Replies an embed of current weather"""

        async with httpx.AsyncClient() as client:
            resp = await client.get(CALL_URI)
        weather_data = resp.json()

        icon = weather_data["current"]["condition"]["icon"]

        embed = discord.Embed(
            title="St. John's Weather",
            description=weather_data["current"]["condition"]["text"],
            thumbnail= icon[2:len(icon)],
            colour = discord.Color.blue()
        )

        embed.add_field(name="Temperature 🌡️", value= str(weather_data["current"]["temp_c"]) +" C")
        embed.add_field(name="Feels Like", value= str(weather_data["current"]["feelslike_c"]) + " C")
        embed.add_field(name="Precipitation 🌧️" , value= str(weather_data["current"]["precip_mm"]) + "mm")
        embed.add_field(name="Humidity 💦", value= str(weather_data["current"]["humidity"]) + "%")
        embed.add_field(name="Cloud ☁️", value= str(weather_data["current"]["cloud"]) + "%")
        embed.add_field(name="Wind Speed 💨", value= str(weather_data["current"]["wind_kph"]) + " KPH")
        embed.add_field(name="Wind Direction 🧭", value= str(weather_data["current"]["wind_dir"]))
        await ctx.send(embed=embed)

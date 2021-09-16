
import discord
import requests
from discord.ext import commands
from Plugin import AutomataPlugin

URANDOM_ECOJI_URI = "https://jackharrhy.dev/urandom/ecoji/"
        
class Ecojistorm(AutomataPlugin):
  f"""Advanced tactical version of Ecoji"""
  
  @commands.command()
  async def ecojistorm(self, ctx: commands.Context, limit):
        limit = int(limit)
        while limit > 0:
          await ctx.send(requests.get(f"{URANDOM_ECOJI_URI}{limit}").text)
          limit-=1
      

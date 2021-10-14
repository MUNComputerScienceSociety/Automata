from discord import channel
from discord.ext import commands
import discord
from Plugin import AutomataPlugin
#from Globals import STARBOARD_CHANNEL, STARBOARD_THRESHOLD

STARBOARD_CHANNEL = 706658088995782677
STARBOARD_THRESHOLD = 1

class Starboard(AutomataPlugin):
    """Starboard"""

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction: discord.reaction, user: discord.user):
        """React with 5 ⭐'s on a message for adding a bookmark"""

        if reaction.emoji == '⭐':
            if reaction.count == STARBOARD_THRESHOLD:        
                channel1 = self.bot.get_channel(STARBOARD_CHANNEL)
                embedVar = discord.Embed(title="Original Message",url = reaction.message.jump_url, description = reaction.message.content, color = 0xFFFF00)
                embedVar.set_author(name=reaction.message.author.display_name,icon_url=reaction.message.author.avatar_url)
                await channel1.send(embed=embedVar)

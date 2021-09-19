from discord.ext import commands
import discord
from Plugin import AutomataPlugin


class Starboard(AutomataPlugin):
    """Starboard"""


    @commands.Cog.listener()
    async def on_reaction_add(self, reaction: discord.reaction, user: discord.user):
        #await reaction.message.channel.send(reaction.emoji.id)
        if reaction.emoji == '⭐':
            if reaction.count==1:        
                channel1 = discord.utils.get(discord.Client.get_all_channels(self), name='bookmark')
                #channel1 = commands.Bot.get_channel(878984320130355220)
                embedVar = discord.Embed(title="Original Message",url = reaction.message.jump_url, description = reaction.message.content, color = 0xFFFF00)
                embedVar.set_author(name=reaction.message.author.display_name,icon_url=reaction.message.author.avatar_url)
                #await channel1.send(reaction.message.content)
                await channel1.send(embed=embedVar)
        
            #await reaction.message.channel.send(reaction.message.content)
        #if 'star' in message.reactions:
            
        #    await message.channel.send('message')
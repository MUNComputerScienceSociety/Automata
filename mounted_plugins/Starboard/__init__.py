from datetime import datetime
from typing import Optional, Union

from discord import channel
from discord.ext import commands
import discord


from Plugin import AutomataPlugin
from Globals import mongo_client
    
#from Globals import STARBOARD_CHANNEL, STARBOARD_THRESHOLD

STARBOARD_CHANNEL = 706658088995782677
STARBOARD_THRESHOLD = 1

class Starboard(AutomataPlugin):
    """React with ⭐'s on a message to add a message to the starboard."""
    
    # Starboard entry: message_id, channel_id, user_id, timestamp

    def __init__(self, manifest, bot: commands.Bot):
        super().__init__(manifest, bot)

        self.starboard = mongo_client.automata.starboard_starboard

    def get_entry(
        self, *, message_id: int, channel_id: int
    ) -> Optional[Union[int, int, int, datetime.datetime]]:
        """Retrieve an entry from the starboard, if it exists.
        
        :param message_id: The message id of the starboard entry.
        :param channel_id: The channel id of the channel the starboard entry was sent in.
        :return: The starboard message, if it exists
        :rtype: ???
        """
        pass

    def add_entry(
        self, *, message_id: int, channel_id: int, user_id: int, timestamp: datetime = datetime.now()
    ) -> bool:
        """Add an entry to the starboard, if it does not already exist.
        :param message_id: The message id of the starboard entry.
        :param channel_id: The channel id of the channel the starboard entry was sent in.
        :param user_id: The user that sent the message to be added.
        :param timestamp: Optionally provide a time to store, otherwise uses current time.
        :return: True or false, depending on if the operation was successful or not.
        :rtype: bool
        """
        pass


    @commands.Cog.listener()
    async def on_reaction_add(self, reaction: discord.reaction, user: discord.user):

        if reaction.emoji == '⭐':
            if reaction.count == STARBOARD_THRESHOLD:        
                channel1 = self.bot.get_channel(STARBOARD_CHANNEL)
                embedVar = discord.Embed(title="Original Message",url = reaction.message.jump_url, description = reaction.message.content, color = 0xFFFF00)
                embedVar.set_author(name=reaction.message.author.display_name,icon_url=reaction.message.author.avatar_url)
                await channel1.send(embed=embedVar)

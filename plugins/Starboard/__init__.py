from datetime import datetime
from logging import StreamHandler
from typing import Dict, Optional, Union

import discord
from discord.ext import commands

from Plugin import AutomataPlugin
from Globals import STARBOARD_CHANNEL_ID, STARBOARD_THRESHOLD


class Starboard(AutomataPlugin):
    """React with ⭐'s on a message to add a message to the starboard."""

    def __init__(self, manifest, bot: commands.Bot):
        super().__init__(manifest, bot)

    async def cog_load(self):
        self.starboard = self.bot.database.automata.starboard_starboard

    async def get_entry(
        self,
        *,
        message: Union[discord.Message, int],
        channel: Union[discord.TextChannel, int],
    ) -> Optional[Dict[str, Union[str, int, datetime]]]:
        """Retrieve an entry from the starboard, if it exists.

        :param message: The message of the starboard entry.
        :param message: Union[discord.Message, int]
        :param channel: The channel the starboard entry was sent in.
        :param channel: Union[discord.TextChannel, int]
        :return: The starboard message, if it exists
        :rtype: Optional[Dict[str, Union[str, int, datetime]]]
        """

        message_id = self._get_id(message)
        channel_id = self._get_id(channel)
        query = {}
        query["message_id"] = message_id
        query["channel_id"] = channel_id
        entry = await self.starboard.find_one(query)
        return entry

    async def add_entry(
        self,
        *,
        message: Union[discord.Message, int],
        channel: Union[discord.TextChannel, int],
        user: Union[discord.User, int],
        timestamp: Optional[datetime] = datetime.now(),
    ) -> bool:
        """Add an entry to the starboard, if it does not already exist.
        :param message: The message of the starboard entry.
        :param message: Union[discord.Message, int]
        :param channel_id: The channel the starboard entry was sent in.
        :param channel_id: Union[discord.TextChannel, int]
        :param user_id: The user that sent the message to be added.
        :param user_id: Union[discord.User, int]
        :param timestamp: Optionally provide a time to store, otherwise uses current time.
        :param timestamp: datetime, optional
        :return: True or false, depending on if the operation was successful or not.
        :rtype: bool
        """
        message_id = self._get_id(message)
        channel_id = self._get_id(channel)
        user_id = self._get_id(user)
        if await self.get_entry(message=message_id, channel=channel_id) is not None:
            return False
        await self.starboard.insert_one(
            {
                "message_id": message_id,
                "channel_id": channel_id,
                "user_id": user_id,
                "timestamp": timestamp,
            }
        )
        return True

    def _format_starboard_embed(self, message: discord.Message) -> discord.Embed:
        """Generates a formatted embed for a given starboard message"""
        embed = discord.Embed(title="Original Message", color=0xFFFF00)
        embed.url = message.jump_url
        embed.description = message.content

        urls = []

        for a in message.attachments:
            if "image" in a.content_type and embed.image != discord.Embed.Empty:
                embed.set_image(url=a.url)
            else:
                urls.append(a.url)

        if len(urls) > 0:
            embed.description += "\n".join(urls)

        embed.set_author(
            name=message.author.display_name, icon_url=message.author.display_avatar
        )
        post_date = message.created_at.strftime("%B %d, %Y")
        embed.set_footer(text=f"Posted on {post_date}")

        return embed

    def _get_id(
        self,
        id_or_object: Union[discord.Message, discord.TextChannel, discord.User, int],
    ) -> int:
        """Returns the ID of a discord object/id union"""
        if type(id_or_object) is int:
            return id_or_object
        else:
            return id_or_object.id

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction: discord.Reaction, user: discord.Member):
        if user.bot or not reaction.emoji == "⭐":
            return

        if (
            reaction.count != STARBOARD_THRESHOLD
            or reaction.message.channel.id == STARBOARD_CHANNEL_ID
        ):
            return

        message = reaction.message
        channel = message.channel
        user = message.author

        if (await self.get_entry(message=message, channel=channel)) is not None:
            return

        starboard_channel = message.guild.get_channel(STARBOARD_CHANNEL_ID)
        embed = self._format_starboard_embed(message=message)
        await starboard_channel.send(embed=embed)
        await self.add_entry(message=message, channel=channel, user=user)

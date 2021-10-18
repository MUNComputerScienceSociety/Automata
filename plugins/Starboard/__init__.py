from datetime import datetime
from typing import Dict, Optional, Union

import nextcord
from discord.ext import commands

from Plugin import AutomataPlugin
from Globals import mongo_client, STARBOARD_CHANNEL_ID, STARBOARD_THRESHOLD


class Starboard(AutomataPlugin):
    """React with ⭐'s on a message to add a message to the starboard."""

    def __init__(self, manifest, bot: commands.Bot):
        super().__init__(manifest, bot)

        self.starboard = mongo_client.automata.starboard_starboard

    async def get_entry(
        self,
        *,
        message: Union[nextcord.Message, int],
        channel: Union[nextcord.TextChannel, int],
    ) -> Optional[Dict[str, Union[str, int, datetime]]]:
        """Retrieve an entry from the starboard, if it exists.

        :param message: The message of the starboard entry.
        :param message: Union[nextcord.Message, int]
        :param channel: The channel the starboard entry was sent in.
        :param channel: Union[nextcord.TextChannel, int]
        :return: The starboard message, if it exists
        :rtype: Optional[Dict[str, Union[str, int, datetime]]]
        """
        if isinstance(message, int):
            message_id = message
        elif message is not None:
            message_id = message.id
        if isinstance(channel, int):
            channel_id = channel
        elif channel is not None:
            channel_id = channel.id
        query = {}
        if message is not None and channel is not None:
            query["message_id"] = message_id
            query["channel_id"] = channel_id
        entry = await self.starboard.find_one(query)
        return entry

    async def add_entry(
        self,
        *,
        message: Union[nextcord.Message, int],
        channel: Union[nextcord.TextChannel, int],
        user: Union[nextcord.User, int],
        timestamp: Optional[datetime] = datetime.now(),
    ) -> bool:
        """Add an entry to the starboard, if it does not already exist.
        :param message: The message of the starboard entry.
        :param message: Union[nextcord.Message, int]
        :param channel_id: The channel the starboard entry was sent in.
        :param channel_id: Union[nextcord.TextChannel, int]
        :param user_id: The user that sent the message to be added.
        :param user_id: Union[nextcord.User, int]
        :param timestamp: Optionally provide a time to store, otherwise uses current time.
        :param timestamp: datetime, optional
        :return: True or false, depending on if the operation was successful or not.
        :rtype: bool
        """
        if isinstance(message, int):
            message_id = message
        elif message is not None:
            message_id = message.id
        if isinstance(channel, int):
            channel_id = channel
        elif channel is not None:
            channel_id = channel.id
        if isinstance(user, int):
            user_id = user
        elif user is not None:
            user_id = user.id
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

    def _format_starboard_embed(self, message: nextcord.Message) -> nextcord.Embed:
        """Generates a formatted embed for a given starboard message"""
        embed = nextcord.Embed(title="Original Message", color=0xFFFF00)
        embed.url = message.jump_url
        embed.description = message.content

        urls = []

        for a in message.attachments:
            if "image" in a.content_type and embed.image != nextcord.Embed.Empty:
                embed.set_image(url=a.url)
            else:
                urls.append(a.url)

        if len(urls) > 0:
            embed.description += "\n".join(urls)

        embed.set_author(
            name=message.author.display_name, icon_url=message.author.display_avatar
        )
        post_date = message.created_at.strftime("%B %m, %Y")
        embed.set_footer(text=f"Posted on {post_date}")

        return embed

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction: nextcord.Reaction, user: nextcord.Member):
        if not user.bot and reaction.emoji == "⭐":
            if (
                reaction.count == STARBOARD_THRESHOLD
                and reaction.message.channel.id != STARBOARD_CHANNEL_ID
            ):
                message = reaction.message
                channel = message.channel
                user = message.author

                if (await self.get_entry(message=message, channel=channel)) is not None:
                    return

                starboard_channel = message.guild.get_channel(STARBOARD_CHANNEL_ID)
                embed = self._format_starboard_embed(message=message)
                await starboard_channel.send(embed=embed)
                await self.add_entry(message=message, channel=channel, user=user)

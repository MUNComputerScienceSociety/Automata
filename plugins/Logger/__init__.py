from datetime import datetime

import discord
from discord.ext import commands

from Plugin import AutomataPlugin
from Globals import mongo_client


class Logger(AutomataPlugin):
    """Provides logging services."""

    def __init__(self, manifest, bot):
        super().__init__(manifest, bot)
        self.events = mongo_client.automata.logger_events

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        await self.events.insert_one(
            {
                "author_id": message.author.id,
                "channel_id": message.channel.id,
                "message_id": message.id,
                "content": message.content,
                "type": "message_sent",
                "timestamp": message.created_at,
            }
        )

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        await self.events.insert_one(
            {
                "author_id": message.author.id,
                "channel_id": message.channel.id,
                "message_id": message.id,
                "type": "message_deleted",
                "timestamp": datetime.utcnow(),
            }
        )

    @commands.Cog.listener()
    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        await self.events.insert_one(
            {
                "author_id": after.author.id,
                "channel_id": after.channel.id,
                "message_id": after.id,
                "type": "message_deleted",
                "timestamp": after.edited_at,
                "old_content": before.content,
                "new_content": after.content,
            }
        )

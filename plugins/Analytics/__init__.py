import discord
from discord.ext import commands
from prometheus_client import Counter, Gauge

from Plugin import AutomataPlugin
from Globals import mongo_client

MESSAGES = Counter(
    "automata_message_count", "Total number of messages sent.", ["channel"]
)
MEMBERS = Gauge("automata_member_count", "Number of members in the server", ["status"])


class Analytics(AutomataPlugin):
    """Provides statistics and analystics tracking services."""

    def __init__(self, manifest, bot: commands.Bot):
        super().__init__(manifest, bot)
        self.message_counts = mongo_client.automata.analytics_message_counts

    def _set_member_count(self) -> None:
        totals = {"total": 0, "online": 0, "offline": 0, "idle": 0, "dnd": 0}
        for member in self.bot.get_guild(514110851016556567).members:
            totals[member.status.value] += 1
            totals["total"] += 1
        for label, value in totals.items():
            MEMBERS.labels(label).set(value)

    @commands.Cog.listener()
    async def on_ready(self):
        cursor = self.message_counts.find()
        for channel in await cursor.to_list(length=None):
            guild_channel = self.bot.get_guild(514110851016556567).get_channel(
                channel["channel_id"]
            )
            MESSAGES.labels(guild_channel.name).inc(channel["count"])
        self._set_member_count()

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """Process incoming messages, updating the relevant counters on Prometheus."""
        if not isinstance(message.channel, discord.abc.PrivateChannel):
            existing_count = await self.message_counts.find_one(
                {"channel_id": message.channel.id}
            )
            if existing_count is not None:
                await self.message_counts.update_one(
                    {"channel_id": message.channel.id}, {"$inc": {"count": 1}}
                )
            else:
                await self.message_counts.insert_one(
                    {"channel_id": message.channel.id, "count": 1}
                )
            MESSAGES.labels(message.channel.name).inc(1)

    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        """Handle member update events, updating the relevant gague on Prometheus."""
        self._set_member_count()

import discord
from discord.ext import commands
from prometheus_client import Counter, Gauge

from Plugin import AutomataPlugin

MESSAGES = Counter("automata_message_count", "Total number of messages sent.", ["channel"])
MEMBERS = Gauge("automata_member_count", "Number of members in the server", ["status"])


class Analytics(AutomataPlugin):
    """Provides statistics and analystics tracking services."""

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """Process incoming messages, updating the relevant counters on Prometheus."""
        MESSAGES.labels(message.channel.name).inc(1)

    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        """Handle member update events, updating the relevant gague on Prometheus."""
        totals = {
            "total": 0,
            "online": 0,
            "offline": 0,
            "idle": 0,
            "dnd": 0
        }
        for member in self.bot.get_guild(514110851016556567).members:
            totals[member.status.value] += 1
            totals["total"] += 1
        for label, value in totals.items():
            MEMBERS.labels(label).set(value)

import time

from nextcord.ext import commands

from Plugin import AutomataPlugin


class Uptime(AutomataPlugin):
    """See how long Automata has been running"""

    startup_time = int(time.time())

    @commands.command()
    async def uptime(self, ctx):
        """Replies with the current uptime for this bot"""

        await ctx.message.reply(
            f"I have been awake for {self.time_since(self.startup_time)}."
        )

    def time_since(self, comparison_time):
        """
        Returns a human-readable representation of the elapsed time since the given time argument.

        Args:
            comparison_time: The time being compared to the current time. Expressed as epoch time in seconds.
        """
        days = divmod(int(time.time()) - comparison_time, 86400)
        hours = divmod(days[1], 3600)
        minutes = divmod(hours[1], 60)
        seconds = minutes[1]

        output = ""
        if days[0] > 0:
            output += str(days[0]) + (" day, " if days[0] == 1 else " days, ")
        if hours[0] > 0:
            output += str(hours[0]) + (" hour, " if hours[0] == 1 else " hours, ")
        if minutes[0] > 0:
            output += str(minutes[0]) + (
                " minute, " if minutes[0] == 1 else " minutes, "
            )
        if seconds > 0:
            output += str(seconds) + (" second" if seconds == 1 else " seconds")

        return output

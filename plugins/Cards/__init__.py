from discord.ext import commands

from Plugin import AutomataPlugin
from .deck import Deck


class Cards(AutomataPlugin):
    """
    Miscellaneous playing card games / tasks
    Built using https://deckofcardsapi.com/
    """

    def __init__(self, manifest, bot: commands.Bot):
        super().__init__(manifest, bot)

    @commands.group()
    async def cards(self, ctx: commands.Context):
        await ctx.trigger_typing()
        if ctx.invoked_subcommand is None:
            await ctx.reply(content="Invalid command, check !help cards")

    @cards.command(name="random", aliases=["r"])
    async def cards_random(self, ctx: commands.Context):
        """Sends an image of a random card to the channel"""
        deck = await Deck.create()
        [card] = await deck.draw()
        await ctx.reply(card.image)

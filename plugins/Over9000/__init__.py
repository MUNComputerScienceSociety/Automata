from random import choice
import discord
from discord.ext import commands

from Plugin import AutomataPlugin


class Over9000(AutomataPlugin):
    """Kakarot"""

    quotes_list = ["Well, if your friend is stronger than you, \n"
                   "I guess you're the third strongest Saiyan now.",
                   
                   "I'm the Saiyan who came all the way from Earth for\n"
                   "the sole purpose of beating you. I am the warrior \n" 
                   "you've heard of in the legends, pure of heart and\n" 
                   "awakened by fury - that's what I am.",

                   "I am the hope of the universe....I am the answer to all\n"
                   "living things that cry out for peace...I am the protector\n"
                   "of the innocent...I am the light in the darkness...I am truth.\n"
                   "Ally to good... Nightmare to you!!!"
                   ]

    @commands.command()
    async def over9000(self, ctx: commands.Context, quotes=quotes_list):
        """Replies with a super saiyan emoji and random
        Goku quote!"""

        await ctx.send(f"ᕙ(⇀‸↼‶)ᕗ\n{choice(quotes_list)}")

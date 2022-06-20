import httpx
from discord.ext import commands
from Plugin import AutomataPlugin
from plugins.Continue.gptj import gptj_query, gptj_query_simple


class Continue(AutomataPlugin):
    """Continues a prompt using GPT-J"""

    @commands.command(aliases=["continue"])
    async def gpt(self, ctx: commands.Context, *, prompt: str):
        """Continues your prompt with the default parameters"""
        res = await gptj_query_simple(prompt)
        await ctx.send(f"{prompt}{str(res)}...")

    @commands.command(aliases=["continueadv", "continueadvanced"])
    async def gpt_adv(
        self,
        ctx: commands.Context,
        temperature: float,
        top_probability: float,
        max_length: int,
        *,
        prompt: str,
    ):
        """Continues your prompt with custom creativity, randomness and length \n(Defaults are 0.8, 0.9 and 100 respectively)"""
        res = await gptj_query(
            prompt,
            max_length=max_length,
            temperature=temperature,
            top_probability=top_probability,
        )
        await ctx.send(f"{prompt}{str(res)}...")

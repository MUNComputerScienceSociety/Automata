import re

from discord.ext import commands
import httpx

from Plugin import AutomataPlugin

BARAB_API = "https://jackharrhy.dev/barab"
CODE_BLOCK_REGEX = "```[a-z]*\n(?P<content>[\s\S]*?)\n```"
HEADERS = {"Content-Type": "text/plain"}

code_block = re.compile(CODE_BLOCK_REGEX)


class Verilog(AutomataPlugin):
    """
    Verilog
    Made using https://jackharrhy.dev/barab
    """

    @commands.command()
    async def verilog(self, ctx: commands.Context):
        """Executes all code blocks in your message as verilog"""

        code = "\n\n".join(code_block.findall(ctx.message.content))

        async with httpx.AsyncClient() as client:
            response = await client.post(
                BARAB_API, headers=HEADERS, content=code.encode(), timeout=15.0
            )

        text = response.text.replace("````", "\`\`\`")
        await ctx.send(f"```{text}```")

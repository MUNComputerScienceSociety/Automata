from discord.ext import commands

from automata.utils import CommandContext, Plugin

pointer, data, output = None, None, None


def find_end(source: str) -> int:
    loops = 1
    for i in range(len(source)):
        loops += (source[i] == "[") - (source[i] == "]")
        if not loops:
            return i + 1


def execute(source, in_loop=False):
    global pointer, data, output
    i = 0
    if not in_loop:
        pointer, data, output = 0, [0] * 30000, ""
    while i < len(source):
        pointer += (source[i] == ">") - (source[i] == "<")
        pointer %= 30000
        data[pointer] += (source[i] == "+") - (source[i] == "-")
        if source[i] == ".":
            output += chr(data[pointer] % 256)
        elif source[i] == ",":
            data[pointer] = ord(input("\n"))
        elif source[i] == "[":
            j = find_end(source[i + 1 :])
            execute_loop(source[i + 1 : j + i])
            i += j
        i += 1
    if in_loop:
        return data
    return output


def execute_loop(source):
    while execute(source, True)[pointer] % 256:
        pass


class Brainf(Plugin):
    """Brainf*ck"""

    @commands.command()
    async def bf(self, ctx: CommandContext, message: str):
        """Responds with the output of running the message in brainf*ck"""

        await ctx.send(execute(message))

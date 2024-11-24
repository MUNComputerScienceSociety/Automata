from time import sleep

import httpx
from bs4 import BeautifulSoup
from discord.ext import commands

from automata.utils import CommandContext, Plugin


class Man(Plugin):
    """Linux man command via man7.org"""

    cached = {}

    def __init__(self, bot: commands.Bot):
        super().__init__(bot)
        pages = []
        for i in range(9):
            r = httpx.get(url=f"https://man7.org/linux/man-pages/dir_section_{i}.html")
            sleep(0.1)
            pages.append(BeautifulSoup(r.text, "html.parser"))
        for i, x in enumerate(pages):
            links = x.find_all("a")
            for j, y in enumerate(links):
                if f"man{i}" in y["href"]:
                    if y["href"][5:-5][0] in "012345678":
                        if y.string.split("(")[0] in self.cached:
                            if (
                                self.cached[y.string.split("(")[0]][0]
                                != "There were multiple results:"
                            ):
                                self.cached[y.string.split("(")[0]].insert(
                                    0, "There were multiple results:"
                                )
                            self.cached[y.string.split("(")[0]].append(y["href"][5:-5])
                        else:
                            self.cached[y.string.split("(")[0]] = [y["href"][5:-5]]

    @staticmethod
    def urlfy(s: str = ""):
        if s[0] in "012345678":
            return "https://man7.org/linux/man-pages/man" + s + ".html"
        else:
            return s

    @commands.command()
    async def man(self, ctx: CommandContext, search: str = ""):
        """Searches man7.org for the requested man page"""
        try:
            if search == "":
                await ctx.send("No search request given :(")
            elif search in self.cached:
                if len(self.cached[search]) == 1:
                    await ctx.send(Man.urlfy(self.cached[search][0]))
                else:
                    s = "\n".join(map(Man.urlfy, self.cached[search]))
                    await ctx.send(s)
            else:
                res = []
                for i in range(1, 9):
                    r = httpx.get(
                        url=f"https://man7.org/linux/man-pages/man{i}/{search}.{i}.html"
                    )
                    sleep(0.1)
                    if r.status_code == 200:
                        res.append(i)
                if len(res) == 0:
                    self.cached[search] = [f"No manual entry for {search}"]
                    await ctx.send(f"No manual entry for {search}")
                elif len(res) == 1:
                    self.cached[search] = [f"{res[0]}/{search}.{res[0]}"]

                    await ctx.send(
                        f"https://man7.org/linux/man-pages/man{res[0]}/{search}.{res[0]}.html"
                    )
                else:
                    s = ["There were multiple results:"]
                    for x in res:
                        s.append(f"{x}/{search}.{x}")
                    self.cached[search] = s
                    await ctx.send("\n".join(s))
        except Exception as e:
            await ctx.send(f"There was an error finding the man page for {search}")
            raise e

from time import sleep
import requests
from bs4 import BeautifulSoup

from nextcord.ext import commands

from Plugin import AutomataPlugin


class Man(AutomataPlugin):
    """Linux man command via man7.org"""

    cached = {}

    def __init__(self, manifest, bot: commands.Bot):
        super().__init__(manifest, bot)
        pages = []
        for i in range(8):
            r = requests.get(
                url=f"https://man7.org/linux/man-pages/dir_section_{i}.html"
            )
            sleep(0.1)
            pages.append(BeautifulSoup(r.text, "html.parser"))
        for i, x in enumerate(pages):
            links = x.find_all("a")
            for j, y in enumerate(links):
                if f"man{i}" in y["href"]:
                    if y.string.split("(")[0] in self.cached:
                        self.cached[y.string.split("(")[0]].append(
                            "https://man7.org/linux/man-pages" + y["href"][1:]
                        )
                    else:
                        self.cached[y.string.split("(")[0]] = [
                            "https://man7.org/linux/man-pages" + y["href"][1:]
                        ]

    @commands.command()
    async def man(self, ctx: commands.Context, search: str = ""):
        """Searches man7.org for the requested man page"""
        try:
            if search == "":
                await ctx.send("No search request given :(")
            elif search in cached:
                if len(cached[search]) == 1:
                    await ctx.send(cached[search])
                else:
                    s = "There were multiple results:\n"
                    s += "\n".join(cached[search])
                    await ctx.send(s)
            else:
                self.cached[search] = f"No manual entry for {search}"
                await ctx.send(f"No manual entry for {search}")
                res = []
                for i in range(1, 9):
                    r = requests.get(
                        url=f"https://man7.org/linux/man-pages/man{i}/{search}.{i}.html"
                    )
                    sleep(0.1)
                    if r.status_code == 200:
                        res.append(i)
                if len(res) == 0:
                    self.cached[search] = f"No manual entry for {search}"
                    await ctx.send(f"No manual entry for {search}")
                elif len(res) == 1:
                    self.cached[
                        search
                    ] = f"https://man7.org/linux/man-pages/man{res[0]}/{search}.{res[0]}.html"
                    await ctx.send(
                        f"https://man7.org/linux/man-pages/man{res[0]}/{search}.{res[0]}.html"
                    )
                else:
                    s = "There were multiple results:\n"
                    for x in res:
                        s += f"https://man7.org/linux/man-pages/man{x}/{search}.{x}.html\n"
                    s = s[:-1]
                    self.cached[search] = s
                    await ctx.send(s)
        except Exception as e:
            await ctx.send(f"There was an error finding the man page for {search}")
            raise e

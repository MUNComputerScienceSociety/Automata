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
        for i in range(9):
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
                        if self.cached[y.string.split("(")[0]][0] != "There were multiple results:":
                            self.cached[y.string.split("(")[0]].insert(0, "There were multiple results:")
                        self.cached[y.string.split("(")[0]].append(
                            y["href"][5:-5]
                        )
                    else:
                        self.cached[y.string.split("(")[0]] = [
                            y["href"][5:-5]
                        ]

    def urlfy(s: str = ""):
        if s[0] in [0,1,2,3,4,5,6,7,8]:
            return "https://man7.org/linux/man-pages/man" + s + ".html"
        else:
            return s

    @commands.command()
    async def man(self, ctx: commands.Context, search: str = ""):
        """Searches man7.org for the requested man page"""
        try:
            if search == "":
                await ctx.send("No search request given :(")
            elif search in cached:
                if len(cached[search]) == 1:
                    await ctx.send(urlfy(cached[search][0]))
                else:
                    s = "\n".join(map(urlfy,cached[search]))
                    await ctx.send(s)
            else:
                raise TypeError
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
                    ] = f"{res[0]}/{search}.{res[0]}"
                    await ctx.send(
                        f"https://man7.org/linux/man-pages/man{res[0]}/{search}.{res[0]}.html"
                    )
                else:
                    s = ["There were multiple results:"]
                    for x in res:
                        s.append(f"{x}/{search}.{x}"
                    self.cached[search] = s
                    await ctx.send("\n".join(s))
        except Exception as e:
            await ctx.send(f"There was an error finding the man page for {search}")
            raise e

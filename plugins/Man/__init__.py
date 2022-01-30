from time import sleep
import requests

from nextcord.ext import commands

from Plugin import AutomataPlugin


class Man(AutomataPlugin):
    """Linux man command via man7.org"""

    cached = {}

    @commands.command()
    async def man(self, ctx: commands.Context, search: str = ""):
        """Searches man7.org for the requested man page"""
        try:
            res = []
            if search == "":
                await ctx.send("No search request given :(")
                return
            elif search in self.cached:
                await ctx.send(self.cached[search])
                return
            else:
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
                x = res[0]
                self.cached[
                    search
                ] = "https://man7.org/linux/man-pages/man{x}/{search}.{x}.html".format(
                    x=x, search=search
                )
                await ctx.send(
                    "https://man7.org/linux/man-pages/man{x}/{search}.{x}.html".format(
                        x=x, search=search
                    )
                )
            else:
                s = "There were multiple results:\n"
                for x in num:
                    s += "https://man7.org/linux/man-pages/man{x}/{search}.{x}.html\n".format(
                        x=x, search=search
                    )
                s = s[:-1]
                self.cached[search] = s
                await ctx.send(s)
        except:
            ctx.send(f"There was an error finding the man page for {search}")

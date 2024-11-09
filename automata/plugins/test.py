from discord.ext import commands


class Test(commands.Cog):
    async def cog_load(self):
        print("loaded!")

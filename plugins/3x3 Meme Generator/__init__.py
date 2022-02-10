import urllib.parse
import asyncio
from nextcord import http
from nextcord.ext import commands
import nextcord
import httpx
from nextcord.threads import Thread
from Globals import mongo_client
from Plugin import AutomataPlugin
from pymongo import collection


API = "https://awful-3x3-meme-generator.herokuapp.com"


class Generator(AutomataPlugin):
    """
    Generates a meme that's probably already dead
    """

    def __init__(self, manifest, bot):
        super().__init__(manifest, bot)
        self.gen3x3_sessions: collection.Collection = (
            mongo_client.automata.gen3x3_sessions
        )
        self.gen3x3_session_counter: collection.Collection = (
            mongo_client.automata.gen3x3_session_counter
        )
        loop = asyncio.get_event_loop()
        document_count = loop.run_until_complete(
            self.gen3x3_session_counter.count_documents({})
        )
        if document_count == 0:
            self.gen3x3_session_counter.insert_one({"counter": 0})

    @commands.command()
    async def gen3x3(
        self,
        ctx: commands.Context,
        lawful_good,
        neutral_good,
        chaotic_good,
        lawful_neutral,
        true_neutral,
        chaotic_neutral,
        lawful_evil,
        neutral_evil,
        chaotic_evil,
    ):
        """Responds with a meme that's probably already dead"""

        params = {
            "lg": lawful_good,
            "ng": neutral_good,
            "cg": chaotic_good,
            "ln": lawful_neutral,
            "tn": true_neutral,
            "cn": chaotic_neutral,
            "le": lawful_evil,
            "ne": neutral_evil,
            "ce": chaotic_evil,
        }

        error_check = httpx.get(f"{API}/api", params=params).text

        await ctx.send(
            error_check
            if error_check[1:16] == "Malformed input"
            else f"{API}/api?{urllib.parse.urlencode(params)}"
        )

    @commands.command()
    async def gen3x3start(self, ctx: commands.Context):
        message = await ctx.send("Creating 3x3 Generation Session")
        await self.gen3x3_session_counter.update_one({}, {"$inc": {"counter": 1}})
        counter_obj = await self.gen3x3_session_counter.find_one()
        id = counter_obj["counter"]
        thread = await message.create_thread(name=f"Gen 3x3 Session {id}")
        alignments = {
            "lg": None,
            "ng": None,
            "cg": None,
            "ln": None,
            "tn": None,
            "cn": None,
            "le": None,
            "ne": None,
            "ce": None,
        }
        await self.gen3x3_sessions.insert_one(
            {"id": id, "thread": thread.id, "alignments": alignments}
        )
        await thread.trigger_typing()
        await asyncio.sleep(5)
        await thread.send(
            "Please use the gen3x3set command followed by one of the following and a link to an image to set the alignments: \nlg, ng, cg, ln, tn, cn, le, ne, ce"
        )
        await thread.trigger_typing()
        await asyncio.sleep(1)
        await thread.send('For example "!gen3x3set lg https://i.imgur.com/V73crmb.jpg"')
        await thread.trigger_typing()
        await asyncio.sleep(3)
        await thread.send(
            "Once all alignments have been set use the gen3x3publish command to publish the image beck to the main channel."
        )
        await thread.trigger_typing()
        await asyncio.sleep(1)
        await thread.send(
            "You can overwrite any of the alignments at any point before it's published"
        )

    async def set_check(self, content: str):
        res = httpx.get(f"{API}/test", params={"image_url": content}).text
        return res == "Valid"

    @commands.command()
    async def gen3x3set(self, ctx: commands.Context, alignment: str, *, content: str):
        res = await self.gen3x3_sessions.find_one({"thread": ctx.message.channel.id})
        if not res:
            await ctx.send(
                "This command can only be used in a thread created with the gen3x3start command (that is not yet archived)"
            )
            return
        thread = ctx.message.channel
        check = await self.set_check(content)
        if not check:
            await thread.send("That doesn't seem to be a valid image url")
            return
        res["alignments"][alignment] = content
        await self.gen3x3_sessions.update_one(
            {"id": res["id"]}, {"$set": {"alignments": res["alignments"]}}
        )
        await thread.send(f"Set {alignment} to: {content}")

    @commands.command()
    async def gen3x3get(self, ctx: commands.Context, alignment: str):
        res = await self.gen3x3_sessions.find_one({"thread": ctx.message.channel.id})
        if not res:
            await ctx.send(
                "This command can only be used in a thread created with the gen3x3start command (that is not yet archived)"
            )
            return
        thread = ctx.message.channel
        await thread.send(f"Current {alignment} value: {res['alignments'][alignment]}")

    def publish_check(self, alignments: dict):
        errors = []
        keys = alignments.keys()
        for key in keys:
            if alignments[key] == None:
                errors.append(key)
        return errors

    @commands.command()
    async def gen3x3publish(self, ctx: commands.Context):
        res = await self.gen3x3_sessions.find_one({"thread": ctx.message.channel.id})
        if not res:
            await ctx.send(
                "This command can only be used in a thread created with the gen3x3start command (that is not yet archived)"
            )
            return
        thread: Thread = ctx.message.channel
        empty_alignments = self.publish_check(res["alignments"])
        if len(empty_alignments) != 0:
            await thread.send(
                f"The following alignments have not been assigned yet: \n{', '.join(empty_alignments)}"
            )
            return
        await self.gen3x3_sessions.delete_one({"thread": thread.id})
        await thread.edit(archived=True)
        channel = thread.parent
        image_url = f"{API}/api?{urllib.parse.urlencode(res['alignments'])}"
        await channel.send(f"Published image from Session {res['id']}:")
        await channel.send(image_url)

    @commands.command()
    async def gen3x3preview(self, ctx: commands.Context):
        res = await self.gen3x3_sessions.find_one({"thread": ctx.message.channel.id})
        if not res:
            await ctx.send(
                "This command can only be used in a thread created with the gen3x3start command (that is not yet archived)"
            )
            return
        temp_grid = {}
        keys = res["alignments"].keys()
        for key in keys:
            if res["alignments"][key] == None:
                temp_grid[key] = "https://via.placeholder.com/200"
            else:
                temp_grid[key] = res["alignments"][key]
        image_url = f"{API}/api?{urllib.parse.urlencode(temp_grid)}"
        await ctx.send("Preview Image: ")
        await ctx.send(image_url)

    # Admin only utility commands
    @commands.command()
    async def gen3x3count(self, ctx: commands.Context):
        if ctx.message.author.guild_permissions.administrator:
            active_sessions = await self.gen3x3_sessions.count_documents({})
            await ctx.send(
                f"Currently there are {active_sessions} active Gen 3x3 Sessions"
            )

    @commands.command()
    async def gen3x3clearall(self, ctx: commands.Context):
        if ctx.message.author.guild_permissions.administrator:
            count = 0
            async for session in self.gen3x3_sessions.find():
                thread = ctx.channel.get_thread(session["thread"])
                await thread.edit(archived=True)
                count += 1
            await self.gen3x3_sessions.delete_many({})
            await ctx.send(f"{count} Sessions archived and deleted")

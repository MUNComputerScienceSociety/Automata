import asyncio
from datetime import datetime
import httpx
import discord
from discord.ext import commands, tasks

from Plugin import AutomataPlugin
from Globals import (
    mongo_client,
    PRIMARY_GUILD,
    EXECUTIVE_DOCS_CHANNEL,
)

EXECUTIVE_DOCS_BASE_URI = "https://www.cs.mun.ca/~csclub/executive-documents"
EXECUTIVE_DOCS_JSON_URI = f"{EXECUTIVE_DOCS_BASE_URI}/docs.json"
CS_LOGO_COLOR_SQUARE_TRANSPARENT = (
    "https://www.cs.mun.ca/~csclub/assets/logos/color-square-trans.png"
)
DOC_TYPE_TO_COLOUR = {
    "Minutes": discord.Colour.lighter_gray(),
    "Agendas": discord.Colour.dark_gray(),
}


class ExecutiveDocs(AutomataPlugin):
    """Posts new executive documents"""

    def doc_embed(self, doc):
        embed = discord.Embed(
            title=f"Meeting {doc['type']} | {doc['time'].strftime('%A, %B %e, %Y')}",
            description=doc["url"],
            url=doc["url"],
            colour=DOC_TYPE_TO_COLOUR.get(doc["type"], discord.Colour.dark_blue()),
            timestamp=doc["time"],
        )
        embed.set_footer(
            text="Executive Documents", icon_url=CS_LOGO_COLOR_SQUARE_TRANSPARENT
        )
        return embed

    async def post_new_doc(self, doc):
        embed = self.doc_embed(doc)
        await self.bot.get_guild(PRIMARY_GUILD).get_channel(
            EXECUTIVE_DOCS_CHANNEL
        ).send(embed=embed)
        await self.posted_documents.insert_one(doc)

    async def fetch_docs_json(self):
        async with httpx.AsyncClient() as client:
            resp = await client.get(EXECUTIVE_DOCS_JSON_URI)
        return resp.json()

    async def post_new_docs(self):
        docs_json = await self.fetch_docs_json()

        for doc in docs_json:
            doc["time"] = datetime.strptime(doc["time"], "%Y-%m-%d %H:%M:%S")
            doc["url"] = f"{EXECUTIVE_DOCS_BASE_URI}/{doc['path']}"

        docs_json.sort(key=lambda doc: doc["time"])

        for doc in docs_json:
            potential_doc = await self.posted_documents.find_one({"path": doc["path"]})

            if potential_doc is None:
                await self.post_new_doc(doc)
                await asyncio.sleep(5.0)

    def __init__(self, manifest, bot: commands.Bot):
        super().__init__(manifest, bot)

        self.posted_documents = mongo_client.automata.executivedocs_posted_documents

    def cog_load(self):
        self.check_for_new_docs.start()

    def cog_unload(self):
        self.check_for_new_docs.cancel()

    @tasks.loop(seconds=60.0 * 10.0)
    async def check_for_new_docs(self):
        await self.post_new_docs()

    @check_for_new_docs.before_loop
    async def before_checking_for_new_docs(self):
        await self.bot.wait_until_ready()

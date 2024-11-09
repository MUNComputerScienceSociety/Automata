import asyncio
from datetime import datetime
from typing import Any

import discord
import httpx
from discord.ext import tasks

from automata.config import config
from automata.mongo import mongo
from automata.utils import Plugin

EXECUTIVE_DOCS_BASE_URI = "https://www.cs.mun.ca/~csclub/executive-documents"
EXECUTIVE_DOCS_JSON_URI = f"{EXECUTIVE_DOCS_BASE_URI}/docs.json"
CS_LOGO_COLOR_SQUARE_TRANSPARENT = (
    "https://www.cs.mun.ca/~csclub/assets/logos/color-square-trans.png"
)
DOC_TYPE_TO_COLOUR = {
    "Minutes": discord.Colour.lighter_gray(),
    "Agendas": discord.Colour.dark_gray(),
}

type Doc = Any


class ExecutiveDocs(Plugin):
    """Posts new executive documents"""

    def doc_embed(self, doc: Doc) -> discord.Embed:
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

    async def post_new_doc(self, doc: Doc):
        embed = self.doc_embed(doc)

        guild = self.bot.get_guild(config.primary_guild)
        if guild is None:
            await self.cog_unload()
            return

        channel = guild.get_channel(config.executive_docs_channel)
        if channel is None:
            await self.cog_unload()
            return

        await channel.send(embed=embed)
        await self.posted_documents.insert_one(doc)

    async def fetch_docs_json(self) -> list[Doc]:
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

    async def cog_load(self):
        self.posted_documents = mongo.automata.executivedocs_posted_documents
        self.check_for_new_docs.start()

    async def cog_unload(self):
        self.check_for_new_docs.cancel()

    @tasks.loop(seconds=60.0 * 10.0)
    async def check_for_new_docs(self):
        await self.post_new_docs()

    @check_for_new_docs.before_loop
    async def before_checking_for_new_docs(self):
        await self.bot.wait_until_ready()

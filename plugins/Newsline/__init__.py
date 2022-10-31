import asyncio
import re
from urllib.parse import urlencode
from datetime import datetime

import httpx
import discord
from discord.ext import commands, tasks

from Plugin import AutomataPlugin
from Globals import (
    mongo_client,
    PRIMARY_GUILD,
    NEWSLINE_CHANNEL,
)

NEWSLINE_API_BASE_URI = "https://jackharrhy.dev/newsline"
NEWSLINE_API_POSTS = f"{NEWSLINE_API_BASE_URI}/posts"
MUN_LOGO = "https://www.cs.mun.ca/~csclub/assets/logos/others/mun-color.png"

CHECKING_INTERVAL = 60 * 5


class Newsline(AutomataPlugin):
    """Posts from http://cliffy.ucs.mun.ca/archives/newsline.html, using https://github.com/jackharrhy/newsline-api"""

    def __init__(self, manifest, bot: commands.Bot):
        super().__init__(manifest, bot)

        self.posted_posts = mongo_client.automata.newsline_posts
        self.posted_posts.drop()
        self.posting = False

    @commands.Cog.listener()
    async def on_ready(self):
        await self.check_for_new_posts.start()

    def post_embed(self, post, post_detail):
        desc = post_detail["text"]

        if len(desc) > 2048:
            desc = desc[0 : 2048 - len("...")] + "..."

        url = post["htmlurl"]
        if url is None:
            url = post["url"]

        embed = discord.Embed(
            title=f"{post_detail['subject']} - {post['date'].strftime('%r')}",
            description=desc,
            colour=discord.Colour.dark_red(),
            url=url,
            timestamp=post["date"],
        )
        embed.set_footer(text="Newsline", icon_url=MUN_LOGO)
        return embed

    async def post_new_post(self, post, post_details):
        embed = self.post_embed(post, post_details)
        await self.bot.get_guild(PRIMARY_GUILD).get_channel(NEWSLINE_CHANNEL).send(
            embed=embed
        )
        await self.posted_posts.insert_one({"id": post["id"]})

    async def make_request_to_post_detail(self, post_id):
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{NEWSLINE_API_BASE_URI}/posts/{post_id}/detail")
        post_detail = resp.json()
        post_detail["text"] = re.sub(r"(\n\s*)+\n+", "\n\n", post_detail["text"])
        return post_detail

    async def make_request_to_posts(self, page):
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{NEWSLINE_API_POSTS}?{urlencode({'page': page})}")
        return resp.json()

    async def fetch_posts(self):
        page = 0

        while len(posts := await self.make_request_to_posts(page)) != 0:
            for post in posts:
                post["date"] = post["date"].replace("Z", "-03:30")
                post["date"] = datetime.fromisoformat(post["date"])
                yield post

            await asyncio.sleep(0.5)
            page += 1

    async def post_new_posts(self):
        if self.posting:
            return

        self.posting = True
        posts_to_post = []

        async for post in self.fetch_posts():
            potential_post = await self.posted_posts.find_one({"id": post["id"]})

            if potential_post is None:
                posts_to_post.append(post)
            else:
                break

        posts_to_post.reverse()

        for post in posts_to_post:
            post_detail = self.make_request_to_post_detail(post["id"])
            await self.post_new_post(post, post_detail)
            await asyncio.sleep(5)

        self.posting = False

    def cog_unload(self):
        self.check_for_new_posts.cancel()

    @tasks.loop(seconds=CHECKING_INTERVAL)
    async def check_for_new_posts(self):
        await self.post_new_posts()

    @check_for_new_posts.before_loop
    async def before_checking_for_new_posts(self):
        await self.bot.wait_until_ready()

import asyncio
import pathlib
from humps import camelize

from datetime import datetime

import requests
import discord
from discord.ext import commands, tasks

from Plugin import AutomataPlugin
from Globals import (
    mongo_client,
    PRIMARY_GUILD,
    CTSNL_JOBS_CHANNEL
)

CTSNL_BASE_URI = "https://ctsnl.ca"
CTSNL_DATA_URI = f"{CTSNL_BASE_URI}/data.json"
CTSNL_LOGO_SQUARE = "https://www.cs.mun.ca/~csclub/assets/logos/others/cts-square.jpg"

"""
{
  "meta": {
    "lastUpdate": "Nov 08, 2020"
  },
  "data": {
    "jobs": [
      {
        "company": "lemur",
        "jobs": [
          {
            "post_date": "2019-06-13",
            "jobs": [
              {
                "title": "Embedded Systems Engineer / Developer",
                "link": "https://www.bluedriver.com/about-us/careers"
              }
            ]
          },
          {
            "post_date": "2019-03-07",
            "jobs": [
              {
                "title": "Software Developer / Engineer",
                "link": "https://www.bluedriver.com/about-us/careers"
              }
            ]
          }
        ]
      }
    ],
    "companies": {
      "acenet": {
        "name": "ACENET",
        "url": "https://www.ace-net.ca/"
      }
    },
    "groups": {
      "acenet": {
        "name": "ACENET",
        "url": "https://www.ace-net.ca/"
      }
    }
  }
}
"""

def to_camel(string):
    return camelize(string)

class Meta(BaseModel):
    last_update: str

class Root(BaseModel):
    meta: Meta
    id: int
    name = 'John Doe'
    signup_ts: Optional[datetime] = None
    friends: List[int] = []


class CTSNL(AutomataPlugin):
    """Interops with the data from the CTSNL website"""

    def job_embed(self, job):
        embed = discord.Embed(
            title=f"Meeting {doc['type']} | {doc['time'].strftime('%A, %B %e, %Y')}",
            description=doc["url"],
            url=doc["url"],
            colour=DOC_TYPE_TO_COLOUR.get(doc["type"], discord.Colour.dark_blue()),
            timestamp=doc["time"],
        )
        embed.set_footer(
            text="CTSNL", icon_url=CTSNL_LOGO_SQUARE
        )
        return embed

    async def post_new_job(self, job):
        embed = self.job_embed(doc)
        await self.bot.get_guild(PRIMARY_GUILD).get_channel(
            CTSNL_JOBS_CHANNEL
        ).send(embed=embed)
        # await self.posted_documents.insert_one(doc)

    def fetch_data_json(self):
        return requests.get(CTSNL_DATA_URI).json()

    async def post_new_jobs(self):
        data_json = self.fetch_data_json()

        print(data_json)

        return

        for doc in docs_json:
            doc["time"] = datetime.strptime(doc["time"], "%Y-%m-%d %H:%M:%S")
            doc["url"] = f"{EXECUTIVE_DOCS_BASE_URI}/{doc['path']}"

        docs_json.sort(key=lambda doc: doc["time"])

        for doc in docs_json:
            potential_doc = await self.posted_documents.find_one({"path": doc["path"]})

            if potential_doc is None:
                await self.post_new_doc(doc)
                await asyncio.sleep(5)

    def __init__(self, manifest, bot: commands.Bot):
        super().__init__(manifest, bot)

        self.posted_jobs = mongo_client.automata.ctsnl_posted_jobs

        loop = asyncio.get_event_loop()
        self.check_for_new_jobs.start()

    def cog_unload(self):
        self.check_for_new_jobs.cancel()

    @tasks.loop(seconds=60 * 10)
    async def check_for_new_jobs(self):
        await self.post_new_jobs()

    @check_for_new_jobs.before_loop
    async def before_checking_for_new_jobs(self):
        await self.bot.wait_until_ready()

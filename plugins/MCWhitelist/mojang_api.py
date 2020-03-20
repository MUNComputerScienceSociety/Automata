import asyncio
import json
from base64 import b64decode
from datetime import datetime

import requests

from Globals import mongo_client

MOJANG_API_BASE = "https://api.mojang.com"
MOJANG_SESSIONSERVER_BASE = "https://sessionserver.mojang.com"


class MojangAPI:
    """https://wiki.vg/Mojang_API"""

    username_base = f"{MOJANG_API_BASE}/users/profiles/minecraft"
    profile_base = f"{MOJANG_SESSIONSERVER_BASE}/session/minecraft/profile"

    def __init__(self):
        self.profile_cache = mongo_client.automata.mojangapi_profile_cache

        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.ensure_collection_expiry())

    async def ensure_collection_expiry(self):
        await self.profile_cache.create_index(
            "datetime", expireAfterSeconds=900  # 15 minutes
        )

    def info_from_username(self, username):
        try:
            return requests.get(f"{MojangAPI.username_base}/{username}").json()
        except:
            return None

    async def profile_from_uuid(self, uuid):
        cached = await self.profile_cache.find_one({"uuid": uuid})

        if cached:
            return cached["data"]

        try:
            resp = requests.get(f"{MojangAPI.profile_base}/{uuid}").json()
        except:
            resp = None

        await self.profile_cache.insert_one(
            {"datetime": datetime.utcnow(), "uuid": uuid, "data": resp}
        )
        return resp

    def skin_url_from_profile(self, profile):
        if (not profile) and (not profile["properties"]):
            return None

        textures_encoded = next(
            x for x in profile["properties"] if x["name"] == "textures"
        )

        if not textures_encoded:
            return None

        textures = json.loads(b64decode(textures_encoded["value"]))

        if (not textures["textures"]) and (not textures["SKIN"]):
            return None

        return textures["textures"]["SKIN"]["url"]

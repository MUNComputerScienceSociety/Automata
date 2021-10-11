import asyncio
import json
from base64 import b64decode
from datetime import datetime

import httpx

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

    async def info_from_username(self, username):
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{MojangAPI.username_base}/{username}")

        if resp.status_code == 200:
            return resp.json()

    async def profile_from_uuid(self, uuid):
        cached = await self.profile_cache.find_one({"uuid": uuid})

        if cached is not None:
            return cached["data"]

        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{MojangAPI.profile_base}/{uuid}")

        if resp.status_code == 200:
            data = resp.json()
        else:
            data = None

        await self.profile_cache.insert_one(
            {"datetime": datetime.utcnow(), "uuid": uuid, "data": data}
        )
        return data

    def skin_url_from_profile(self, profile):
        if (profile is None) and (profile["properties"] is None):
            return None

        textures_encoded = next(
            x for x in profile["properties"] if x["name"] == "textures"
        )

        if textures_encoded is None:
            return None

        textures = json.loads(b64decode(textures_encoded["value"]))

        if (textures["textures"] is None) or (textures["textures"]["SKIN"] is None):
            return None

        return textures["textures"]["SKIN"]["url"]

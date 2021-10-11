import httpx

from Globals import WHITELIST_HTTP_API_BEARER_TOKEN

WHITELIST_HTTP_API_BASE = "http://craft.muncompsci.ca:7500"
HEADERS = {"authorization": f"WHA {WHITELIST_HTTP_API_BEARER_TOKEN}"}


class WhitelistHttpApi:
    async def whitelist(self):
        async with httpx.AsyncClient() as client:
            resp = await client.get(WHITELIST_HTTP_API_BASE, headers=HEADERS)

        return resp.json()

    async def add(self, username):
        data = {"name": username}

        async with httpx.AsyncClient() as client:
            resp = await client.post(
                WHITELIST_HTTP_API_BASE, json=data, headers=HEADERS
            )
        resp.raise_for_status()

    async def remove(self, username):
        data = {"name": username}

        async with httpx.AsyncClient() as client:
            resp = await client.delete(
                WHITELIST_HTTP_API_BASE, json=data, headers=HEADERS
            )
        resp.raise_for_status()

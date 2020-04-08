import json

import requests

from Globals import mongo_client, WHITELIST_HTTP_API_BEARER_TOKEN

WHITELIST_HTTP_API_BASE = "http://craft.muncompsci.ca:7500"
HEADERS = {"authorization": f"WHA {WHITELIST_HTTP_API_BEARER_TOKEN}"}


class WhitelistHttpApi:
    def whitelist(self):
        return requests.get(WHITELIST_HTTP_API_BASE, headers=HEADERS).json()

    def add(self, username):
        data = {"name": username}
        requests.post(
            WHITELIST_HTTP_API_BASE, json=data, headers=HEADERS
        ).raise_for_status()

    def remove(self, username):
        data = {"name": username}
        requests.delete(
            WHITELIST_HTTP_API_BASE, json=data, headers=HEADERS
        ).raise_for_status()

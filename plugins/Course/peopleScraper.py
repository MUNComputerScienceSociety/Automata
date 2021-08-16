import asyncio
import requests
from bs4 import BeautifulSoup
import json
from Globals import mongo_client
from datetime import datetime

# The URL for MUNs listing of CS faculty
url = "https://www.mun.ca/appinclude/bedrock/public/api/v1/ua/people.php?type=advanced&nopage=1&department=Computer%20Science"


class PeopleScraper:
    def __init__(self, cache_lifetime):
        # Get a reference to the cache
        self.people_cache = mongo_client.automata.people_scraper_cache
        # Set up the cache data lifetimes
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.ensure_collection_expiry(cache_lifetime))

    # Set up the cache data lifetimes
    async def ensure_collection_expiry(self, lifetime):
        await self.people_cache.create_index("datetime", expireAfterSeconds=lifetime)

    async def get_faculty_staff(self):
        # Try to get the staff data from the cache
        cached = await self.people_cache.find_one()
        # If any data was found return it
        if cached is not None:
            return cached["data"]

        # Convert the response to a dict and store the info as a list of dicts
        faculty_staff = eval(requests.get(url).text)["results"]

        # Add the faculty staff data to the cache and return it
        self.people_cache.insert_one(
            {"datetime": datetime.utcnow(), "data": faculty_staff}
        )
        return faculty_staff

    async def get_prof_info_from_name(self, prof_name):

        # Get the info of all of the staff in the faculty
        faculty_staff = await self.get_faculty_staff()

        # Split the parameter name into individual words
        separated_name = prof_name.lower().split(" ")

        # Loop through the staff
        for i in range(len(faculty_staff)):
            # Assume they are the prof we're looking for
            correct_prof = True
            for j in range(len(separated_name)):
                # If any of the parts of the parameter name aren't present in the profs "displayname" they're not it
                if separated_name[j] not in faculty_staff[i]["displayname"].lower():
                    correct_prof = False
                    break
            # Otherwise return the dict containing the profs info
            if correct_prof:
                return faculty_staff[i]

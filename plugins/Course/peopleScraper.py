import asyncio
import httpx
from bs4 import BeautifulSoup
import json
from datetime import datetime

# The URL for MUNs listing of CS faculty
url = "https://www.mun.ca/appinclude/bedrock/public/api/v1/ua/people.php?type=advanced&nopage=1&department=Computer%20Science"


class PeopleScraper:
    def __init__(self, cache_lifetime, cache):
        self.people_cache = cache

    # Sets up the cache; deletes whats in it and ensures they expire within the given lifetime
    async def setup_cache(self, lifetime):
        await self.people_cache.delete_many({})
        await self.people_cache.create_index("datetime", expireAfterSeconds=lifetime)

    async def get_faculty_staff(self):
        # Try to get the staff data from the cache
        cached = await self.people_cache.find_one()
        # If any data was found return it
        if cached is not None:
            return cached["data"]

        # Convert the response to a dict and store the info as a list of dicts
        async with httpx.AsyncClient() as client:
            resp = await client.get(url)
            faculty_staff = eval(resp.text)["results"]

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

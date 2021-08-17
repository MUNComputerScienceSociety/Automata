import asyncio
from datetime import datetime
from bs4 import BeautifulSoup
from urllib.request import urlopen
from Globals import mongo_client

# The URL for MUNs listing of CS courses
calendar_url = "https://www.mun.ca/regoff/calendar/sectionNo=SCI-1023"


class CalendarScraper:
    def __init__(self, cache_lifetime):
        # Get a reference to the cache
        self.calendar_cache = mongo_client.automata.calendar_scraper_cache

        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.setup_cache(cache_lifetime))

    # Sets up the cache; deletes whats in it and ensures they expire within the given lifetime
    async def setup_cache(self, lifetime):
        await self.calendar_cache.delete_many()
        await self.calendar_cache.create_index("datetime", expireAfterSeconds=lifetime)

    async def get_calendar_HTML(self):
        # Try to get the HTML data from the cache
        cached = await self.calendar_cache.find_one()

        # If any data was found return it
        if cached is not None:
            return cached["data"]

        # Otherwise, get the data through web scraping
        client = urlopen(calendar_url)
        page_html = client.read()
        client.close()

        # Add the HTML data to the cache and return it
        self.calendar_cache.insert_one(
            {"datetime": datetime.utcnow(), "data": page_html}
        )
        return page_html

    async def get_name_and_info_from_ID(self, course_ID):
        # Get the HTML from the url
        page_html = await self.get_calendar_HTML()

        # Make soup and get all of the course divs
        soup = BeautifulSoup(page_html, "html.parser")
        course_divs = soup.find_all("div", {"class": "course"})

        # Try to find a course with the correct ID
        course_index = -1
        for i in range(len(course_divs)):
            if (
                course_divs[i].find("p", {"class": "courseNumber"}).text.strip()
                == course_ID
            ):
                course_index = i
                break
        # If it's not there return Nones
        if course_index == -1:
            return None, None

        # Otherwise return the courses name and description
        course = course_divs[course_index]
        course_name = course.find("p", {"class": "courseTitle"}).text.strip()
        course_desc = course.div.p.text.strip()
        return course_name, f"{course_name} {course_desc}"

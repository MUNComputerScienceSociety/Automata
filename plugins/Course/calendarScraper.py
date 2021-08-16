import asyncio
from datetime import datetime
from bs4 import BeautifulSoup
from urllib.request import urlopen
from Globals import mongo_client

# The URL for MUNs listing of CS courses
calendar_url = "https://www.mun.ca/regoff/calendar/sectionNo=SCI-1023"


class CalendarScraper:

    def __init__(self, cache_lifetime):
        self.calendar_cache = mongo_client.automata.calendar_scraper_cache

        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.ensure_collection_expiry(cache_lifetime))


    async def ensure_collection_expiry(self, lifetime):
        await self.calendar_cache.create_index(
            "datetime", expireAfterSeconds=lifetime
        )


    async def get_calendar_HTML(self):
        cached = await self.calendar_cache.find_one()

        if cached is not None:
            print("Got calendar data from cache")
            return cached["data"]
        
        client = urlopen(calendar_url)
        page_html = client.read()
        client.close()
        print("Scraping for calendar data")

        self.calendar_cache.insert_one({
            "datetime": datetime.utcnow(), "data": page_html
        })
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
            if course_divs[i].find("p", {"class": "courseNumber"}).text.strip() == course_ID:
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

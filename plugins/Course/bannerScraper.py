import requests
from bs4 import BeautifulSoup
import asyncio
from datetime import datetime
from Globals import mongo_client

# The stuff between these lines was taken from https://github.com/jackharrhy/muntrunk/blob/master/muntrunk/scrape.py
# Full credit to Jack for this stuff
# --------------------------------------------------------------------------------------------------
headers = {
    "User-Agent": "github.com/MUNComputerScienceSociety/Automata",
    "Accept": "text/html",
    "Accept-Language": "en-US,en;q=0.5",
    "Content-Type": "application/x-www-form-urlencoded",
    "Origin": "https://www5.mun.ca",
    "Connection": "keep-alive",
    "Referer": "https://www5.mun.ca/admit/hwswsltb.P_CourseSearch",
    "Upgrade-Insecure-Requests": "1",
}
# --------------------------------------------------------------------------------------------------


class BannerScraper:
    def __init__(self, cache_lifetime):
        # Get a reference to the cache
        self.banner_cache = mongo_client.automata.banner_scraper_cache

        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.setup_cache(cache_lifetime))

    # Sets up the cache; deletes whats in it and ensures they expire within the given lifetime
    async def setup_cache(self, lifetime):
        await self.banner_cache.delete_many({})
        await self.banner_cache.create_index("datetime", expireAfterSeconds=lifetime)

    # --------------------------------------------------------------------------------------------------

    def actually_fetch_banner(self, year, term, level):
        data = {
            "p_term": f"{year}0{term}",
            "p_levl": f"0{level}*00",
            "campus": "%",
            "faculty": "Computer Science",
            "prof": "%",
            "crn": "%",
        }

        response = requests.post(
            "https://www5.mun.ca/admit/hwswsltb.P_CourseResults",
            headers=headers,
            data=data,
        )

        soup = BeautifulSoup(response.text, "html.parser")

        h2 = soup.find_all("h2")
        if len(h2) >= 2 and h2[1].text == "No matches were found for your search":
            return None

        return soup

    # --------------------------------------------------------------------------------------------------

    async def get_listings_from_ID(self, course_ID):
        output = []

        # If it's before May in a given year, assume it's term 2 of the previous year
        current_date = datetime.now()
        isTerm2 = current_date.month < 5
        year = (current_date.year - 1) if isTerm2 else current_date.year
        term = 2 if isTerm2 else 1

        # Try to get the listings from the cache
        cached = await self.banner_cache.find_one({"year": year, "term": term})

        search_HTML = None

        # If any were found store them in a variable
        if cached is not None:
            search_HTML = cached["data"]
        else:
            # Otherwise get them through webscraping and add them to the cache
            search_HTML = self.actually_fetch_banner(year, term, 1).text
            await self.banner_cache.insert_one(
                {
                    "datetime": datetime.utcnow(),
                    "year": year,
                    "term": term,
                    "data": search_HTML,
                }
            )

        # If there is no HTML, panic
        if not search_HTML:
            return "Something went wrong..."

        # Split the HTML by campuses
        courses_by_campus = search_HTML.split("Campus: ")
        # Get rid of the first part because it's nonsense
        courses_by_campus.pop(0)

        # For each campus
        for i in range(len(courses_by_campus)):
            # Split its contents into individual courses
            courses = courses_by_campus[i].split("\nCOMP")
            # Get the name of the campus
            campus_name = courses.pop(0).split("\n", 1)[0].strip()
            # For each course, if it has the right ID
            for j in range(len(courses)):
                if courses[j][1:5] == course_ID:
                    # Append it and its campus name to the output
                    output.append([(f"COMP{courses[j]}").split("\n"), campus_name])

        return output

    async def get_profs_from_course(self, course_ID):

        # Get the listing
        listing = await self.get_listings_from_ID(course_ID)

        profs_by_campuses = {}

        # For each campus in the listing
        for i in range(len(listing)):
            # Add an empty list to the dict with the campus name as the key
            campus_name = listing[i][1]
            profs_by_campuses[campus_name] = []

            # For each line in the listing for the campus
            for j in range(len(listing[i][0])):
                # If the line is empty you're at the end
                if len(listing[i][0][j]) == 0:
                    listing[i][0] = listing[i][0][0:j]
                    break

                # If the line has a "section number" in the space specified, look for a prof name
                if listing[i][0][j][38] != " ":
                    # If the spot where the name should be is not empty
                    prof_name = listing[i][0][j][148:].strip()
                    if prof_name:
                        # Check to see if it is a new prof campus combo
                        is_new = True
                        for k in range(len(profs_by_campuses[campus_name])):
                            if profs_by_campuses[campus_name][k] == prof_name:
                                is_new = False

                        # If it is, add it to the list in the dict for that particular campus
                        if is_new:
                            profs_by_campuses[campus_name].append(prof_name)

        return profs_by_campuses

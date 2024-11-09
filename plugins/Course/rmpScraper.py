from bs4 import BeautifulSoup
from urllib.request import urlopen
from datetime import datetime
import asyncio

# These are the parts that go into a RMP search for a MUN prof (minus the name)
url_parts = [
    "https://www.ratemyprofessors.com/search/teachers?query=",
    "&sid=U2Nob29sLTE0NDE=",
]


class RMPScraper:
    def __init__(self, cache_lifetime, cache):
        self.rmp_cache = cache

    # Set up the cache data lifetimes
    async def ensure_collection_expiry(self, lifetime):
        await self.rmp_cache.create_index("datetime", expireAfterSeconds=lifetime)

    # Get the completed URL for the RMP search
    def get_rmp_url(self, separated_prof_name):
        # Append every word from the name together with "%20" in between them
        name_with_spaces = "%20".join(separated_prof_name)

        return f"{url_parts[0]}{name_with_spaces}{url_parts[1]}"

    # Get the soup from a URL
    def get_soup_from_url(self, url):
        client = urlopen(url)
        page_html = client.read()
        client.close()
        return BeautifulSoup(page_html, "html.parser")

    async def get_rating_from_prof_name(self, prof_name):
        prof_name = prof_name.lower()

        # Try to get the profs data from the cache
        cached = await self.rmp_cache.find_one({"prof_name": prof_name})

        # If it's found return the profs "rmp string" and name from rmp
        if cached is not None:
            return cached["rmp_string"], cached["prof_rmp_name"]

        # Get the URL for the search
        separated_name = prof_name.split(" ")
        url = self.get_rmp_url(separated_name)
        # Soup
        soup = self.get_soup_from_url(url)
        # Get all divs for profs
        profs = soup.find_all(
            "a", {"class": "TeacherCard__StyledTeacherCard-syjs0d-0 dLJIlx"}
        )

        # If there are no prof divs found we try again, but leave out the first name
        if not profs:
            url = self.get_rmp_url(separated_name[1:])
            soup = self.get_soup_from_url(url)
            profs = soup.find_all(
                "a", {"class": "TeacherCard__StyledTeacherCard-syjs0d-0 dLJIlx"}
            )
            # Two fails means no profile
            if not profs:
                return None, None

        probably_the_right_prof = None
        # If more than one prof is found from the search find the first one in the CS department
        if len(profs) > 1:
            found_cs_prof = False
            for i in range(len(profs)):
                if (
                    profs[i]
                    .find(
                        "div", {"class": "CardSchool__Department-sc-19lmz2k-0 haUIRO"}
                    )
                    .text
                    == "Computer Science"
                ):
                    probably_the_right_prof = profs[i]
                    found_cs_prof = True
                    break
            # If none of the ooptions are in the CS department there is no profile
            if not found_cs_prof:
                return None, None
        else:
            # Only one prof means that ones probably the right one
            probably_the_right_prof = profs[0]

        # Format and return the output string
        score_box = probably_the_right_prof.div.div.div.find_all("div")[1:3]
        rmp_string = f"{score_box[0].text} with {score_box[1].text}"
        prof_rmp_name = probably_the_right_prof.div.find(
            "div", {"class": "TeacherCard__CardInfo-syjs0d-1 fkdYMc"}
        ).div.text

        # Add the data to the cache and return it
        await self.rmp_cache.insert_one(
            {
                "datetime": datetime.utcnow(),
                "prof_name": prof_name,
                "rmp_string": rmp_string,
                "prof_rmp_name": prof_rmp_name,
            }
        )
        return rmp_string, prof_rmp_name

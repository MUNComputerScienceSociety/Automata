from asyncio.windows_events import NULL
import requests
from bs4 import BeautifulSoup
import datetime

# The stuff between these lines was taken from https://github.com/jackharrhy/muntrunk/blob/master/muntrunk/scrape.py
# Full credit to Jack for this stuff
# --------------------------------------------------------------------------------------------------
headers = {
    "User-Agent": "github.com/cmoyates/MUN-Info-Discord-Bot",
    "Accept": "text/html",
    "Accept-Language": "en-US,en;q=0.5",
    "Content-Type": "application/x-www-form-urlencoded",
    "Origin": "https://www5.mun.ca",
    "Connection": "keep-alive",
    "Referer": "https://www5.mun.ca/admit/hwswsltb.P_CourseSearch",
    "Upgrade-Insecure-Requests": "1",
}


def actually_fetch_banner(year, term, level):
    data = {
        "p_term": f"{year}0{term}",
        "p_levl": f"0{level}*00",
        "campus": "%",
        "faculty": "Computer Science",
        "prof": "%",
        "crn": "%",
    }

    response = requests.post(
        "https://www5.mun.ca/admit/hwswsltb.P_CourseResults", headers=headers, data=data
    )

    soup = BeautifulSoup(response.text, "html.parser")

    h2 = soup.find_all("h2")
    if len(h2) >= 2 and h2[1].text == "No matches were found for your search":
        return None

    return soup


# --------------------------------------------------------------------------------------------------


def getListingsFromID(courseID):
    output = []

    # If it's before May in a given year, assume it's term 2 of the previous year
    currentDate = datetime.datetime.now()
    isTerm2 = currentDate.month < 5
    year = (currentDate.year - 1) if isTerm2 else currentDate.year
    term = 2 if isTerm2 else 1

    # Get the HTML
    searchHTML = actually_fetch_banner(year, term, 1)
    # If there is no HTML, panic
    if not searchHTML:
        return "Something went wrong..."

    # Split the HTML by campuses
    coursesByCampus = searchHTML.text.split("Campus: ")
    # Get rid of the first part because it's nonsense
    coursesByCampus.pop(0)

    # For each campus
    for i in range(len(coursesByCampus)):
        # Split its contents into individual courses
        courses = coursesByCampus[i].split("\nCOMP")
        # Get the name of the campus
        campusName = courses.pop(0).split("\n", 1)[0].strip()
        # For each course, if it has the right ID
        for j in range(len(courses)):
            if courses[j][1:5] == courseID:
                # Append it and its campus name to the output
                output.append([("COMP" + courses[j]).split("\n"), campusName])

    return output


def getProfsFromCourse(courseID):
    profsByCampuses = {}

    # Get the listing
    listing = getListingsFromID(courseID)

    # For each campus in the listing
    for i in range(len(listing)):
        # Add an empty list to the dict with the campus name as the key
        campusName = listing[i][1]
        profsByCampuses[campusName] = []

        # For each line in the listing for the campus
        for j in range(len(listing[i][0])):
            # If the line is empty you're at the end
            if len(listing[i][0][j]) == 0:
                listing[i][0] = listing[i][0][0:j]
                break

            # If the line has a "section number" in the space specified, look for a prof name
            if listing[i][0][j][38] != " ":
                # If the spot where the name should be is not empty
                profName = listing[i][0][j][148:].strip()
                if profName:
                    # Check to see if it is a new prof campus combo
                    isNew = True
                    for k in range(len(profsByCampuses[campusName])):
                        if profsByCampuses[campusName][k] == profName:
                            isNew = False

                    # If it is, add it to the list in the dict for that particular campus
                    if isNew:
                        profsByCampuses[campusName].append(profName)

    return profsByCampuses

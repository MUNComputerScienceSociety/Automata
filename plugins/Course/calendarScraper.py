from bs4 import BeautifulSoup
from urllib.request import urlopen as uReq

# The URL for MUNs listing of CS courses
calendar_url = "https://www.mun.ca/regoff/calendar/sectionNo=SCI-1023"


def getNameAndInfoFromID(courseID):
    # Get the HTML from the url
    uClient = uReq(calendar_url)
    page_html = uClient.read()
    uClient.close()

    # Make soup and get all of the course divs
    soup = BeautifulSoup(page_html, "html.parser")
    courseDivs = soup.find_all("div", {"class": "course"})

    # Try to find a course with the correct ID
    courseIndex = -1
    for i in range(len(courseDivs)):
        if courseDivs[i].find("p", {"class": "courseNumber"}).text.strip() == courseID:
            courseIndex = i
            break
    # If it's not there return Nones
    if courseIndex == -1:
        return None, None

    # Otherwise return the courses name and description
    course = courseDivs[courseIndex]
    courseName = course.find("p", {"class": "courseTitle"}).text.strip()
    courseDesc = course.div.p.text.strip()
    return courseName, courseName + " " + courseDesc

from bs4 import BeautifulSoup
from urllib.request import urlopen

# The URL for MUNs listing of CS courses
calendar_url = "https://www.mun.ca/regoff/calendar/sectionNo=SCI-1023"


def get_name_and_info_from_ID(course_ID):
    # Get the HTML from the url
    client = urlopen(calendar_url)
    page_html = client.read()
    client.close()

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

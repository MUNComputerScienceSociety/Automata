import requests
from bs4 import BeautifulSoup
import json

# The URL for MUNs listing of CS faculty
url = "https://www.mun.ca/appinclude/bedrock/public/api/v1/ua/people.php?type=advanced&nopage=1&department=Computer%20Science"
# Convert the response to a dict and store the info as a list of dicts
faculty_staff = eval(requests.get(url).text)["results"]


def get_prof_info_from_name(prof_name):
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

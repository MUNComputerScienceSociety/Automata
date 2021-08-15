import requests
from bs4 import BeautifulSoup
import json

# The URL for MUNs listing of CS faculty
url = "https://www.mun.ca/appinclude/bedrock/public/api/v1/ua/people.php?type=advanced&nopage=1&department=Computer%20Science"
# Convert the response to a dict and store the info as a list of dicts
facultyStaff = eval(requests.get(url).text)["results"]


def getProfInfoFromName(profName):
    # Split the parameter name into individual words
    separatedName = profName.lower().split(" ")

    # Loop through the staff
    for i in range(len(facultyStaff)):
        # Assume they are the prof we're looking for
        correctProf = True
        for j in range(len(separatedName)):
            # If any of the parts of the parameter name aren't present in the profs "displayname" they're not it
            if separatedName[j] not in facultyStaff[i]["displayname"].lower():
                correctProf = False
                break
        # Otherwise return the dict containing the profs info
        if correctProf:
            return facultyStaff[i]

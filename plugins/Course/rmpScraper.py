from bs4 import BeautifulSoup
from urllib.request import urlopen as uReq

# These are the parts that go into a RMP search for a MUN prof (minus the name)
urlParts = [
    "https://www.ratemyprofessors.com/search/teachers?query=",
    "&sid=U2Nob29sLTE0NDE=",
]

# Get the completed URL for the RMP search
def getRMPURL(separatedProfName):

    finalUrl = urlParts[0]

    # Append every word from the name to the URL with "%20" in between them
    finalUrl += "%20".join(separatedProfName)

    finalUrl += urlParts[1]
    return finalUrl


# Get the soup from a URL
def getSoupFromURL(url):
    uClient = uReq(url)
    page_html = uClient.read()
    uClient.close()
    return BeautifulSoup(page_html, "html.parser")


def getRatingFromProfName(profName):
    # Get the URL for the search
    profName = profName.lower()
    separatedName = profName.split(" ")
    finalUrl = getRMPURL(separatedName)
    # Soup
    soup = getSoupFromURL(finalUrl)
    # Get all divs for profs
    profs = soup.find_all(
        "a", {"class": "TeacherCard__StyledTeacherCard-syjs0d-0 dLJIlx"}
    )

    # If there are no prof divs found we try again, but leave out the first name
    if not profs:
        finalUrl = getRMPURL(separatedName[1:])
        soup = getSoupFromURL(finalUrl)
        profs = soup.find_all(
            "a", {"class": "TeacherCard__StyledTeacherCard-syjs0d-0 dLJIlx"}
        )
        # Two fails means no profile
        if not profs:
            return None, None

    probablyTheRightProf = None
    # If more than one prof is found from the search find the first one in the CS department
    if len(profs) > 1:
        foundCSProf = False
        for i in range(len(profs)):
            if (
                profs[i]
                .find("div", {"class": "CardSchool__Department-sc-19lmz2k-0 haUIRO"})
                .text
                == "Computer Science"
            ):
                probablyTheRightProf = profs[i]
                foundCSProf = True
                break
        # If none of the ooptions are in the CS department there is no profile
        if not foundCSProf:
            return None, None
    else:
        # Only one prof means that ones probably the right one
        probablyTheRightProf = profs[0]

    # Format and return the output
    scoreBox = probablyTheRightProf.div.div.div.find_all("div")[1:3]
    output = scoreBox[0].text + " with " + scoreBox[1].text
    profRMPName = probablyTheRightProf.div.find(
        "div", {"class": "TeacherCard__CardInfo-syjs0d-1 fkdYMc"}
    ).div.text
    return output, profRMPName

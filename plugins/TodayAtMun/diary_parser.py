from bs4 import BeautifulSoup
import requests
import os
from os import path
import json

class diary_parser:
    def __init__(self):
        if path.exists("diary.json"):
            os.remove("diary.json")
            print("File Removed")
        r = requests.get(
            "https://www.mun.ca/regoff/calendar/sectionNo=GENINFO-0086", verify=False
        ).text

        soup = BeautifulSoup(r, "html.parser")

        with open("diary.json", "w") as file:

            data = soup.find_all("td", attrs={"align": "left"})
            data2 = soup.find_all("td", attrs={"align": "justify"})
            day_contents = {}
            diary = {}

            for i, j in zip(data, data2):
                try:
                    diary[i.find("p").get_text().strip("\n\t")] = (
                        j.get_text().replace("\n", "").replace("\t", "")
                    )
                except AttributeError:
                    continue

            diary_file = file.write(json.dumps(diary))

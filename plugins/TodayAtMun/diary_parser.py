from bs4 import BeautifulSoup
import requests
import os
from os import path
import json
from pathlib import Path


class diary_parser:
    def __init__(self):
        BASE_DIR = Path(__file__).parent
        file_name = BASE_DIR / "diary.json"
        try:
            Path.unlink(file_name)
        except FileNotFoundError:
            Path.touch(file_name)
        r = requests.get(
            "https://www.mun.ca/regoff/calendar/sectionNo=GENINFO-0086", verify=False
        ).text
        soup = BeautifulSoup(r, "html.parser")

        with open(file_name, "w") as file:

            data = soup.find_all("td", attrs={"align": "left"})
            data2 = soup.find_all("td", attrs={"align": "justify"})
            diary = {}

            for i, j in zip(data, data2):
                try:
                    diary[i.find("p").get_text().strip("\n\t")] = (
                        j.get_text()
                        .replace("\n", "")
                        .replace("\t", "")
                        .replace("'", '"')
                    )
                except AttributeError:
                    continue

            diary_file = file.write(json.dumps(diary))

import json
import os
from os import path
from pathlib import Path

import requests
from bs4 import BeautifulSoup


class DiaryParser:
    def __init__(self):
        self.diary = {}

        r = requests.get(
            "https://www.mun.ca/regoff/calendar/sectionNo=GENINFO-0086", verify=False
        ).text
        soup = BeautifulSoup(r, "html.parser")
        left_aligned_data = soup.find_all("td", attrs={"align": "left"})
        right_aligned_data = soup.find_all("td", attrs={"align": "justify"})

        for i, j in zip(left_aligned_data, right_aligned_data):
            try:
                self.diary[i.find("p").get_text().strip("\n\t")] = (
                    j.get_text().replace("\n", "").replace("\t", "").replace("'", '"')
                )
            except AttributeError:
                continue

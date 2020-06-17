import json
import os
from os import path
from pathlib import Path

import certifi
import urllib3
from bs4 import BeautifulSoup


class DiaryParser:
    def __init__(self):
        self.diary = {}
        self.data_source = 'https://www.mun.ca/regoff/calendar/sectionNo=GENINFO-0086'
        http = urllib3.PoolManager(cert_reqs="CERT_REQUIRED", ca_certs=certifi.where())
        mun_request = http.request(
            "GET", self.data_source
        )
        soup = BeautifulSoup(mun_request.data, "html.parser")
        left_aligned_data = soup.find_all("td", attrs={"align": "left"})
        right_aligned_data = soup.find_all("td", attrs={"align": "justify"})

        for i, j in zip(left_aligned_data, right_aligned_data):
            try:
                self.diary[i.find("p").get_text().strip("\n\t")] = (
                    j.get_text().replace("\n", "").replace("\t", "").replace("'", '"')
                )
            except AttributeError:
                continue

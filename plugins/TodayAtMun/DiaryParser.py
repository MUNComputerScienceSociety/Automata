import requests
from bs4 import BeautifulSoup


class DiaryParser:
    DATA_SOURCE = "https://www.mun.ca/regoff/calendar/sectionNo=GENINFO-0086"

    def __init__(self):
        self.diary = {}
        mun_request = requests.get(DiaryParser.DATA_SOURCE).text
        soup = BeautifulSoup(mun_request, "html.parser")
        dates_in_diary = soup.find_all("td", attrs={"align": "left"})
        description_of_date = soup.find_all("td", attrs={"align": "justify"})

        for left_item, right_item in zip(dates_in_diary, description_of_date):
            right_item_parse = right_item.get_text().split()
            try:
                self.diary[left_item.find("p").get_text().strip("\n\t")] = " ".join(
                    right_item_parse
                )
            except AttributeError:
                self.diary[left_item.find("li").get_text().strip("\n\t")] = " ".join(
                    right_item_parse
                )

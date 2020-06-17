from datetime import datetime, timedelta
from json import load
from pathlib import Path
from typing import Dict


class Today:
    """A class used to go find significant days on Mun Calendar"""

    def __init__(self, diary: Dict):
        self.diary = diary

    def set_current_date(self) -> None:
        """Current day, month, hour, second"""
        self.date = datetime.now()

    def get_current_date(self) -> datetime:
        """Getter method for date"""
        return self.date

    def format_date(self, date: datetime) -> str:
        """Provides current date formatted to Muns style."""
        time_format = date.strftime("%Y-%B-%#d-%A").split("-")
        curr_year = time_format[0]
        curr_month = time_format[1]
        curr_day = time_format[2]
        curr_day_of_week = time_format[3]

        return f"{curr_month} {curr_day}, {curr_year}, {curr_day_of_week}"

    def next_day(self) -> datetime:
        """Increases day by one"""
        self.date = self.date + timedelta(days=1)
        return self.date

    def go_to_event(self):
        """Sets dict value"""
        self.this_date = self.diary[self.fdate]

    def find_event(self, date: datetime) -> str:
        """Provides the significant event on the mun calendar"""
        self.fdate = self.format_date(date)
        for key in self.diary:
            if key == self.fdate:
                self.info_day = self.diary[key]
                return key

        self.find_event(self.next_day())

    def next_event(self, date: datetime):
        """Gets following event after next"""
        self.find_event(date)
        self.go_to_event()

from datetime import datetime, timedelta
from json import load
from pathlib import Path
from typing import Dict

class Today:
    """
    A class used to go find significant days on Mun Calendar

    ...

    Attributes:
    ------------
    None

    Methods
    ----------
    set_current_day() : None
        sets the current date at the moment called
    get_current_date() : datetime
        returns the the current date
    format_date() : str
        returns the formatted time string for dict lookup
    next_date() : None
        increases the date by one.
    goToEvent(): None
        dictionary lookup sets this to a variable
    findEvent() : str
        Looks for the next date in the dictionary. Starting at a date
    next_Event(): None
        Goes to the next date if user calls this after finding first event
    """

    def __init__(self,diary:Dict):

        #path = Path(__file__).parent
        #file_name = path / "diary.json"
        #with open(file_name, "r") as f:
            #self.info = load(f)
        self.diary = diary
        self.nextEvents = []
        self.temp_date = datetime.now()

    def set_current_date(self) -> None:
        """Current day, month, hour, second"""
        self.date = datetime.now()

    def get_current_date(self) -> datetime:
        """Getter method for date"""
        return self.date

    def format_date(self, date: datetime) -> str:
        """Provides current date formatted to Muns style."""
        temp = date.strftime("%Y-%B-%#d-%A").split("-")
        currYear = temp[0]
        currMonth = temp[1]
        currDay = temp[2]
        currDayOfWeek = temp[3]

        return f"{currMonth} {currDay}, {currYear}, {currDayOfWeek}"

    def next_day(self) -> datetime:
        """Increases day by one"""
        self.date = self.date + timedelta(days=1)
        return self.date

    def go_to_event(self):
        """Sets dict value"""
        self.thisDate = self.diary[self.fdate]

    def find_event(self, date: datetime) -> str:
        """Provides the significant event on the mun calendar"""
        self.fdate = self.format_date(date)
        for key in self.diary:
            if key == self.fdate:
                self.infoDay = self.diary[key]
                return key

        self.find_event(self.next_day())

    def next_event(self, date: datetime):
        """Gets following event after next"""
        self.nextEvent = self.find_event(date)
        self.go_to_event()

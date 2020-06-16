from datetime import datetime, timedelta
from json import load
from pathlib import Path

from plugins.TodayAtMun.Month import month


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

    def __init__(self):

        path = Path(__file__).parent
        file_name = path / "diary.json"
        with open(file_name, "r") as f:
            self.info = load(f)
        self.nextEvents = []
        self.temp_date = datetime.now()

    def set_current_date(self) -> None:
        #Current Day, Month, Hour, second
        self.date = datetime.now()

    def get_current_date(self) -> datetime:
        #Getter method for date
        return self.date

    def format_date(self, date: datetime) -> str:
        #Provides Current Date formatted to Muns style.
        temp = date.strftime("%Y-%#m-%#d-%A").split("-")
        currYear = temp[0]
        currMonth = int(temp[1])
        currDay = temp[2]
        currDayOfWeek = temp[3]

        return f"{month[currMonth]} {currDay}, {currYear}, {currDayOfWeek}"

    def nextDay(self) -> datetime:
        #Increases Day By One
        self.date = self.date + timedelta(days=1)
        return self.date

    def goToEvent(self):
        # sets dict value
        self.thisDate = self.info[self.fdate]

    def findEvent(self, date: datetime) -> str:
        #Provides the significant event on the mun calendar
        self.fdate = self.format_date(date)
        for key in self.info:
            if key == self.fdate:
                self.infoDay = self.info[key]
                return key

        self.findEvent(self.nextDay())

    def next_Event(self, date: datetime):
        # Gets following event after next
        self.nextEvent = self.findEvent(date)
        self.goToEvent()

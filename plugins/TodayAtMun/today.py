from datetime import datetime
from datetime import timedelta
from plugins.TodayAtMun.Month import month
from pathlib import Path
from json import load


class Today:
    def __init__(self):
        self.date = datetime.now()
        path = Path(__file__).parent
        file_name = path / "diary.json"
        with open(file_name, "r") as f:
            self.info = load(f)
        self.nextEvents = []
        self.temp_date = datetime.now()

    def set_current_date(self):
        """ Current Day, Month, Hour, second """
        self.date = datetime.now()

    def get_current_date(self):
        return self.date

    def format_date(self, date):
        """Provides Current Date formatted to Muns style."""
        temp = date.strftime("%Y-%#m-%#d-%A").split("-")
        currYear = temp[0]
        currMonth = int(temp[1])
        currDay = temp[2]
        currDayOfWeek = temp[3]

        return f"{month[currMonth]} {currDay}, {currYear}, {currDayOfWeek}"

    def nextDay(self):
        """Increases Day By One """
        self.date = self.date + timedelta(days=1)
        return self.date

    def goToEvent(self):
        self.thisDate = self.info[self.fdate]

    def findEvent(self, date):
        """ Provides the significant event on the mun calendar """
        #self.set_current_date()
        self.fdate = self.format_date(date)
        for key in self.info:
            if key == self.fdate:
                self.infoDay = self.info[key]
                return key

        self.findEvent(self.nextDay())

    def next_Event(self,date):
        self.nextEvent = self.findEvent(date)
        self.goToEvent()

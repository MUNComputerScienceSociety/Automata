from datetime import datetime
from datetime import timedelta
from plugins.TodayAtMun.Month import month
from pathlib import Path
from json import load

class Today:

    def set_current_date(self):
        """ Current Day, Month, Hour, second """
        self.date = datetime.now()
        path = Path(__file__).parent
        file_name = path / "diary.json"
        with open(file_name, "r") as f:
            self.info = load(f)

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
        self.fdate = self.format_date(self.date)
        for key in self.info:
            if key == self.fdate:
                self.infoDay = self.info[key]
                return True

        self.findEvent(self.nextDay())

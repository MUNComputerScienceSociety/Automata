from datetime import datetime, timedelta
from typing import Dict


class Today:
    """Provides methods to manipulate dates and lookup/match parsed data."""

    def __init__(self, diary: Dict):
        self.diary = diary
        self.curr_date = datetime.now()

    def set_current_date(self) -> None:
        """Sets the current date at that moment."""
        self.date = datetime.now()

    def get_current_date(self) -> datetime:
        """Returns current date."""
        return self.date

    def format_date(self, date: datetime) -> str:
        """Provides current date formatted to MUN style."""
        print("%B %-d, %Y, %A")
        return date.strftime("%B %d, %Y, %A")

    def next_day(self) -> datetime:
        """Increases day by one returns date."""
        self.date = self.date + timedelta(days=1)
        return self.date

    def go_to_event(self) -> None:
        """Look up key in dict and set it to variable."""
        self.this_date = self.diary[self.formatted_date]

    def find_event(self, date: datetime) -> str:
        """Searches for date/event pair in MUN calendar."""
        if self.date.year - datetime.now().year > 1:
            # Parsed data lookup is outside of 1 year.
            return ""
        self.formatted_date = self.format_date(date)
        for self.key in self.diary:
            if self.key == self.formatted_date:
                return self.key

        self.find_event(self.next_day())

    def next_event(self, date: datetime) -> None:
        """Finds the next significant date in diary."""
        self.find_event(date)
        self.go_to_event()

    def package_of_events(self, date: datetime, weight: int) -> dict:
        """Creates a package of upcoming events in MUN diary."""
        package_size = 0
        self.packaged_items = {}
        self.find_event(self.date)
        self.first_event = self.format_date(self.date)
        while package_size < weight:
            self.packaged_items[self.formatted_date] = self.diary[self.formatted_date]
            self.next_event(self.next_day())
            package_size += 1
        self.last_event = self.format_date(self.date)
        return self.packaged_items

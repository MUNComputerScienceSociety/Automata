from datetime import datetime, timedelta


class DiaryUtil:
    """Provides methods to manipulate dates and lookup/match parsed data."""

    def __init__(self, diary: dict[str, str]):
        self.diary = diary
        self.date = DiaryUtil.get_current_date()

    @staticmethod
    def get_current_date() -> datetime:
        return datetime.now()

    @staticmethod
    def str_to_datetime(str_date: str):
        return datetime.strptime(str_date, "%B %d, %Y, %A")

    @staticmethod
    def time_delta_event(
        event_date: datetime, curr_date: datetime = datetime.now()
    ) -> int:
        """Provides time delta of days remaining for a given date to current date."""
        return (
            DiaryUtil.truncate_date_time(event_date)
            - DiaryUtil.truncate_date_time(curr_date)
        ).days

    @staticmethod
    def truncate_date_time(date: datetime) -> datetime:
        return datetime(date.year, date.month, date.day)

    @staticmethod
    def time_to_dt_delta(date: str) -> int:
        convert_date = DiaryUtil.str_to_datetime(date)
        return DiaryUtil.time_delta_event(convert_date)

    def time_delta_emojify(self) -> str:
        remaining_time = DiaryUtil.time_delta_event(DiaryUtil.str_to_datetime(self.key))
        if remaining_time > 1:
            return f"⏳ {remaining_time} day(s)"
        elif 0 < remaining_time <= 1:
            return f"⌛ {remaining_time} day"
        elif remaining_time == 0:
            return "🔴"
        else:
            return "✅"

    def set_current_date(self) -> None:
        """Sets the current date at that moment."""
        self.date = datetime.now()

    def get_date(self) -> datetime:
        """Returns current date."""
        return self.date

    def format_date(self, date: datetime) -> str:
        """Provides current date formatted to MUN style."""
        return date.strftime("%B %-d, %Y, %A")

    def next_day(self, date: datetime) -> datetime:
        """Increases day by one returns date."""
        date = date + timedelta(days=1)
        return date

    def go_to_event(self) -> None:
        """Look up key in dict and set it to variable."""
        self.this_date = self.diary[self.key]

    def find_event(self, date: datetime) -> str:
        """Searches for date/event pair in MUN calendar."""
        if (date - DiaryUtil.get_current_date()).days == 365:
            return ""
        formatted_date = self.format_date(date)
        for self.key in self.diary:
            if self.key == formatted_date:
                return self.key
        return self.find_event(self.next_day(date))

    def next_event(self, date: datetime) -> None:
        """Finds the next significant date in diary."""
        self.find_event(date)
        self.go_to_event()

    def package_of_events(self, date: datetime, weight: int) -> list[datetime]:
        """Creates a package of upcoming events in MUN diary"""
        if weight < 0 or weight > 10:
            weight = 10
        packaged_items = {}
        while len(packaged_items) < weight:
            self.find_event(date)
            packaged_items[self.key] = self.diary[self.key]
            date = self.next_day(date)
        return packaged_items

    def today_is_next(self, date: str) -> str:
        """Provides an emoji indicator if the next event occurs on current day."""
        today_date = self.format_date(self.get_current_date())
        if today_date == date:
            return "🔴"
        return ""

    def find_following_event(self):
        """Provides date immediately following the next date in the calendar"""
        self.set_current_date()
        self.find_event(self.date)
        self.next_event(DiaryUtil.str_to_datetime(self.key) + timedelta(days=1))

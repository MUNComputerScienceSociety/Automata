import unittest

# from plugins.TodayAtMun.Diary import Diary
from Diary import Diary
from DiaryParser import DiaryParser
from datetime import datetime, timedelta, date


class TestDateMethods(unittest.TestCase):
    """Testing TodayAtMun Plugin"""

    parse = DiaryParser()
    diary = Diary(parse.diary)

    def test1_today_is_next(self):
        print("Start today_is_next tests")
        print("Success 1 - Test a formatted date that is not the same")
        self.assertEqual(self.diary.today_is_next("May 31, 2020, Monday"), "")
        print("Success 2 - Test a formatted date that is today")
        self.assertEqual(
            self.diary.today_is_next(self.diary.format_date(datetime.now())), "🔴"
        )
        print("Success 3 - Test a date that is not formatted")
        self.assertNotEqual(self.diary.format_date(datetime.now()), "🔴")

    def test2_time_delta_event(self):
        print("\nStart time_delta_event tests")
        print("Success 1 - Test a date ahead of the current date")
        self.assertAlmostEqual(
            self.diary.time_delta_event(datetime.now() + timedelta(days=3)), 2, 3
        )
        print("Success 2 - Test a current date")
        self.assertEqual(self.diary.time_delta_event(datetime.now()), 0)


if __name__ == "__main__":
    unittest.main()

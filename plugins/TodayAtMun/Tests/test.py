import sys
import unittest
from unittest.case import TestCase
import pytest


sys.path.append("../")
from datetime import date, datetime, timedelta
from DiaryUtil import DiaryUtil
from DiaryParser import DiaryParser


class TestDateMethods(unittest.TestCase):
    """Testing TodayAtMun Plugin"""

    parse = DiaryParser()
    diary = DiaryUtil(parse.diary)

    def test1_today_is_next(self):
        print("Start today_is_next tests")
        print("Success 1 - Test a formatted date that is not the same")
        self.assertEqual(self.diary.today_is_next("May 31, 2020, Monday"), "")
        print("Success 2 - Test a formatted date that is today")
        self.assertEqual(
            self.diary.today_is_next(self.diary.format_date(datetime.now())), "🔴"
        )
        print("Success 3 - Test a date that is not formatted")
        self.assertNotEqual(datetime.now(), "🔴")

    def test2_time_delta_event(self):
        print("\nStart time_delta_event tests")
        print("Success 1 - Test a date ahead of the current date")
        self.assertEqual(self.diary.time_delta_event(datetime.now()), 0)
        print("Success 2 - Test date with y, m, d")
        self.assertEqual(
            self.diary.time_delta_event(datetime(2022, 10, 2), datetime(2022, 10, 1)), 1
        )
        print("Success 3 - Test date with y, m, d, hr, min")
        self.assertEqual(
            self.diary.time_delta_event(
                datetime(2022, 10, 3, 23, 0), datetime(2022, 10, 2, 22, 59)
            ),
            1,
        )


@pytest.fixture
def parsed_diary():
    return DiaryUtil(DiaryParser().diary)

@pytest.mark.parametrize(
    "date, expected",
    [
    (date(2021, 10, 22), ""),
    (datetime.now(), "🔴")
    ],
)
def test_today_is_next(date, expected):
    parse = DiaryParser()
    diary = DiaryUtil(parse.diary)
    date = diary.format_date(diary.truncate_date_time(date))
    assert diary.today_is_next(date) == expected

@pytest.mark.parametrize(
    " today_time, event_time, expected",
    [
        (datetime(2022, 10, 2), datetime(2022, 10, 1), 1),
        (datetime(2022, 10, 2), datetime(2022, 10, 1), 1),
        (datetime(2022, 10, 3, 23, 0), datetime(2022, 10, 2, 22, 59), 1),
    ],
)
def test_time_delta_event(today_time, event_time, expected):
    parse = DiaryParser()
    diary = DiaryUtil(parse.diary)
    assert diary.time_delta_event(today_time, event_time) == expected


def test_package_of_events(parsed_diary):
    diary_data = {
        "October 23, 2010, Saturday": "Pizza Party",
        "November 20, 2010, Saturday": "foo",
        "December 10, 2010, Friday": "December",
        "December 30, 2010, Thursday": "Last Day of the year",
    }
    date = datetime(2010, 10, 22)
    TestCase().assertDictEqual(parsed_diary.package_of_events(date, 4), diary_data)

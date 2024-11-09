import sys
import unittest
from unittest.case import TestCase
import pytest

sys.path.append("../../../")
from datetime import date, datetime, timedelta
from plugins.TodayAtMun.DiaryUtil import DiaryUtil
from plugins.TodayAtMun.__init__ import TodayAtMun


class TestDateMethods(unittest.TestCase):
    """Testing TodayAtMun Plugin"""

    # parse = TodayAtMun.parse_diary()
    parse = {}
    diary = DiaryUtil(parse)

    def test1_today_is_next(self):
        self.assertEqual(self.diary.today_is_next("May 31, 2020, Monday"), "")
        self.assertEqual(
            self.diary.today_is_next(self.diary.format_date(datetime.now())), "🔴"
        )
        self.assertNotEqual(datetime.now(), "🔴")

    def test2_time_time(self):
        self.assertEqual(self.diary.delta_time(now := datetime.now(), now), 0)
        self.assertEqual(
            self.diary.delta_time(datetime(2022, 10, 1), datetime(2022, 10, 2)), 1
        )
        self.assertEqual(
            self.diary.delta_time(
                datetime(2022, 10, 2, 22, 59), datetime(2022, 10, 3, 23, 0)
            ),
            1,
        )


@pytest.fixture
def parsed_diary():
    diary = TodayAtMun.parse_diary()
    return DiaryUtil(diary)


@pytest.mark.parametrize(
    "date, expected",
    [(date(2021, 10, 22), ""), (datetime.now(), "🔴")],
)
def test_today_is_next(date, expected):
    parse = TodayAtMun.parse_diary()
    diary = DiaryUtil(parse)
    date = diary.format_date(diary.truncate_date_time(date))
    assert diary.today_is_next(date) == expected


@pytest.mark.parametrize(
    " today_time, event_time, expected",
    [
        (datetime(2022, 10, 2), datetime(2022, 10, 1), 1),
        (datetime(2022, 10, 2), datetime(2022, 10, 1), 1),
        (datetime(2022, 10, 3, 23, 0), datetime(2022, 10, 2, 22, 59), 1),
        (datetime(2000, 8, 2), datetime(2000, 8, 2), 0),
    ],
)
def test_time_delta_event(today_time, event_time, expected):
    diary = TodayAtMun.parse_diary()
    diary = DiaryUtil(diary)
    assert diary.delta_time(event_time, today_time) == expected


def test_package_of_events():
    diary_data = {
        "October 23, 2010, Saturday": "Pizza Party",
        "November 20, 2010, Saturday": "Santa Clause parade lol",
        "December 10, 2010, Friday": "December is on the go",
        "December 30, 2010, Thursday": "NYE EVE",
        "December 31, 2010, Friday": "Friday NYE",
        "January 1, 2011, Saturday": "NYD",
    }

    test1_diary_expected = {
        "October 23, 2010, Saturday": "Pizza Party",
        "November 20, 2010, Saturday": "Santa Clause parade lol",
        "December 10, 2010, Friday": "December is on the go",
        "December 30, 2010, Thursday": "NYE EVE",
    }

    test2_diary_expected = {
        "October 23, 2010, Saturday": "Pizza Party",
        "November 20, 2010, Saturday": "Santa Clause parade lol",
        "December 10, 2010, Friday": "December is on the go",
        "December 30, 2010, Thursday": "NYE EVE",
        "December 31, 2010, Friday": "Friday NYE",
    }
    date = datetime(2010, 10, 22)
    diary = DiaryUtil(diary_data)
    TestCase().assertDictEqual(diary.package_of_events(date, 4), test1_diary_expected)
    TestCase().assertDictEqual(diary.package_of_events(date, 5), test2_diary_expected)


def test_find_event(parsed_diary):
    future_date = datetime.now() + timedelta(days=400)
    formatted_future_date = parsed_diary.format_date(future_date)
    diary_data = {f"{formatted_future_date}": "2 years away"}
    diary_util = DiaryUtil(diary_data)
    date = datetime.now()
    assert diary_util.find_event(date) == ""

    future_date2 = datetime.now() + timedelta(days=30)
    formated_date2 = parsed_diary.format_date(future_date2)
    diary_data = {f"{formated_date2}": "40 days away"}
    diary_util = DiaryUtil(diary_data)
    assert diary_data[diary_util.find_event(date)] == "40 days away"


def test_daily_time_delta():
    time = datetime(2021, 10, 22)
    diary = {
        (time + timedelta(days=10)).strftime("%B %-d, %Y, %A"): "First event",
        (time + timedelta(days=20)).strftime("%B %-d, %Y, %A"): "Second event",
        (time + timedelta(days=30)).strftime("%B %-d, %Y, %A"): "Third event",
        (time + timedelta(days=40)).strftime("%B %-d, %Y, %A"): "Fourth event",
    }
    diary_key_list = list(diary)
    diary_util = DiaryUtil(diary)

    assert diary_util.find_event(time) == diary_key_list[0]
    next_event_date = diary_util.find_event(time)
    assert DiaryUtil.delta_time(time, DiaryUtil.str_to_datetime(next_event_date)) == 10
    time = time + timedelta(days=1)
    assert DiaryUtil.delta_time(time, DiaryUtil.str_to_datetime(next_event_date)) == 9
    time = time + timedelta(days=1)
    assert DiaryUtil.delta_time(time, DiaryUtil.str_to_datetime(next_event_date)) == 8
    time = datetime(2021, 10, 31)
    next_event_date = diary_util.find_event(time)
    assert DiaryUtil.delta_time(time, DiaryUtil.str_to_datetime(next_event_date)) == 1

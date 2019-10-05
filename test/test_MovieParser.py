import unittest
import datetime
from MovieScheduleParser import parser


def check_required_field_in_schedule(schedule: dict):

    assert 'start_time' in schedule.keys() and schedule['start_time'] is not None
    assert 'title' in schedule.keys() and schedule['title'] is not None
    assert 'rating' in schedule.keys() and schedule['rating'] is not None


class TestCJMovieParser(unittest.TestCase):

    def test_parse_cj_channel_today(self):
        cj_parser = parser.CJScheduleParser('http://ocn.tving.com/ocn/schedule')
        schedules = cj_parser.get_channel_schedule()

        self.assertNotEqual(schedules, None)

        for schedule in schedules:
            check_required_field_in_schedule(schedule)
            print(schedule)

    def test_parse_cj_channel_with_date(self):
        
        today = datetime.date.today()
        url = 'http://ocn.tving.com/ocn/schedule?startDate={:04d}{:02d}{:02d}'.format(today.year,
                                                                                      today.month,
                                                                                      today.day)
        cj_parser = parser.CJScheduleParser(url)
        schedules = cj_parser.get_channel_schedule()

        self.assertNotEqual(schedules, None)

        for schedule in schedules:
            check_required_field_in_schedule(schedule)
            print(schedule)

    def test_parse_cj_ocn(self):
        url = 'http://ocn.tving.com/ocn/schedule'
        cj_parser = parser.CJScheduleParser(url)
        schedules = cj_parser.get_channel_schedule()

        self.assertNotEqual(schedules, None)

    def test_parse_cj_super_action(self):
        url = 'http://superaction.tving.com/superaction/schedule'
        cj_parser = parser.CJScheduleParser(url)
        schedules = cj_parser.get_channel_schedule()

        self.assertNotEqual(schedules, None)

        for schedule in schedules:
            check_required_field_in_schedule(schedule)
            print(schedule)

    def test_parse_cj_ch_cgv(self):
        url = 'http://chcgv.tving.com/chcgv/schedule'
        cj_parser = parser.CJScheduleParser(url)
        schedules = cj_parser.get_channel_schedule()

        self.assertNotEqual(schedules, None)

        for schedule in schedules:
            check_required_field_in_schedule(schedule)
            print(schedule)


class TestCatchOnScheduleParser(unittest.TestCase):

    def test_parse_cj_catch_on_1(self):
        url = 'https://www.catchon.co.kr/mp/tv/exclude/ch1.co'
        catch_on_parser = parser.CatchOnScheduleParser(url)
        schedules = catch_on_parser.get_channel_schedule()

        self.assertNotEqual(schedules, None)

        for schedule in schedules:
            check_required_field_in_schedule(schedule)
            print(schedule)

    def test_parse_cj_catch_on_2(self):
        url = 'https://www.catchon.co.kr/mp/tv/exclude/ch2.co'
        catch_on_parser = parser.CatchOnScheduleParser(url)
        schedules = catch_on_parser.get_channel_schedule()

        self.assertNotEqual(schedules, None)

        for schedule in schedules:
            check_required_field_in_schedule(schedule)
            print(schedule)


class TestTCastMovieParser(unittest.TestCase):

    def test_parse_tcast_screen_channel(self):
        tcast_parser = parser.TCastScheduleParser('http://www.imtcast.com/screen/program/schedule.jsp')
        end_date, schedules = tcast_parser.get_channel_schedule()

        self.assertNotEqual(end_date, None)
        self.assertNotEqual(schedules, None)

        for schedule in schedules:
            check_required_field_in_schedule(schedule)
            print(schedule)

    def test_parse_tcast_cinef_channel(self):
        tcast_parser = parser.TCastScheduleParser('http://www.imtcast.com/cinef/program/schedule.jsp')
        end_date, schedules = tcast_parser.get_channel_schedule()

        self.assertNotEqual(end_date, None)
        self.assertNotEqual(schedules, None)

        for schedule in schedules:
            check_required_field_in_schedule(schedule)
            print(schedule)

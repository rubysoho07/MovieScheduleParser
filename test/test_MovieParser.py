import os
import unittest
import datetime
from MovieScheduleParser import parser


class TestCJMovieParser(unittest.TestCase):

    def test_parse_cj_channel_today(self):
        cj_parser = parser.CJScheduleParser('http://ocn.tving.com/ocn/schedule')
        schedules = cj_parser.get_channel_schedule()

        self.assertNotEqual(schedules, None)

    def test_parse_cj_channel_with_date(self):
        
        today = datetime.date.today()
        url = 'http://ocn.tving.com/ocn/schedule?startDate={:04d}{:02d}{:02d}'.format(today.year,
                                                                                      today.month,
                                                                                      today.day)
        cj_parser = parser.CJScheduleParser(url)
        schedules = cj_parser.get_channel_schedule()

        self.assertNotEqual(schedules, None)

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

    def test_parse_cj_ch_cgv(self):
        url = 'http://chcgv.tving.com/chcgv/schedule'
        cj_parser = parser.CJScheduleParser(url)
        schedules = cj_parser.get_channel_schedule()

        self.assertNotEqual(schedules, None)

    def test_parse_cj_catch_on_1(self):
        url = 'http://catchon.tving.com/catchon/schedule1'
        cj_parser = parser.CJScheduleParser(url)
        schedules = cj_parser.get_channel_schedule()

        self.assertNotEqual(schedules, None)

    def test_parse_cj_catch_on_2(self):
        url = 'http://catchon.tving.com/catchon/schedule2'
        cj_parser = parser.CJScheduleParser(url)
        schedules = cj_parser.get_channel_schedule()

        self.assertNotEqual(schedules, None)


class TestTCastMovieParser(unittest.TestCase):

    def test_parse_tcast_screen_channel(self):
        tcast_parser = parser.TCastScheduleParser('http://www.imtcast.com/screen/program/schedule.jsp')
        end_date, schedules = tcast_parser.get_channel_schedule()

        self.assertEqual(os.path.exists('/tmp/geckodriver.log'), False)
        self.assertNotEqual(end_date, None)
        self.assertNotEqual(schedules, None)

    def test_parse_tcast_cinef_channel(self):
        tcast_parser = parser.TCastScheduleParser('http://www.imtcast.com/cinef/program/schedule.jsp')
        end_date, schedules = tcast_parser.get_channel_schedule()

        self.assertEqual(os.path.exists('/tmp/geckodriver.log'), False)
        self.assertNotEqual(end_date, None)
        self.assertNotEqual(schedules, None)

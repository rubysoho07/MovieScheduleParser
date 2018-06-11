import os
import unittest
import datetime
from MovieScheduleParser import parser


class TestMovieParser(unittest.TestCase):

    def test_parse_cj_channel_today(self):
        cj_parser = parser.CJScheduleParser()
        schedules = cj_parser.get_channel_schedule('http://ocn.tving.com/ocn/schedule')

        self.assertNotEqual(schedules, None)

    def test_parse_cj_channel(self):
        cj_parser = parser.CJScheduleParser()
        today = datetime.date.today()
        url = 'http://ocn.tving.com/ocn/schedule?startDate={:04d}{:02d}{:02d}'.format(today.year,
                                                                                      today.month,
                                                                                      today.day)
        schedules = cj_parser.get_channel_schedule(url)

        self.assertNotEqual(schedules, None)

    def test_parse_tcast_channel(self):
        tcast_parser = parser.TCastScheduleParser('Screen')
        end_date, schedules = tcast_parser.get_channel_schedule('http://www.imtcast.com/screen/program/schedule.jsp')

        self.assertEqual(os.path.exists('/tmp/geckodriver.log'), False)
        self.assertNotEqual(end_date, None)
        self.assertNotEqual(schedules, None)

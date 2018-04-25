import os
import unittest
from MovieScheduleParser import parser


class TestMovieParser(unittest.TestCase):

    def test_parse_cj_channel(self):
        cj_parser = parser.CJScheduleParser()
        schedules = cj_parser.get_channel_schedule('http://ocn.tving.com/ocn/schedule')
        print(schedules)

        self.assertNotEqual(schedules, None)

    def test_parse_tcast_channel(self):
        tcast_parser = parser.TCastScheduleParser('Screen')
        end_date, schedules = tcast_parser.get_channel_schedule('http://www.imtcast.com/screen/program/schedule.jsp')
        print(end_date)
        print(schedules)

        if os.path.exists('/tmp/ghostdriver.log'):
            os.remove('/tmp/ghostdriver.log')

        self.assertNotEqual(end_date, None)
        self.assertNotEqual(schedules, None)
        self.assertEqual(os.path.exists('/tmp/ghostdriver.log'), False)

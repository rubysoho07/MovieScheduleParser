# -*- coding: utf-8 -*-
"""
    Movie Schedule Parser.
    2017~2019 Yungon Park
"""
import os
import re
from datetime import datetime, timezone, timedelta, date

import requests
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


class MovieScheduleParser(object):
    """Parse movie schedule from schedule table of Korean movie channels."""

    def __init__(self, url):
        self.url = url

    @staticmethod
    def _get_original_data(url):
        """Get source from web and returns BeautifulSoup object."""

        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:49.0) Gecko/20100101 Firefox/49.0'
        }
        data = requests.get(url, headers=headers)

        return BeautifulSoup(data.text, "html.parser")

    @staticmethod
    def _parse_string_to_int(string_to_parse, default=0):
        """Try to parse string to int, or return default value."""

        try:
            return int(string_to_parse)
        except ValueError:
            return default

    @staticmethod
    def execute_chromium():
        """ Execute Chromium in headless mode """

        options = webdriver.ChromeOptions()
        options.binary_location = os.path.join(os.path.dirname(__file__), 'headless-chromium')
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        driver = webdriver.Chrome(os.path.join(os.path.dirname(__file__), 'chromedriver'), options=options,
                                  service_log_path='/tmp/chromium.log')

        return driver

    @staticmethod
    def clean_chromium_log():

        if os.path.exists('/tmp/chromium.log'):
            os.remove('/tmp/chromium.log')

    def _get_rating(self, rating):
        raise NotImplementedError

    def _parse_schedule_item(self, item, schedule_date):
        raise NotImplementedError

    def _parse_daily_schedule(self, table, schedule_date):
        raise NotImplementedError

    def get_channel_schedule(self):
        raise NotImplementedError


class CJScheduleParser(MovieScheduleParser):
    """Parser for movie schedule from CJ E&M channels."""

    def _get_rating(self, rating):
        """Return rating information from string."""

        age = re.findall(r'age(\d{1,2})', rating)

        if len(age) == 0:
            return 0
        else:
            return age[0]

    def _parse_schedule_item(self, item, schedule_date):
        """Return CJ E&M channel schedule from table row."""

        schedule = dict()

        # Get title
        try:
            title = item.find('div', class_='program')['title']
        except KeyError:
            # Remove span tag
            title = item.find('div', class_='program').text

        schedule['title'] = title.strip()

        # Get ratings
        rating = item.find('td', class_='rating').find('span')['class'][0]
        schedule['rating'] = self._get_rating(rating)

        # Get start_time and end_time
        duration = item.find('td', class_='runningTime').text
        start_time = datetime.strptime(item.find('em').text.strip(), "%H:%M")
        start_datetime = schedule_date.replace(hour=start_time.hour, minute=start_time.minute)
        schedule['start_time'] = start_datetime
        schedule['end_time'] = \
            start_datetime + timedelta(minutes=MovieScheduleParser._parse_string_to_int(duration, 0))

        return schedule

    def _parse_daily_schedule(self, table, schedule_date):
        """Get daily schedule for CJ E&M channels."""

        schedule_list = []

        last_hour = 0  # Hour of last schedule
        for item in table:
            schedule = self._parse_schedule_item(item, schedule_date)

            if schedule['start_time'].hour < last_hour and last_hour >= 22:
                # Move to next day's schedule.
                schedule['start_time'] = (schedule['start_time'] + timedelta(days=1)).isoformat()
                schedule['end_time'] = (schedule['end_time'] + timedelta(days=1)).isoformat()

                # Move to next day.
                schedule_date = schedule_date + timedelta(days=1)
            elif schedule['end_time'].day != schedule_date.day:
                # Set next day because next schedule is for next day.
                schedule_date = schedule_date + timedelta(days=1)

            # Save hour field of last schedule.
            last_hour = schedule['end_time'].hour

            schedule_list.append(schedule)

        return schedule_list

    def get_channel_schedule(self):
        """Get movie schedule from CJ E&M channels."""

        schedule = self._get_original_data(self.url).find('div', class_='scheduler')

        date_text = schedule.find('em').text[:-4].strip()
        date_split = date_text.split(".")

        # If date is different from the day of argument, return None.
        if self.url.find('startDate') != -1 and "".join(date_split) != self.url[-8:]:
            return None

        schedule_date = datetime(int(date_split[0]), int(date_split[1]), int(date_split[2]))
        # Set to Korea Standard Time (KST)
        schedule_date = schedule_date.astimezone(timezone(timedelta(hours=9)))
        schedule_table = schedule.find('tbody').find_all('tr')

        if len(schedule_table) == 0:
            # If no schedule exists
            return None

        return self._parse_daily_schedule(schedule_table, schedule_date)


class CatchOnScheduleParser(MovieScheduleParser):
    """ Parser for movie schedule from Catch On Channels. """

    @staticmethod
    def _parse_date(date_txt: str):
        """ Parse date to parse movie schedule. """

        today = date.today()
        parsed_date = datetime.strptime(date_txt, '%m.%d')

        return parsed_date.replace(year=today.year).date()

    def _parse_schedule_item(self, item, schedule_date):

        schedule = dict()

        start_time_str = item.find('span', class_='time').text

        if start_time_str.startswith('\nNOW'):
            start_time_str = start_time_str[4:]

        start_time = datetime.strptime(start_time_str.strip(), '%H:%M').time()
        start_time_dt = datetime.combine(schedule_date, start_time).astimezone(timezone(timedelta(hours=9)))

        duration = self._parse_string_to_int(item.find('span', class_='runningTime').text[:-1])

        schedule['start_time'] = start_time_dt.isoformat()
        schedule['end_time'] = (start_time_dt + timedelta(minutes=duration)).isoformat()

        schedule['title'] = item.find('span', class_='title').find('strong').text

        schedule['rating'] = self._get_rating(item)

        return schedule

    def _parse_daily_schedule(self, table, schedule_date):
        schedule_list = []

        for row in table:
            item = row.find('div', class_='items')
            result = self._parse_schedule_item(item, schedule_date)
            schedule_list.append(result)

        return schedule_list

    def get_channel_schedule(self):
        """ Get Catch On channel schedule until no schedule exists. And return last update date. """

        driver = self.execute_chromium()
        driver.get(self.url)

        # Get current week of start_date
        source = BeautifulSoup(driver.page_source, 'html.parser')
        schedule_table = source.find('ul', class_='schedule').find_all('li')
        table_date = self._parse_date(source.find('span', class_='date').text)

        schedules = self._parse_daily_schedule(schedule_table, table_date)

        driver.close()

        return schedules

    def _get_rating(self, rating):

        if rating.find('span', class_='tag adult') is not None:
            return 19

        rating_span = rating.find('span', class_='gradeType')

        if rating_span is not None:
            return self._parse_string_to_int(rating_span.text.strip()[1:-1])
        else:
            return 0


class TCastScheduleParser(MovieScheduleParser):
    """Parser for movie schedule from t.cast channels."""

    def __init__(self, url, start_date=None):
        """Constructor for the parser of t.cast channel. It needs channel, start_hour, start_date."""
        super().__init__(url)
        self.start_hour = self._get_tcast_start_hour(url)
        if start_date is None:
            self.start_date = datetime.today()
        else:
            self.start_date = start_date

        # Remove time information
        self.start_date = self.start_date.replace(hour=0, minute=0, second=0, microsecond=0)
        # Set to Korea Standard Time (KST)
        self.start_date = self.start_date.astimezone(timezone(timedelta(hours=9)))

    @staticmethod
    def _get_tcast_start_hour(url):
        """Get start hour of schedule table from t.cast channel."""

        if url.startswith('http://www.imtcast.com/cinef/'):
            return 6
        else:
            return 5

    @staticmethod
    def _check_tcast_date_range(schedule_date, date_range):
        """Extract date range from table and check if date is in that range."""

        found = False
        for i in date_range[1:]:
            if str(i.find_all(text=True)[-1]) == datetime.strftime(schedule_date, "%Y.%m.%d"):
                found = True
                break

        return found

    def _get_tcast_next_week_page(self, start_date, date_range, wait, driver):
        """Get next week schedule page from t.cast channels."""

        while self._check_tcast_date_range(start_date, date_range) is not True:
            driver.find_element_by_xpath("//span[@class='next']/a").click()
            _ = wait.until(expected_conditions.element_to_be_clickable((By.XPATH, "//span[@class='next']/a")))
            date_range = BeautifulSoup(driver.page_source, 'html.parser').find_all('th')

        return driver

    def _get_rating(self, rating):
        """Return rating information from file name of rating information."""

        rating_file_name = rating.split("/")[-1]

        age = re.findall(r'icon_(\d{1,2})age.gif', rating_file_name)

        if len(age) == 0:
            return 0
        else:
            return age[0]

    def _parse_schedule_item(self, item, schedule_date):
        """
        Make single schedule for t.cast channel. Return single schedule dictionary.

        :param item: <div class="con active">
        :param schedule_date: <strong>05:30</strong>
        :return schedule of movie
        """

        schedule = dict()

        start_time = datetime.strptime(item.find('strong').text.strip(), "%H:%M")
        start_datetime = schedule_date.replace(hour=start_time.hour, minute=start_time.minute)
        schedule['start_time'] = start_datetime.isoformat()

        schedule['title'] = item.find('a').text.strip()

        rating = item.find('img')
        if rating is None:
            schedule['rating'] = 0
        else:
            schedule['rating'] = self._get_rating(rating['src'])

        return schedule

    def _parse_daily_schedule(self, table, schedule_date):
        """Get daily schedule for t.cast channel."""

        date_format = datetime.strftime(schedule_date, "%Y%m%d")
        daily_schedule = []

        # Get schedule
        for hour in range(24):
            date_hour_string = date_format + '{:02d}'.format(hour)
            cell = table.find('td', id=date_hour_string)

            if cell is None:
                return None

            schedules = cell.find_all('div', class_='con active')
            for schedule in schedules:
                if hour in range(self.start_hour):
                    daily_schedule.append(self._parse_schedule_item(schedule, schedule_date + timedelta(days=1)))
                else:
                    daily_schedule.append(self._parse_schedule_item(schedule, schedule_date))

        # Add to list
        return daily_schedule

    def _parse_schedule_from_table(self, source, schedule_date):
        """
        Find schedule table and parse daily schedule from the table.
        Finally, return schedule list
        """

        schedule_table = BeautifulSoup(source, 'html.parser').find('tbody')
        temp_schedules = self._parse_daily_schedule(schedule_table, schedule_date)

        return temp_schedules

    def get_channel_schedule(self):
        """Get t.cast channel schedule until no schedule exists. And return last update date. """

        driver = self.execute_chromium()
        driver.get(self.url)

        # Get current week of start_date
        date_range = BeautifulSoup(driver.page_source, 'html.parser').find_all('th')
        wait = WebDriverWait(driver, 8)

        driver = self._get_tcast_next_week_page(self.start_date, date_range, wait, driver)

        # Get one day's schedule iteratively.
        end_date = self.start_date
        schedules = []
        temp_schedules = self._parse_schedule_from_table(driver.page_source, self.start_date)
        while len(temp_schedules) != 0:
            if temp_schedules is not None:
                schedules += temp_schedules

            end_date = end_date + timedelta(days=1)
            temp_schedules = self._parse_schedule_from_table(driver.page_source, end_date)

            if temp_schedules is None:
                driver = self._get_tcast_next_week_page(end_date, date_range, wait, driver)
                temp_schedules = self._parse_schedule_from_table(driver.page_source, end_date)

        driver.close()

        return end_date, schedules

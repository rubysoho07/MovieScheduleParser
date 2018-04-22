from setuptools import setup, find_packages

setup(
    name='MovieScheduleParser',
    version='0.0.1',
    url='https://github.com/rubysoho07/MovieScheduleParser',
    author='Yungon Park',
    author_email='hahafree12@gmail.com',
    description='Parsing broadcasting schedules from Korean cable broadcasting stations.',
    install_requires=[
        "requests == 2.18.4",
        "beautifulsoup4 == 4.6.0",
        "selenium == 3.8.0",
    ],
    packages=find_packages()
)

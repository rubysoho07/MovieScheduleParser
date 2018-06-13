from setuptools import setup, find_packages

setup(
    name='MovieScheduleParser',
    version='0.0.2',
    url='https://github.com/rubysoho07/MovieScheduleParser',
    author='Yungon Park',
    author_email='hahafree12@gmail.com',
    description='Parsing broadcasting schedules from Korean cable broadcasting stations.',
    install_requires=[
        "requests",
        "beautifulsoup4",
        "selenium",
    ],
    packages=find_packages(
        exclude=['test']
    ),
    include_package_data=True,
    zip_safe=False
)

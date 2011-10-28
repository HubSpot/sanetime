#!/usr/bin/env python
from distutils.core import setup

setup(
    name='sanetime',
    version='3.0.0',
    description='A drop-in replacement for datetime that bring sanity and ease-of-use to the date/time/timezone/dateutil/calendar/pytz/timetuple/parsing insane shitshow.',
    author='Michael Prior',
    author_email='prior@cracklabs.com',
    url='https://github.com/prior/sanetime',
    download_url='https://github.com/prior/sanetime/tarball/v3.0.0',
    packages=['sanetime'],
    install_requires=[
        'nose',
        'pytz',
        'unittest2',
        'python-dateutil==1.5'
    ],
    long_description="""

        A drop-in replacement for datetime that bring sanity and ease-of-use to the date/time/timezone/dateutil/calendar/pytz/timetuple/parsing insane shitshow.

        This library forces timezones on every object, and stores everything in UTC micros internally.  Expect ease-of-use and correctness in all aspects of datetime/timezone manipulation now.

        Maintained on github:
            https://github.com/prior/sanetime

    """

)

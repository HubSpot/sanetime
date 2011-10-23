#!/usr/bin/env python
from distutils.core import setup

setup(
    name='sanetime',
    version='2.0.0',
    description='A Sane date/time/timezone/dateutil/calendar/pytz Wrapping Time Class',
    author='Michael Prior',
    author_email='prior@cracklabs.com',
    url='',
    packages=['sanetime'],
    install_requires=[
        'nose',
        'pytz',
        'unittest2',
        'python-dateutil==1.5'
    ]
)

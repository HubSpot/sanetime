#!/usr/bin/env python
from distutils.core import setup

setup(
    name='sanetime',
    version='3.4.1',
    description='A drop-in replacement for datetime that brings sanity and ease-of-use to the date/time/timezone/dateutil/calendar/pytz/timetuple/parsing insane shitshow.',
    long_description = open('README.md').read(),
    author='Michael Prior',
    author_email='prior@cracklabs.com',
    url='https://github.com/prior/sanetime',
    download_url='https://github.com/prior/sanetime/tarball/v3.4.1',
    license='LICENSE.txt',
    packages=['sanetime'],
    install_requires=[
        'nose==1.1.2',
        'pytz==2012b',
        'python-dateutil==1.5'
    ]
)

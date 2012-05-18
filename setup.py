#!/usr/bin/env python
from setuptools import setup, find_packages

VERSION = '4.0.8'

setup(
    name='sanetime',
    version=VERSION,
    author='prior',
    author_email='mprior@hubspot.com',
    packages=find_packages(),
    url='https://github.com/HubSpot/sanetime',
    download_url='https://github.com/HubSpot/sanetime/tarball/v%s'%VERSION,
    license='LICENSE.txt',
    description='A sane date/time python interface:  better epoch time, timezones, and deltas -- django support as well',
    long_description=open('README.rst').read(),
    install_requires=[
        'pytz>=2010',
        'python-dateutil>=1.5,<2.0'  # we're not compatible with python 3.0 yet
    ],
    platforms=['any']
)


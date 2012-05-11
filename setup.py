#!/usr/bin/env python
from distutils.core import setup

VERSION = '4.0.7'

setup(
    name='sanetime',
    version=VERSION,
    author='Michael Prior',
    author_email='prior@cracklabs.com',
    packages=['sanetime'],
    url='https://github.com/prior/sanetime',
    download_url='https://github.com/prior/sanetime/tarball/v%s'%VERSION,
    license='LICENSE.txt',
    description='A sane date/time python interface -- better epoch time, timezones, and deltas -- django support as well',
    long_description=open('README.rst').read(),
    install_requires=[
        'pytz>=2010',
        'python-dateutil>=1.5,<2.0'  # we're not compatible with python 3.0 yet
    ]
)



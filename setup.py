#!/usr/bin/env python
from distutils.core import setup

VERSION = '4.0.1'

setup(
    name='sanetime',
    version=VERSION,
    author='Michael Prior',
    author_email='prior@cracklabs.com',
    packages=['sanetime'],
    url='https://github.com/prior/sanetime',
    download_url='https://github.com/prior/sanetime/tarball/v%s'%VERSION,
    license='LICENSE.txt',
    description='A sane date/time python interface -- better epoch time, timezone, and delta support -- optional django support as well',
    long_description=open('README.rst').read(),
    install_requires=[ 
        'nose==1.1.2', 
        'pytz>=2012b', 
        'python-dateutil==1.5' 
    ]
)



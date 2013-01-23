#!/usr/bin/env python
from setuptools import setup, find_packages

__VERSION__ = '4.2.2'

setup(
    name='sanetime',
    version=__VERSION__,
    author='prior',
    author_email='mprior@hubspot.com',
    maintainer='prior',
    maintainer_email='mprior@hubspot.com',
    packages=find_packages(),
    url='http://hubspot.github.com/sanetime/',
    download_url='https://github.com/HubSpot/sanetime/tarball/v%s'%__VERSION__,
    license=open('LICENSE').read(),
    description='A sane date/time python interface:  better epoch time, timezones, and deltas -- django support as well',
    long_description=open('README.markdown').read(),
    install_requires=[
        'pytz>=2010',
        'python-dateutil>=1.5,<2.0',  # we're not compatible with python 3.0 yet
        'unittest2'
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Database',
        'Topic :: Internet',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Scientific/Engineering :: Physics',
        'Topic :: Software Development',
        'Topic :: Software Development :: Internationalization',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Localization',
        'Topic :: Utilities',
    ],
    include_package_data=True,
    test_suite='sanetime.test',
    platforms=['any']
)


sanetime
========

**a sane date/time python library**

::

    >>> from sanetime import time
    >>> time('2011-01-01 23:00','America/New_York').ms  # str to epoch millis
    1335758969218
    >>> str(time(1335752844194691))  # epoch micros to str
    '2012-04-30 02:27:24.194691 UTC'
    >>> (time('2012-05-01') - datetime(2012,6,1)).hours # hours in the month of may
    38234
    >>> time(s=1335758200,tz='Europe/London').datetime # epoch millis to tz-ed datetime
    datetime.datetime(2012, 4, 30, 4, 56, 40, tzinfo=<DstTzInfo 'Europe/London' BST+1:00:00 DST>)
    >>> time().ms  # epoch millis at this moment
    2909423432
    >>> -(time()-time()).us  # microseconds between construction moments
    84
    >>> (time(s=2039420392) - time(s=239402342)).rounded_hours  # rounded
    2


**sanetime** was written to DRY up all the common date/time manipulations we do constantly in our code while offering the most simple and intuitive client possible.
We've all learned that the only sane way to store and manipulate times is using epoch time. (You have, haven't you?)
Unfortunately, manipulating epoch time and timezones with the standard python toolset can be very frustrating.
**sanetime** tries to bring a little more sanity to manipulation of timezones, epoch time, time deltas, and time generally.

API Documentation
-----------------

If you are looking for information on a specific function, class or method,
this part of the documentation is for you.

.. toctree::
   :maxdepth: 2

   api


who?
----
If you've ever used python's datetime, date, time, calendar, timedelta, timetuple, pytz, and dateutil modules and thought: "Wow -- I love how explicit I'm being right now", then this library is not for you.

If, on the other hand, you'd rather not have to remember how to be so explicit, then you have found what you're looking for.


time
====
The ``time`` class represents a moment in time, internally stored as microseconds since epoch.  
A ``time`` object always keeps a timezone kicking around (UTC by default), however the timezone will never be considered during hashing, comparison or equality checks.  
A moment in time experienced in America/New_York is equal to the same moment in time experienced in Europe/Dublin.
If you need this single moment in time experienced in two different timezones to be inequal, then use the tztime class instead

tztime
======
All the features of time, except that it 



construction
------------
from epoch time
::

    >>> from sanetime import time
    >>> t = time()
    >>> time(t.us) == time(us=t.us) == time(micros=t.us) == time(microseconds=t.us)
    True
    >>> time(ms=1) == time(millis=1) == time(milliseconds=1)
    True
    >>> time(s=1) == time(secs=1) == time(seconds=1)
    True


from string
::

    >>> # 
    >>> time

    >>> str(time(2**50))
    '2011-01-01 23:00','America/New_York').ms
    1335758969218

    >>> str(time(1335752844194691))  # human readable str
    '2012-04-30 02:27:24.194691 UTC'
    
    >>> time(s=1335758200,tz='Europe/London').datetime
    datetime.datetime(2012, 4, 30, 4, 56, 40, tzinfo=<DstTzInfo 'Europe/London' BST+1:00:00 DST>)
    
    >>> time().ms  # epoch millis at this moment
    2909423432

    >>> -(time()-time()).us
    84

    >>> (time(s=2039420392) - time(s=239402342)).rounded_hours
    2


properties
----------

methods
-------


tztime
======
``tztime`` represents a moment in time and where that time was experienced (i.e. the timezone), internally stored as microseconds since epoch and timezone.

delta
=====
``delta`` is an amount of time, internally stored as microseconds.





time
----

If you're looking to get a better handle on what it can do, just read through the examples



principles
==========
* intuitive: easy to remember methods, with many reasonable aliases - be as verbose (and communicative) or as terse (and efficient) as you want to be.  for example  t = time();  t.ms == t.millis == t.milliseconds
* simple: eas






okay...
----------



FAQ
===
Why is everything stored internally as microseconds?

Python's datetime gives us access to microseconds, and since milliseconds would already have us cross the 32bit integer boundary, we might as well capture everything we can and take on microseconds as well.  There are plenty of helpers on the time, tztime, and delta classes so you never have to see/manipulate the huge microsecond numbers yourself.





The Basics
==========

time
----
``time`` represents only a moment in time, internally stored as microseconds since epoch.

timetz
------
``timetz`` represents a moment in time and where that time is experienced (i.e. the timezone), internally stored as microseconds since epoch and timezone.

delta
-----



Confusion
=========
Though sanetime avoids a menagerie of confusion you'd encounter without it, it does introduce one unavoidable? point of confusion.  delta's can never change based on context -- that means a delta(d=1) is always 24 hours.  So you have to be careful around daylight savings time jumps.   Whenever you use something like this: delta(d=1), you should be thinking 24 hours.  For example:



::

    >>> time('2011-01-01','America/New_York').ms
    23208402093

    >>> tztime('2012-04-15 12:30','America/New_York')-delta(d=1)

    48238492992932

    >>> -(time()-time()).us
    84

    >>> (time('2011-01-01',tz='America/New_York') - time('2011-01-01',tz='America/Phoenix')).h
    2

    >>> str(time('2011-01-01',tz='America/New_York') + delta(h=12)).with_tz('America/Phoenix'))



Requests: HTTP for Humans
=========================

Release v\ |version|. (:ref:`Installation <install>`)

Requests is an :ref:`ISC Licensed <isc>` HTTP library, written in Python, for human beings.

Python's standard **urllib2** module provides most of
the HTTP capabilities you need, but the API is thoroughly **broken**.
It was built for a different time — and a different web. It requires an *enormous* amount of work (even method overrides) to perform the simplest of tasks.

Things shouldn’t be this way. Not in Python.

::

    >>> r = requests.get('https://api.github.com', auth=('user', 'pass'))
    >>> r.status_code
    204
    >>> r.headers['content-type']
    'application/json'
    >>> r.text
    ...

See `the same code, without Requests <https://gist.github.com/973705>`_.

Requests takes all of the work out of Python HTTP/1.1 — making your integration with web services seamless. There's no need to manually add query strings to your URLs, or to form-encode your POST data. Keep-alive and HTTP connection pooling are 100%  automatic, powered by `urllib3 <https://github.com/shazow/urllib3>`_, which is embedded within Requests.


Testimonials
------------

`Heroku <http://heroku.com>`_, `PayPal <https://www.paypal.com/>`_,
`Transifex <https://www.transifex.net/>`_,
`Native Instruments <http://www.native-instruments.com/>`_, `The Washington Post <http://www.washingtonpost.com/>`_,
`Twitter, Inc <http://twitter.com>`_,
`Readability <http://readability.com>`_, and
Federal US Institutions
use Requests internally. It has been installed over 100,000 times from PyPI.

**Armin Ronacher**
    Requests is the perfect example how beautiful an API can be with the
    right level of abstraction.

**Matt DeBoard**
    I'm going to get @kennethreitz's Python requests module tattooed
    on my body, somehow. The whole thing.

**Daniel Greenfeld**
    Nuked a 1200 LOC spaghetti code library with 10 lines of code thanks to
    @kennethreitz's request library. Today has been AWESOME.

**Kenny Meyers**
    Python HTTP: When in doubt, or when not in doubt, use Requests. Beautiful,
    simple, Pythonic.


Feature Support
---------------

Requests is ready for today's web.

- International Domains and URLs
- Keep-Alive & Connection Pooling
- Sessions with Cookie Persistence
- Browser-style SSL Verification
- Basic/Digest Authentication
- Elegant Key/Value Cookies
- Automatic Decompression
- Unicode Response Bodies
- Multipart File Uploads
- Connection Timeouts
- ``.netrc`` support





Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


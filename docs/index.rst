sanetime
========

**a sane date/time python interface**

::

    >>> from sanetime import time

    >>> time('2011-01-01 23:01','America/New_York').ms
    1293940860000

    >>> moment = time(ms=1335752844194,tz='Europe/London')
    >>> str(t = time(ms=1335752844194,'Europe/London'))
    '2012-04-30 03:27:24.194000 +Europe/London'

    >>> str(time(ms=1335752844194,'Europe/London').set_tz('America/New_York'))
    '2012-04-30 02:27:24.194691 UTC'

    >>> (time('2012-05-01') - time(2012,6,1)).hours
    38234

    >>> time(s=1335758200,tz='UTC').datetime 
    datetime.datetime(2012, 4, 30, 4, 56, 40, tzinfo=<DstTzInfo 'Europe/London' BST+1:00:00 DST>)

    >>> time().ms  # now epoch millis
    2909423432

    >>> abs(time()-time()).us
    84

    >>> str(time(s=2039420392) - time(s=239402342))
    2


**sanetime** was written to DRY up all the common date/time manipulations we all do constantly in our code while offering the most simple and intuitive client possible.

We've all learned that the only sane way to store times is using epoch time. (You have, haven't you?)

Unfortunately, manipulating epoch time and timezones with the standard python toolset requires getting up to speed on a managerie of python modules and concepts: datetime, date, time, calendar, pytz, dateutils, timedelta, time tuples, localize, normalize.

**sanetime** seeks to bring a little more sanity ot the manipulations of epoch time, timezone, time delta, and time generally.


time
====
The ``time`` class represents a moment in time, internally stored as microseconds since epoch.  
A ``time`` object also has a timezone (UTC by default), however the timezone will never be considered during hashing, comparison or equality checks.  
A moment in ``time`` experienced in America/New_York is equal to the same moment in ``time`` experienced in Europe/Dublin.

tztime
======
The ``tztime`` class is exactly like the ``time`` object, except that timezone factors into equality.  
A moment in ``tztime`` experienced in America/New_York is **not** the same as the same ``tztime`` moment experienced in Europe/Dublin.

delta
=====
The ``delta`` class represents a period of time, and provides easy access to all the different ways you might slice and dice this: micros, millis, seconds, minutes, hours, mean_days, mean_weeks, mean_months, mean_years.  
There are many aliases so you may be as terse or as explicit as you want to be, and there are many different flavors of these: rounded, floored, floated, positional, rounded_positional.
There is no attempt made in delta yet to be calendar aware (hence the 'mean' prefixes in some cases).

span
====
The ``span`` class represents a window of time ranging from one specific moment in time to another specific moment in time.  
You can think of it as a start ``time`` with a ``delta``, or as a start ``time`` and a stop ``time``.

django
======
A django model field is also provided: SaneTimeField, that makes it super simple to store a sanetime.
They honor the auto_add and auto_add_now features to easily turn your sanetimes into updated_at or created_at fields.
And they even work with south out of the box.


API Documentation
-----------------

If you are looking for information on a specific function, class or method,
this part of the documentation is for you.

.. toctree::
   :maxdepth: 2

   api



principles
==========
* intuitive: easy to remember methods, with many reasonable aliases - be as verbose (and communicative) or as terse (and efficient) as you want to be.  for example  t = time();  t.ms == t.millis == t.milliseconds
* simple: eas


FAQ
===
Why is everything stored internally as microseconds?

Python's datetime gives us access to microseconds, and since milliseconds would already have us cross the 32bit integer boundary, we might as well capture everything we can and take on microseconds as well.  There are plenty of helpers on the time, tztime, and delta classes so you never have to see/manipulate the huge microsecond numbers yourself.





Release v\ |version|. (:ref:`Installation <install>`)

Requests is an :ref:`ISC Licensed <isc>` HTTP library, written in Python, for human beings.

Python's standard **urllib2** module provides most of
the HTTP capabilities you need, but the API is thoroughly **broken**.
It was built for a different time — and a different web. It requires an *enormous* amount of work (even method overrides) to perform the simplest of tasks.


See `the same code, without Requests <https://gist.github.com/973705>`_.

Requests takes all of the work out of Python HTTP/1.1 — making your integration with web services seamless. There's no need to manually add query strings to your URLs, or to form-encode your POST data. Keep-alive and HTTP connection pooling are 100%  automatic, powered by `urllib3 <https://github.com/shazow/urllib3>`_, which is embedded within Requests.


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


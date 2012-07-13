sanetime
========

**a sane date/time python interface**

**sanetime** was written to DRY up all the common date/time manipulations we all do constantly in our code while offering the most simple and intuitive client possible.

We've all learned that the only sane way to store times is using epoch time. (You have, haven't you?) 
Unfortunately, manipulating epoch time and timezones with the standard python toolset requires getting up to speed on a managerie of python modules and concepts: datetime, date, time, calendar, pytz, dateutils, timedelta, time tuples, localize, normalize.
**sanetime** seeks to bring a little more sanity ot the manipulations of epoch time, timezone, time delta, and time generally.

::

    >>> from sanetime import time,delta   # a tiny taste

    >>> time('2012-05-01 22:31',tz='America/New_York').millis  
    1335925860000

    >>> str(time(tz='Europe/London'))   # now in London
    '2012-05-29 15:28:05.178741 +Europe/London'

    >>> (time(2012,6,1) - time('2012-05-01')).hours
    744

    >>> (time() + delta(h=12)).s    # epoch seconds 12 hours from now
    1338344977


time
====
The ``time`` class represents a moment in time, internally stored as microseconds since epoch.  
A ``time`` object also has an associated timezone (UTC by default), however the timezone will never be considered during hashing, comparison or equality checks.  
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

User Guide
----------

Use these guides to quickly get up to speed on the classes and their methods.  They generally teach by example.

.. toctree::
   :maxdepth: 3

   user/time
   user/tztime
   user/delta
   user/span
   user/django


design principles
=================
* simple:  simplify usecases to single methods/properties
* intuitive: easy to remember methods/properties, with guessable aliases - be as verbose (and communicative) or as terse (and efficient) as you want to be.  for example  t = time();  t.ms == t.millis == t.milliseconds
* properties whenever sensible: properties are especially useful for django, cuz you can use them directly in templates without having to stage them first in the views.


FAQ
===
Why is everything stored internally as microseconds?

Python's datetime gives us access to microseconds, and since milliseconds would already have us cross the 32bit integer boundary, we might as well capture everything we can and take on microseconds as well.  There are plenty of helpers on the time, tztime, and delta classes so you never have to see/manipulate the huge microsecond numbers yourself unless you want to.


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


sanetime
========

**a sane date/time python interface**

**sanetime** was written to DRY up all the common date/time manipulations we all do constantly in our code while offering the most simple, versatile, and intuitive client possible.

We've all learned that the only sane way to store times is using epoch time. (You have, haven't you?) 
Unfortunately, manipulating epoch time and timezones with the standard python toolset requires getting up to speed on a managerie of python modules and concepts: datetime, date, time, calendar, pytz, dateutils, timedelta, time tuples, localize, normalize.

**sanetime** seeks to bring a more sanity to the manipulations of epoch time, timezone, time delta, and time generally.

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

overview
--------

time
""""
The :ref:`time` class represents a moment in time, internally stored as microseconds since epoch.  
A :ref:`time` object also has an associated timezone (UTC by default), however the timezone will never be considered during hashing, comparison or equality checks, i.e.  
A moment in :ref:`time` experienced in America/New_York is equal to the same moment in :ref:`time` experienced in Europe/Dublin.

tztime
""""""
The :ref:`tztime` class is exactly like the :ref:`time` object, except that timezone **does** factor into equality.  
A moment in `tztime` experienced in America/New_York is **not** the same as the same `tztime` moment experienced in Europe/Dublin.


delta
"""""
The :ref:`delta` class represents a period of time, and provides easy access to all the different ways you might slice and dice this: micros, millis, seconds, minutes, hours, mean_days, mean_weeks, mean_months, mean_years.  
There are also many different flavors of these: rounded, floored, floated, positional, rounded_positional.
There is no attempt made in delta yet to be calendar aware (hence the 'mean' prefixes in some cases).

span
""""
The :ref:`span` class represents a window of time ranging from one specific moment in time to another specific moment in time.  
You can think of it as a start :ref:`time` with a :ref:`delta`, or as a start :ref:`time` and a stop :ref:`time`.

django
""""""
A django model field is also provided: :ref:`SaneTimeField`, that makes it super simple to store a sanetime.
They honor the auto_add and auto_add_now features to easily turn your sanetimes into updated_at or created_at fields.
And they even work with south out of the box.

user guide
----------

Use these guides to quickly get up to speed on the classes, modules, and their methods.  They generally teach by example.

.. toctree::
   :maxdepth: 2

   user/time
   user/tztime
   user/delta
   user/span
   user/django

.. NOTE::
   This documentation is still a work in progress.  
   Lots of good docs are now in place here, but there are still features lying in the code waiting documentation.  
   As always, the code should be treated as the ultimate source of truth.  
   If you haven't found what you're looking for you, you may very well find it implemented in the code.  
   Please feel free to help us bring it to the surface in the docs.




design principles
-----------------
* simple:  simplify usecases to single method/property
* intuitive: easy to remember methods/properties, with guessable aliases - be as verbose (and communicative) or as terse (and efficient) as you want to be.  for example  t = time();  t.ms == t.millis == t.milliseconds
* properties whenever sensible: properties are especially useful for django, cuz you can use them directly in templates without having to stage them first in the views.


faq
---
Why is everything stored internally as microseconds?

Python's datetime gives us access to microseconds, and since milliseconds would already have us cross the 32bit integer boundary, we might as well capture everything we can and take on microseconds as well.
There are plenty of helpers on the time, tztime, and delta that make using epoch seconds or milis just as easy as using micros.


api documentation
-----------------

If you are looking for information on a specific function, class or method,
this part of the documentation is for you.

.. toctree::
   :maxdepth: 2

   api



.. _time:

time
====

The ``time`` class represents a moment in time, internally stored as microseconds since epoch.  
A ``time`` object also has an associated timezone (UTC by default), however the timezone will never be considered during hashing, comparison or equality checks, i.e.  
A moment in ``time`` experienced in America/New_York is equal to the same moment in ``time`` experienced in Europe/Dublin.

::

    >>> from sanetime import time

construction
------------

You can construct a sanetime object from epoch times, datetimes, date/time parts, or from a parseable string.

Epoch microseconds are assumed when no keyword is given.
Intuitive aliases exists for kwargs, be as terse or verbose as you want (us = micros = epoch_micros = epoch_microseconds):

::

    >>> time(1338508800000000)
    SaneTime(1338508800000000,<UTC>)

    >>> time(micros=1338508800000000)
    SaneTime(1338508800000000,<UTC>)

    >>> time(millis=1338508800000)
    SaneTime(1338508800000000,<UTC>)

    >>> time(seconds=1338508800)
    SaneTime(1338508800000000,<UTC>)

    >>> time(minutes=22308480, tz='America/New_York')
    SaneTime(1338508800000000,<DstTzInfo 'America/New_York' EST-1 day, 19:00:00 STD>)


If you have the calendar parameters, then construct just as you would a datetime:

::

    >>> time(2012,1,1)
    SaneTime(1325376000000000,<UTC>)

    >>> time(2012,1,1,12,30,1)
    SaneTime(1325421001000000,<UTC>)

    >>> time(2012,1,1,12,30,1,1, tz='America/New_York')
    SaneTime(1325421001000001,<DstTzInfo 'America/New_York' EST-1 day, 19:00:00 STD>)
    

If you already have a datetime object, just construct from that:

::

    >>> dt = datetime(2012,1,1)
    >>> time(dt)
    SaneTime(1325376000000000,<UTC>)


Or construct from a parsable string:

::

    >>> time('January 1st, 2012 12:30:01pm')
    SaneTime(1325421001000000,<UTC>)

    >>> time('January 1st, 2012 12:30:01pm', tz='America/New_York')
    SaneTime(1325421001000000,<DstTzInfo 'America/New_York' EST-1 day, 19:00:00 STD>)


arithmetic
----------

Adding any int/long assumes it to be in microseconds.  You can also add any :ref:`delta`:

::  

    >>> time(2012,1,1) + 5
    SaneTime(1325376000000005,<UTC>)

    >>> time(2012,1,1) + delta(hours=5)
    SaneTime(1325394000000000,<UTC>)


Subtracting two sanetimes produces a :ref:`delta`:

::

    >>> time() - time(2012,1,1)  # time since new year
    SaneDelta(15131339063956)
    
    >>> abs(time() - time()).micros  # microseconds to construct a time
    30


conversion
----------

You can easily convert to a timezone-aware datetime or to a naive datetime.  They are accessed as properties.

::

    >>> time(2012,1,1,tz='America/Los_Angeles').datetime
    datetime.datetime(2012, 1, 1, 0, 0, tzinfo=<DstTzInfo 'America/Los_Angeles' PST-1 day, 16:00:00 STD>)

    >>> time(2012,1,1,tz='America/Los_Angeles').naive_datetime
    datetime.datetime(2012, 1, 1, 0, 0)


There are other convenience datetime timezone conversions as well.

::

    >>> time(2012,1,1,tz='America/Los_Angeles').utc_datetime
    datetime.datetime(2012, 1, 1, 8, 0, tzinfo=<UTC>)

    >>> time(2012,1,1,tz='America/Los_Angeles').utc_naive_datetime
    datetime.datetime(2012, 1, 1, 8, 0)

    >>> time(2012,1,1,tz='America/Los_Angeles').ny_datetime
    datetime.datetime(2012, 1, 1, 3, 0, tzinfo=<DstTzInfo 'America/New_York' EST-1 day, 19:00:00 STD>)

    >>> time(2012,1,1,tz='America/Los_Angeles').ny_naive_datetime
    datetime.datetime(2012, 1, 1, 3, 0)


To epoch times:

::

    >>> time(2012,1,1).minutes
    22089600

    >>> time(2012,1,1).seconds
    1325376000

    >>> time(2012,1,1).millis
    1325376000000

    >>> time(2012,1,1).micros
    1325376000000000

long and int conversion just bring back the epoch microseconds

:: 

    >>> int(time(2012,1,1))
    1325376000000000

    >>> long(time(2012,1,1))
    1325376000000000L


date/time parts
---------------

You can get at any of the date parts just as you might with datetime properties.  Be careful-- these properties are all singular.  Do not confuse with the plural epoch possiblities of the previous section.  (this ambiguity will be fixed in future versions)

::

    >>> time().year
    2012
    >>> time().month
    6
    >>> time().day
    24
    >>> time().hour
    3
    >>> time().minute
    42
    >>> time().second
    12
    >>> time().micro
    664819



.. _time:

####
time
####

::

    >>> from sanetime import time

construction
============

epoch times
^^^^^^^^^^^

Construct directly from epoch times (us,ms,s,m).  Microseconds are assumed when no keyword is given.
Intuitive aliases exist if you want to be more verbose, for example: us = micros = epoch_micros = epoch_microseconds

::

    >>> time(1338508800000000)
    SaneTime(1338508800000000,<UTC>)

    >>> time(us=1338508800000000)
    SaneTime(1338508800000000,<UTC>)

    >>> time(ms=1338508800000)
    SaneTime(1338508800000000,<UTC>)

    >>> time(s=1338508800)
    SaneTime(1338508800000000,<UTC>)

    >>> time(epoch_seconds=1338508800)
    SaneTime(1338508800000000,<UTC>)

    >>> time(epoch_minutes=22308480, tz='America/New_York')
    SaneTime(1338508800000000,<DstTzInfo 'America/New_York' EST-1 day, 19:00:00 STD>)

datetime parts
^^^^^^^^^^^^^^

If you have the calendar parameters, then construct just as you would a datetime

::

    >>> time(2012,1,1)
    SaneTime(1325376000000000,<UTC>)

    >>> time(2012,1,1,12)
    SaneTime(1325419200000000,<UTC>)

    >>> time(2012,1,1,12,30)
    SaneTime(1325421000000000,<UTC>)

    >>> time(2012,1,1,12,30,1)
    SaneTime(1325421001000000,<UTC>)

    >>> time(2012,1,1,12,30,1,1, tz='America/New_York')
    SaneTime(1325421001000001,<DstTzInfo 'America/New_York' EST-1 day, 19:00:00 STD>)
    
datetime
^^^^^^^^

Or if you already have a datetime object, just construct from that

::

    >>> dt = datetime(2012,1,1)
    >>> time(dt)
    SaneTime(1325376000000000,<UTC>)

string
^^^^^^

Or construct from a parsable string

::

    >>> time('January 1st, 2012 12:30:01pm')
    SaneTime(1325421001000000,<UTC>)

    >>> time('January 1st, 2012 12:30:01pm', tz='America/New_York')
    SaneTime(1325421001000000,<DstTzInfo 'America/New_York' EST-1 day, 19:00:00 STD>)


arithmetic
==========

addition
^^^^^^^^

Adding any int/long assumes it to be in microseconds.  You can also add any delta.

::  

    >>> time(2012,1,1) + 5
    SaneTime(1325376000000005,<UTC>)


difference
^^^^^^^^^^

Subtracing two sanetimes produces a delta!

::

    >>> time() - time()  # benchmarking time construction
    SaneDelta(-30)

    >>> time() - time(2012,1,1)  # time since new year
    SaneDelta(15131339063956)
    

conversion
==========

The constructor can convert from a number of different formats.  Here we describe all the different things you convert **to**.

to datetime
^^^^^^^^^^^

You can convert to a timezone-aware datetime or to a naive datetime.  They are accessed as properties.

::

    >>> time(2012,1,1,tz='America/Los_Angeles').datetime
    datetime.datetime(2012, 1, 1, 0, 0, tzinfo=<DstTzInfo 'America/Los_Angeles' PST-1 day, 16:00:00 STD>)

    >>> time(2012,1,1,tz='America/Los_Angeles').naive_datetime
    datetime.datetime(2012, 1, 1, 0, 0)

There are convenience datetime timezone conversions as well.  These can

::

    >>> time(2012,1,1,tz='America/Los_Angeles').utc_datetime
    datetime.datetime(2012, 1, 1, 8, 0, tzinfo=<UTC>)

    >>> time(2012,1,1,tz='America/Los_Angeles').utc_naive_datetime
    datetime.datetime(2012, 1, 1, 8, 0)

    >>> time(2012,1,1,tz='America/Los_Angeles').ny_datetime
    datetime.datetime(2012, 1, 1, 3, 0, tzinfo=<DstTzInfo 'America/New_York' EST-1 day, 19:00:00 STD>)

    >>> time(2012,1,1,tz='America/Los_Angeles').ny_naive_datetime
    datetime.datetime(2012, 1, 1, 3, 0)


to epoch times
^^^^^^^^^^^^^^

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
===============

You can get at any of the date parts just as you might with datetime properties.  Be careful-- these properties are all singular.  Do not confuse with the plural epoch possiblities of the previous section.

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
    >>> time().microsecond
    664819



---
title: "sanetime:  a sane date/time python interface"
---

#sanetime

**A sane date/time python interface**

better epoch time, timezones, and deltas, django support as well

##intro

**sanetime** was written to DRY up all the common date/time manipulations we all do constantly in our code while offering the most simple, versatile, and intuitive client possible.

We've all learned that the only sane way to store times is using epoch time. (You have, haven't you?) 
Unfortunately, manipulating epoch time and timezones with the standard python toolset requires getting up to speed on a managerie of python modules and concepts: datetime, date, time, calendar, pytz, dateutils, timedelta, time tuples, localize, normalize.

**sanetime** seeks to bring a more sanity to the manipulations of epoch time, timezone, time delta, and time generally.

~~~ python
>>> from sanetime import time,delta   # a tiny taste

>>> time('2012-05-01 22:31',tz='America/New_York').millis
1335925860000

>>> str(time(tz='Europe/London'))   # now in London
'2012-05-29 15:28:05.178741 +Europe/London'

>>> (time(2012,6,1) - time('2012-05-01')).hours
744

>>> (time() + delta(h=12)).s    # epoch seconds 12 hours from now
1338344977
~~~


##time

###concept

The `time` class represents a moment in time, internally stored as microseconds since epoch.  
A `time` object also has an associated timezone (UTC by default), however the timezone will never be considered during hashing, comparison or equality checks, i.e.  
A moment in `time` experienced in America/New\_York is equal to the same moment in `time` experienced in Europe/Dublin.

###methods

####construction

You can construct a sanetime object from epoch times, datetimes, date/time parts, or from a parseable string.

Epoch microseconds are assumed when no keyword is given.
Intuitive aliases exists for kwargs, be as terse or verbose as you want (us = micros = epoch_micros = epoch_microseconds):

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

    >>> time(2012,1,1)
    SaneTime(1325376000000000,<UTC>)

    >>> time(2012,1,1,12,30,1)
    SaneTime(1325421001000000,<UTC>)

    >>> time(2012,1,1,12,30,1,1, tz='America/New_York')
    SaneTime(1325421001000001,<DstTzInfo 'America/New_York' EST-1 day, 19:00:00 STD>)
    

If you already have a datetime object, just construct from that:

    >>> dt = datetime(2012,1,1)
    >>> time(dt)
    SaneTime(1325376000000000,<UTC>)


Or construct from a parsable string:

    >>> time('January 1st, 2012 12:30:01pm')
    SaneTime(1325421001000000,<UTC>)

    >>> time('January 1st, 2012 12:30:01pm', tz='America/New_York')
    SaneTime(1325421001000000,<DstTzInfo 'America/New_York' EST-1 day, 19:00:00 STD>)


####arithmetic

Adding any int/long assumes it to be in microseconds.  You can also add any :ref:`delta`:

    >>> time(2012,1,1) + 5
    SaneTime(1325376000000005,<UTC>)

    >>> time(2012,1,1) + delta(hours=5)
    SaneTime(1325394000000000,<UTC>)


Subtracting two sanetimes produces a :ref:`delta`:

    >>> time() - time(2012,1,1)  # time since new year
    SaneDelta(15131339063956)

    >>> abs(time() - time()).micros  # microseconds to construct a time
    30


####conversion

You can easily convert to a timezone-aware datetime or to a naive datetime.  They are accessed as properties.

    >>> time(2012,1,1,tz='America/Los_Angeles').datetime
    datetime.datetime(2012, 1, 1, 0, 0, tzinfo=<DstTzInfo 'America/Los_Angeles' PST-1 day, 16:00:00 STD>)

    >>> time(2012,1,1,tz='America/Los_Angeles').naive_datetime
    datetime.datetime(2012, 1, 1, 0, 0)


There are other convenience datetime timezone conversions as well.

    >>> time(2012,1,1,tz='America/Los_Angeles').utc_datetime
    datetime.datetime(2012, 1, 1, 8, 0, tzinfo=<UTC>)
    
    >>> time(2012,1,1,tz='America/Los_Angeles').utc_naive_datetime
    datetime.datetime(2012, 1, 1, 8, 0)

    >>> time(2012,1,1,tz='America/Los_Angeles').ny_datetime
    datetime.datetime(2012, 1, 1, 3, 0, tzinfo=<DstTzInfo 'America/New_York' EST-1 day, 19:00:00 STD>)

    >>> time(2012,1,1,tz='America/Los_Angeles').ny_naive_datetime
    datetime.datetime(2012, 1, 1, 3, 0)


To epoch times:

    >>> time(2012,1,1).minutes
    22089600

    >>> time(2012,1,1).seconds
    1325376000

    >>> time(2012,1,1).millis
    1325376000000

    >>> time(2012,1,1).micros
    1325376000000000


long and int conversion just bring back the epoch microseconds

    >>> int(time(2012,1,1))
    1325376000000000

    >>> long(time(2012,1,1))
    1325376000000000L


#####date/time parts

You can get at any of the date parts just as you might with datetime properties.  Be careful-- these properties are all singular.  Do not confuse with the plural epoch possiblities of the previous section.  (this ambiguity will be fixed in future versions)

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


###tztime
The `tztime` class is exactly like the `time` object, except that timezone **does** factor into equality.  
A moment in `tztime` experienced in America/New\_York is **not** the same as the same `tztime` moment experienced in Europe/Dublin.

###delta
The `delta` class represents a period of time, and provides easy access to all the different ways you might slice and dice this: micros, millis, seconds, minutes, hours, mean\_days, mean\_weeks, mean\_months, mean\_years.  
There are also many different flavors of these: rounded, floored, floated, positional, rounded\_positional.
There is no attempt made in delta yet to be calendar aware (hence the 'mean' prefixes in some cases).

###span
The `span` class represents a window of time ranging from one specific moment in time to another specific moment in time.  
You can think of it as a start `time` with a `delta`, or as a start `time` and a stop `time`.

###django
A django model field is also provided: `SaneTimeField`, that makes it super simple to store a sanetime.
They honor the auto\_add and auto\_add\_now features to easily turn your sanetimes into updated\_at or created\_at fields.
And they even work with south out of the box.


###NOTE
This documentation is still a work in progress.  
Lots of good docs are now in place here, but there are still features lying in the code waiting documentation.  
As always, the code should be treated as the ultimate source of truth.  
If you haven't found what you're looking for you, you may very well find it implemented in the code.  
Please feel free to help us bring it to the surface in the docs.



###design principles
* simple: simplify usecases to single method/property
* intuitive: easy to remember methods/properties, with guessable aliases - be as verbose (and communicative) or as terse (and efficient) as you want to be.  for example  t = time();  t.ms == t.millis == t.milliseconds
* properties whenever sensible: properties are especially useful for django, cuz you can use them directly in templates without having to stage them first in the views.


###FAQ
Why is everything stored internally as microseconds?

Python's datetime gives us access to microseconds, and since milliseconds would already have us cross the 32bit integer boundary, we might as well capture everything we can and take on microseconds as well.
There are plenty of helpers on the time, tztime, and delta that make using epoch seconds or milis just as easy as using micros.




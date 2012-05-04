sanetime & sanetztime
=======================

Sane wrappers around the python's datetime / time / date / timetuple / pytz / timezone / calendar /
timedelta / utc shitshow.  This takes care of most of the ridiculous shit so you don't have to
flush precious brain cells down the toilet trying to figure all this out.  You owe me a beer.  At
least.

There are two classes that you may find useful here, and you should understand the difference:

* sanetime:  this class is only concerned with a particular moment in time, NOT where that moment
        was experienced.
* sanetztime:  this class is concerned with a particular moment in time AND in what timezone that
        moment was experienced.


main source and docs:
https://github.com/prior/sanetime
 

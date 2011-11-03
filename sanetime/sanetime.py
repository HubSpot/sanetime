import calendar as shit_calendar
from datetime import datetime as fucked_datetime
from dateutil import parser as crap_parser
from error import SaneTimeError
import pytz
import re
from numbers import Number

"""
Sane wrappers around the python's datetime / time / date / timetuple / pytz / timezone / calendar /
timedelta / utc shitshow.  This takes care of most of the ridiculous shit so you don't have to
flush precious brain cells down the toilet trying to figure all this out.  You owe me a beer.  At
least.

There are two classes that you mind find useful here, and you should understand the difference:

* sanetime:  this class is only concerned with a particular moment in time, NOT where that moment
        was experienced.
* sanetztime:  this class is concerned with a particular moment in time AND in what timezone that
        moment was experienced.
"""

class sanetime(object):
    """
    sanetime is only concerned with a particular moment in time.  It does not concern itself with
    timezones.  Its constructor will do its best to turn timezoned times into a utc time, and
    operate forever more on this representation.  It stores microseconds since the epoch.  If you
    need to convert to a timezoned representation there are a few methods to do that.
    
    Why not store in millis or seconds?
    datetime stores things in micros, and since millis already crosses over the 32bit boundary, we
    might as well store everything we got in the 64 bit numbers.  This will force 32bit machines to
    go to long's, so maybe a little reduced performance there, but isn't everything on 64 bit now?
    This also avoids the unexpected scenario where two different datetimes would compare as equal
    when they were converted to sanetimes.  As to why-not-seconds, well that's just lame.  You can
    easily go to seconds or millis from sanetime by using the .s or .ms properties.

    When you do arithmetic with sanetime you are operating on microseconds.  st + 1 creates a new
    sanetime that is 1 microsecond in the future from the st sanetime.

    When you do comparisons, all comparisons are happening at the microsecond level.  You are
    comparing microseconds in time.

    On initialization, we use any hints available to determine what that moment in time is,
    including timezone information.  You can include tz as a hint to declare what timezone a time
    is in, but that information will not be kept around- it is only used to convert the given time
    into utc, and then it is purposefully dropped.  If you need to maintain a relationship to the
    timezones then look at sanetztime.
    """

    STR_NATIVE_FORMAT = re.compile(r'^(\d+)([um]?s)$')

    def __init__(self, *args, **kwargs):
        """
        acceptable unkeyworded inputs:
          1) an int/long in utc micros
          2) a datetime
            NOTE!! a naive datetime is assumed to be in UTC, unless you tell this
            method otherwise by also passing in a tz paramter.  A timezoned datetime is 
            preserved with the timezone it has
          3) a string representation that the crap parser can deal with
          4) a string representation of the form /d+us or /d+ms or /d+s
          4) multiple args just as datetime would accept

        acceptable keyworded inputs:
          1) us = an int/long in utc micros
          2) ms = an int/long in utc millis
          3) s = an int/long in utc seconds
          4) tz = a timezone (either a pytz timezone object, a recognizeable pytz timezone string, or a dateutil tz object)
        """
        super(sanetime,self).__init__()
        uss = []
        tzs = []
        naive_dt = None

        args = list(args)
        if len(args)>2 and len(args)<8:
            args = [fucked_datetime(*args)]
        if len(args)==1:
            arg = args.pop()
            if type(arg) in [long,int,float,sanetime]:
                uss.append(int(arg))
            elif isinstance(arg, basestring):
                arg = arg.strip()
                native_format_match = self.__class__.STR_NATIVE_FORMAT.match(arg)
                if native_format_match:
                    kwargs[native_format_match.group(2)] = native_format_match.group(1)
                else:
                    arg = crap_parser.parse(arg)
                    if arg.tzinfo:  # parsed timezones are a special breed of retard
                        arg = arg.astimezone(pytz.utc).replace(tzinfo=None)
                        tzs.append('UTC') # don't allow for a tz specificaion on top of a timezoned datetime str  -- that is opening a whole extra can of confusion -- so force the timezone here so that another tz specification will cause an error
            if type(arg) == fucked_datetime:
                naive_dt = arg
                if naive_dt.tzinfo:
                    tzs.append(naive_dt.tzinfo)
                    naive_dt = naive_dt.replace(tzinfo=None)

        if kwargs.get('us'):
            uss.append(int(kwargs.pop('us')))
        if kwargs.get('ms'):
            uss.append(int(kwargs.pop('ms'))*1000)
        if kwargs.get('s'):
            uss.append(int(kwargs.pop('s'))*1000**2)

        if kwargs.get('tz'):
            tzs.append(kwargs.pop('tz'))


        # now we have enough info to figure out the tz:
        self._set_tz(tzs and tzs[0] or 'UTC')

        # and now that we've figured out tz, we can fully deconstruct the dt
        if naive_dt:
            dt = self._tz.localize(naive_dt).astimezone(pytz.utc)
            uss.append(shit_calendar.timegm(dt.timetuple())*1000**2+dt.microsecond)

        # if we got nothing yet for micros, then make it now
        if len(uss)==0:
            dt = fucked_datetime.utcnow()
            uss.append(shit_calendar.timegm(dt.timetuple())*1000**2+dt.microsecond)

        self.us = uss[0]
        
        if len(tzs)>1 or len(uss)>1 or len(args)>0:
            raise SaneTimeError('Unexpected constructor arguments')

    def to_datetime(self):
        return self.to_utc_datetime()

    def to_utc_datetime(self): 
        dt = fucked_datetime.utcfromtimestamp(self.us/10**6)
        dt = pytz.utc.localize(dt)
        dt = dt.replace(microsecond = self.us%10**6)
        return dt

    def to_naive_datetime(self): 
        return self.to_datetime().replace(tzinfo=None)

    def to_naive_utc_datetime(self): 
        return self.to_utc_datetime().replace(tzinfo=None)

    def strftime(self, *args, **kwargs):
        return self.to_datetime().strftime(*args, **kwargs)

    def __lt__(self, other):
        if not isinstance(other, sanetime):
            other = sanetime(other)
        return self.us < other.us
    def __le__(self, other):
        if not isinstance(other, sanetime):
            other = sanetime(other)
        return self.us <= other.us
    def __gt__(self, other):
        if not isinstance(other, sanetime):
            other = sanetime(other)
        return self.us > other.us
    def __ge__(self, other):
        if not isinstance(other, sanetime):
            other = sanetime(other)
        return self.us >= other.us
    def __eq__(self, other):
        if not isinstance(other, sanetime):
            other = sanetime(other)
        return self.us == int(other)

    def __ne__(self, other):
        if not isinstance(other, sanetime):
            other = sanetime(other)
        return self.us != other.us

    def __hash__(self):
        return self.us.__hash__()

    def __add__(self, operand):
        if not isinstance(operand, Number):
            raise SaneTimeError('Can only add/sub microseconds (expecting a number)')
        return sanetime(self.us + int(operand))
    def __sub__(self, operand):
        if isinstance(operand, sanetime):
            return self.us - operand.us
        return self.__add__(-operand)
    def __int__(self):
        return self.us
    def __long__(self):
        return long(self.us)

    def __repr_naive__(self):
        dt = self.to_naive_datetime()
        return "%04d-%02d-%02d %02d:%02d:%02d.%06d" % (
                dt.year,
                dt.month,
                dt.day,
                dt.hour,
                dt.minute,
                dt.second,
                dt.microsecond)
        return str(self.to_datetime())

    def __repr__(self):
        return self.__repr_naive__() + ' UTC'

    def __str__(self):
        return '%sus' % self.us
    
    def _get_s(self):
        return (self.us+500*1000)/10**6
    s = property(_get_s)

    def _get_ms(self):
        return (self.us+500)/1000
    ms = property(_get_ms)

    def _set_tz(self, tz):
        if type(tz) in (str, unicode):
            tz = pytz.timezone(tz)
        self._tz = tz
        return self



    def ago(self):
        """
        Get a datetime object or a int() Epoch timestamp and return a
        pretty string like 'an hour ago', 'Yesterday', '3 months ago',
        'just now', etc

        copied from http://stackoverflow.com/questions/1551382/python-user-friendly-time-format
        and then tweaked
        """
        micro_delta = sanetime().us - self.us
        second_delta = (micro_delta+500*1000)/1000**2
        day_delta = (micro_delta+1000**2*60**2*12)/(1000**2*60**2*24)

        if micro_delta < 0:
            # TODO: implement future times
            return ''

        if day_delta == 0:
            if second_delta < 10:
                return "just now"
            if second_delta < 30:
                return "%s seconds ago" % second_delta
            if second_delta < 90:
                return "a minute ago"
            if second_delta < 30*60:
                return "%s minutes ago" % ((second_delta+30)/60)
            if second_delta < 90*60:
                return "an hour ago"
            return "%s hours ago" % ((second_delta+30*60)/60**2)
        if day_delta < 2:
            return "yesterday"
        if day_delta < 7:
            return "%s days ago" % day_delta
        if day_delta < 11:
            return "a week ago" % day_delta
        if day_delta < 45:
            return "%s weeks ago" % ((day_delta+3)/7)
        if day_delta < 400:
            return "%s months ago" % ((day_delta+15)/30)
        return "%s years ago" % ((day_delta+182)/365)



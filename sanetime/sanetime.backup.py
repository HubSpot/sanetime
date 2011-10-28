import calendar as shit_calendar
from datetime import datetime as fucked_datetime
from dateutil import parser as crap_parser
from dateutil import tz as dumb_tz
from error import SaneTimeError
import pytz


# keeping lowercase so we can mimic datetime as much as is reasonable
class sanetztime(sanetztime):
    """
    A sane wrapper around the python
    datetime/time/date/timetuple/pytz/timezone/calendar/timedelta/utc shitshow

    This takes care of the ridiculous shit so you don't have to.

    All of these times are stored in micros, and are forced to have an associated timezone (though the association isn't necessarily relevant sometimes depending on what you're doing)

    Think of this object as being divided into two layers, a backend and a
    frontend.  The backend only cares about a moment in time.  It has no
    concern about where that moment in time was.  Then there is a front-end
    layer that allows you to paint that time as being in a certain timezone.
    But all the core funtionality only cares about the moment in time, not the
    place.  On initialization, we use any hints available to determine what
    that moment in time is, and we'll keep any determined timezone kicking
    around, but when you deal with equality, or hashing, or any core
    functionality-- it will always be against the moment in time, not against
    where that moment in time occured.
    """
    def set_tz(self, tz):
        if type(tz) in (str, unicode):
            tz = pytz.timezone(tz)
        self.tz = tz
        return self

    def with_tz(self, tz):
        return sanetime(self.us, tz=tz)

    def __



class sanetime(object):
    """
    A sane wrapper around the python
    datetime/time/date/timetuple/pytz/timezone/calendar/timedelta/utc shitshow

    This takes care of the ridiculous shit so you don't have to.

    All of these times are stored in utc micros, and are forced to have an associated timezone (though the association isn't necessarily relevant sometimes depending on what you're doing)

    Think of this object as being divided into two layers, a backend and a
    frontend.  The backend only cares about a moment in time.  It has no
    concern about where that moment in time was.  Then there is a front-end
    layer that allows you to paint that time as being in a certain timezone.
    But all the core funtionality only cares about the moment in time, not the
    place.  On initialization, we use any hints available to determine what
    that moment in time is, and we'll keep any determined timezone kicking
    around, but when you deal with equality, or hashing, or any core
    functionality-- it will always be against the moment in time, not against
    where that moment in time occured.
    """

    def __init__(self, *args, **kwargs):
        """
        acceptable unkeyworded inputs:
          1) an int/long in utc micros
          2) a datetime
            NOTE!! a naive datetime is assumed to be in UTC, unless you tell this
            method otherwise by also passing in a tz paramter.  A timezoned datetime is 
            preserved with the timezone it has
          3) a string representation that the crap parser can deal with
          4) multiple args just as datetime would accept

        acceptable keyworded inputs:
          1) us = an int/long in utc micros
          2) ms = an int/long in utc millis
          3) s = an int/long in utc seconds
          4) tz = a timezone (either a sanetime timezone object, a pytz timezone object, or a recognizeable timezone string)
        """
        super(sanetime,self).__init__()
        uss = []
        tzs = []
        naive_dt = None

        if kwargs.get('us'):
            uss.append(int(kwargs.pop('us')))
        if kwargs.get('ms'):
            uss.append(int(kwargs.pop('ms'))*1000)
        if kwargs.get('s'):
            uss.append(int(kwargs.pop('s'))*1000**2)

        if kwargs.get('tz'):
            tzs.append(kwargs.pop('tz'))

        args = list(args)
        if len(args)>2 and len(args)<8:
            args = [fucked_datetime(*args)]
        if len(args)==1:
            arg = args.pop()
            if type(arg) in [long,int,float]:
                uss.append(int(arg))
            elif type(arg) in [str,unicode]:
                arg = crap_parser.parse(arg)
                if arg.tzinfo:  # parsed timezones are a special breed of retard
                    arg = arg.astimezone(pytz.utc).replace(tzinfo=None)
                    tzs.append('UTC') # don't allow for a tz specificaion on top of a timezoned datetime str  -- that is opening a whole extra can of confusion
            if type(arg) == fucked_datetime:
                naive_dt = arg
                if naive_dt.tzinfo:
                    tzs.append(naive_dt.tzinfo)
                    naive_dt = naive_dt.replace(tzinfo=None)

        # now we have enough info to figure out the tz:
        self.set_tz(tzs and tzs[0] or 'UTC')

        # and now that we've figured out tz, we can fully deconstruct the dt
        if naive_dt:
            dt = self.tz.localize(naive_dt).astimezone(pytz.utc)
            uss.append(shit_calendar.timegm(dt.timetuple())*1000**2+dt.microsecond)

        # if we got nothing yet for micros, then make it now
        if len(uss)==0:
            dt = fucked_datetime.utcnow()
            uss.append(shit_calendar.timegm(dt.timetuple())*1000**2+dt.microsecond)

        self.us = uss[0]
        
        if len(tzs)>1 or len(uss)>1 or len(args)>0:
            raise SaneTimeError('Unexpected constructor arguments')


    def to_datetime(self):
        dt = fucked_datetime.utcfromtimestamp(self.us/10**6)
        dt = pytz.utc.localize(dt)
        dt = dt.replace(microsecond = self.us%10**6)
        dt = dt.astimezone(self.tz)
        return dt

    def to_naive_datetime(self): 
        return self.to_datetime().replace(tzinfo=None)

    def to_naive_utc_datetime(self): 
        return self.with_tz(pytz.utc).to_naive_datetime()

    def strftime(self, *args, **kwargs):
        return self.to_datetime().strftime(*args, **kwargs)

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


    def __lt__(self, other):
        return self.us < other.us
    def __le__(self, other):
        return self.us <= other.us
    def __gt__(self, other):
        return self.us > other.us
    def __ge__(self, other):
        return self.us >= other.us
    def __eq__(self, other):
        return self.us == other.us
    def __ne__(self, other):
        return self.us != other.us

    def __hash__(self):
        return self.us.__hash__()
    def __cmp__(self, other):
        return self.us.__cmp__(other.us)

    def __add__(self, extra_us):
        if type(extra_us) not in (int,long,float):
            raise SaneTimeError('Can only add microseconds')
        return sanetime(self.us + extra_us, tz=self.tz)
    def __sub__(self, extra_us):
        return self.__add__(-extra_us)

    def __repr__(self):
        dt = self.to_naive_datetime()
        return "%04d-%02d-%02d %02d:%02d:%02d.%06d %s" % (
                dt.year,
                dt.month,
                dt.day,
                dt.hour,
                dt.minute,
                dt.second,
                dt.microsecond,
                self.tz_name)
        return str(self.to_datetime())

    def __str__(self):
        return str(self.us)
    
    def _get_tz_name(self):
        return self.tz.zone

    def _get_tz_abbr(self):
        return self.tz._tzname
    tz_name = property(_get_tz_name)
    tz_abbr = property(_get_tz_abbr)
    
    def _get_s(self):
        return (self.us+500*1000)/10**6
    def _get_ms(self):
        return (self.us+500)/1000
    s = property(_get_s)
    ms = property(_get_ms)



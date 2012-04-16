import calendar as shit_calendar
from datetime import datetime as fucked_datetime
from dateutil import parser as crap_parser
from error import Error
from .sanedelta import SaneDelta
import pytz
import re


#TODO: ensure that this is immutable, and that addiiton,etc always producesa  new object!!!
 
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

class SaneTime(object):

    @classmethod
    def utc_datetime_to_us(kls, dt):
        return shit_calendar.timegm(dt.timetuple())*1000**2+dt.microsecond

    @classmethod
    def us_to_utc_datetime(kls, us):
        return pytz.utc.localize(fucked_datetime.utcfromtimestamp(us/10**6)).replace(microsecond = us%10**6)

    @classmethod
    def to_timezone(kls, tz):
        if not isinstance(tz, basestring): return tz
        return pytz.timezone(tz)


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

    def __init__(self, *args, **kwargs):
        """
        acceptable arg inputs:
          1) epoch micros integer (or int like)
          2) a datetime
            NOTE!! a naive datetime is assumed to be in UTC, unless you tell this
            method otherwise by also passing in a tz paramter.  A timezoned datetime is 
            preserved with the timezone it has
          3) a string representation that the dateutil parser can deal with
          4) multiple args just as datetime would accept

        acceptable keyworded inputs:
          1) us = an int/long in epoch micros
          2) ms = an int/long in epoch millis
          3) s = an int/long in epoch seconds
          4) tz = a timezone (either a pytz timezone object, a recognizeable pytz timezone string, or a dateutil tz object)
        """
        super(SaneTime,self).__init__()
        uss = []
        tzs = []
        naive_dt = None

        if len(kwargs):
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
        if len(args)==2:
            tzs.append(args.pop())
        if len(args)==1:
            arg = args.pop()
            if hasattr(arg,'__int__'):
                uss.append(int(arg))
            elif isinstance(arg, basestring):
                arg = arg.strip()
                arg = crap_parser.parse(arg)
                if arg.tzinfo:  # parsed timezones are a special breed of retard
                    naive_dt = arg.astimezone(pytz.utc).replace(tzinfo=None)
                    tzs.append('UTC') # don't allow for a tz specificaion on top of a timezoned datetime str  -- that is opening a whole extra can of confusion -- so force the timezone here so that another tz specification will cause an error
            elif type(arg) == fucked_datetime:
                naive_dt = arg
                if naive_dt.tzinfo:
                    tzs.append(naive_dt.tzinfo)
                    naive_dt = naive_dt.replace(tzinfo=None)

        if len(tzs)>1:
            raise Error("constructor arguments attempt to specify more than one timezone!  I can't possibly resolve that!  (timezones implied = %s)"%(tzs))

        # now we have enough info to figure out the tz:
        self._tz = SaneTime.to_timezone(tzs and tzs[0] or 'UTC')

        # and now that we've figured out tz, we can fully deconstruct the dt
        if naive_dt:
            uss.append(SaneTime.utc_datetime_to_us(self._tz.localize(naive_dt).astimezone(pytz.utc)))

        # if we got nothing yet for micros, then make it now
        if len(uss)==0:
            uss.append(SaneTime.utc_datetime_to_us(fucked_datetime.utcnow()))

        self._us = uss[0]
        
        if len(uss)>1 or len(args)>0 or len(kwargs):
            raise Error("constructor arguments don't make any sense")

        
    @property
    def us(self): return self._us


    def to_utc_datetime(self): return SaneTime.us_to_utc_datetime(self.us)
    def to_utc_naive_datetime(self): return self.to_utc_datetime().replace(tzinfo=None)
    def to_datetime(self): return self.to_utc_datetime()
    def to_naive_datetime(self): return self.to_utc_naive_datetime()
    def to_timezoned_datetime(self, tz): return self.to_utc_datetime().astimezone(SaneTime.to_timezone(tz))
    def to_timezoned_naive_datetime(self, tz): return self.to_timezoned_datetime(tz).replace(tzinfo=None)

    def clone(self): return sanetime(self._us)

    def strftime(self, *args, **kwargs): return self.to_datetime().strftime(*args, **kwargs)

    def __cmp__(self, other): return cmp(self._us, int(other))
    def __hash__(self): return self._us.__hash__()

    def __add__(self, operand): return SaneTime(self._us + int(operand))
    def __sub__(self, operand):
        if isinstance(operand, SaneTime): return SaneDelta(self.us - operand.us)
        return self.__add__(-int(operand))
    def __int__(self): return self._us
    def __long__(self): return long(self._us)

    def __repr__(self):
        return u"SaneTime(%s)" % self.us
    def __str__(self): return unicode(self).encode('utf-8')
    def __unicode__(self):
        dt = self.datetime
        micros = u".%06d"%dt.microsecond if dt.microsecond else ''
        time = u" %02d:%02d:%02d%s"%(dt.hour,dt.minute,dt.second,micros) if dt.microsecond or dt.second or dt.minute or dt.hour else ''
        return u"%04d-%02d-%02d%s UTC" % (dt.year, dt.month, dt.day, time)

    @property
    def ny_str(self): return self.ny_ndt.strftime('%I:%M:%S%p %m/%d/%Y')
    
    @property
    def s(self): return (self._us+500*1000)/10**6

    @property
    def ms(self): return (self._us+500)/1000

    @property
    def dt(self): return self.to_datetime()

    @property
    def ndt(self): return self.to_naive_datetime()

    @property
    def utc_dt(self): return self.to_utc_datetime()

    @property
    def utc_ndt(self): return self.to_utc_naive_datetime()
    
    @property
    def ny_dt(self): return self.to_timezoned_datetime('America/New_York')

    @property
    def ny_ndt(self): return self.to_timezoned_naive_datetime('America/New_York')




#primary gateways

sanetime = SaneTime
time = SaneTime

def nsanetime(*args, **kwargs): 
    if args:
        if args[0] is None: return None
    elif kwargs:
        if None in [v for k,v in kwargs.iteritems() if k!='tz']: return None
    return SaneTime(*args, **kwargs)

ntime = nsanetime

from .constants import MILLI_MICROS,SECOND_MICROS,MINUTE_MICROS
import calendar
from datetime import datetime
from dateutil import parser
from dateutil.tz import tzlocal
from .error import TimeConstructionError
from .sanedelta import SaneDelta
import pytz


#TODO: ensure that this is immutable, and that addiiton,etc always producesa  new object!!!
 
MICROS_TRANSLATIONS = (
        (('m','mins','minutes','epoch_mins','epoch_minutes'),MINUTE_MICROS),
        (('s','secs','seconds','epoch_secs','epoch_seconds'),SECOND_MICROS),
        (('ms','millis','milliseconds','epoch_millis','epoch_milliseconds'),MILLI_MICROS),
        (('us','micros','microseconds','epoch_micros','epoch_microseconds'),1) )
MICROS_TRANSLATION_HASH = dict((alt,v) for k,v in MICROS_TRANSLATIONS for alt in k)

class SaneTime(object):
    """
    A time stored in epoch microseconds, and optionally decorated with a timezone.
    An object of this class represents a moment in time.
    A moment in time experience in America/New_York is equal to the same moment in time experienced in Europe/Dublin
    """



    """
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
          4) m = an int/long in epoch minutes
          5) tz = a timezone (either a pytz timezone object, a recognizeable pytz timezone string, or a dateutil tz object)
        """
        super(time,self).__init__()
        uss = set()
        tzs = set()
        naive_dt = None
        avoid_localize = False

        for k,v in kwargs.iteritems():
            if k in ('tz','timezone'):
                tzs.add(SaneTime.to_timezone(v))
            elif k in MICROS_TRANSLATION_HASH:
                uss.add(MICROS_TRANSLATION_HASH[k]*v)
            else:
                raise TimeConstructionError("Unexpected kwarg in SaneTime constructor! (%s = %s)" % (k,v))

        args = list(args)
        if len(args)>2 and len(args)<=8:
            args = [datetime(*args)]
        if len(args)==2:
            tzs.add(SaneTime.to_timezone(args.pop()))
        if len(args)==1:
#            import pdb; pdb.set_trace()
            arg = args.pop()
            if hasattr(arg,'__int__'):
                uss.add(int(arg))
                if hasattr(arg,'tz'): tzs.add(arg.tz)
            elif isinstance(arg, basestring):
                parts = arg.strip().split(' ')
                if len(parts)>1 and parts[-1].startswith('+'):
                    try:
                        tzs.add(SaneTime.to_timezone(parts[-1][1:]))
                        arg = ' '.join(parts[:-1])
                    except: pass
                utc = arg.endswith('Z') or arg.endswith('+00:00')  # to deal with strange gunicorn issue -- doesn't want to use UTC time in these cases
                arg = parser.parse(arg)
                if arg.tzinfo:  # parsed timezones are a special breed of retard
                    if utc:  # put this in place to guard against wierd gunicorn issue -- gunicorn will attempt to force local timezone when there's an explicit UTC timezone associated! not sure where that's coming from.
                        tzs.add(pytz.utc)
                        arg = arg.replace(tzinfo=None)
                    elif isinstance(arg.tzinfo, tzlocal):  # in case the parser decides to use tzlocal instead of a tzoffset
                        arg = arg.replace(tzinfo=None)
                    else:
                        # can't rely on the dateutil parser for timezone stuff-- so we go back to UTC and force tz to be set in other ways
                        avoid_localize = True # but we'll still convert back to UTC and allow timezone decoration
                        arg = arg.astimezone(pytz.utc).replace(tzinfo=None)
            if type(arg) == datetime:
                naive_dt = arg
                if naive_dt.tzinfo:
                    tzs.add(SaneTime.to_timezone(str(naive_dt.tzinfo)))
                    naive_dt = naive_dt.replace(tzinfo=None)

        if len(tzs)>1:
            raise TimeConstructionError("constructor arguments seem to specify more than one different timezone!  I can't possibly resolve that!  (timezones implied = %s)"%(tzs))

        # now we have enough info to figure out the tz:
        self.tz = len(tzs) and tzs.pop() or pytz.utc

        # and now that we've figured out tz, we can fully deconstruct the dt
        if naive_dt:
            if avoid_localize:
                uss.add(SaneTime.utc_datetime_to_us(naive_dt))
            else:
                uss.add(SaneTime.utc_datetime_to_us(self.tz.localize(naive_dt).astimezone(pytz.utc)))

        # if we got nothing yet for micros, then make it now
        if len(uss)==0:
            uss.add(SaneTime.utc_datetime_to_us(datetime.utcnow()))

        if len(uss)>1:
            raise TimeConstructionError("constructor arguments seem to specify more than one different time!  I can't possibly resolve that!  (micro times implied = %s)"%(uss))

        self.us = uss.pop()
        
        if len(args)>0:
            raise TimeConstructionError("Unexpected constructor arguments")

        
    @property
    def ms(self): return self.us/MILLI_MICROS 
    epoch_milliseconds = epoch_millis = milliseconds = millis = ms
    @property
    def s(self): return self.us/SECOND_MICROS
    epoch_seconds = epoch_secs = seconds = secs = s
    @property
    def m(self): return self.us/MINUTE_MICROS
    epoch_minutes = epoch_mins = minutes = mins = m
    @property
    def micros(self): return self.us
    epoch_microseconds = epoch_micros = microseconds = micros

    @property
    def tz_name(self): return self.tz.zone
    @property
    def tz_abbr(self): return self.tz._tzname

    def set_tz(self, tz): 
        self.tz = self.__class__.to_timezone(tz); return self
    def with_tz(self, tz):
        return self.__class__(self.us,tz)


    @property
    def _tuple(self): return (self.us, self.tz)

    def strftime(self, *args, **kwargs): return self.datetime.strftime(*args, **kwargs)

    def __cmp__(self, other): 
        if not hasattr(other, '__int__'): other = SaneTime(other)
        return cmp(self.us, int(other))
    def __hash__(self): return self.us.__hash__()

    def __add__(self, operand): 
        if not hasattr(operand, '__int__'): operand = SaneTime(operand)
        return self.__class__(self.us + int(operand),tz=self.tz)
    def __sub__(self, operand):
        if not hasattr(operand, '__int__'): operand = SaneTime(operand)
        if isinstance(operand, SaneTime): return SaneDelta(self.us - int(operand))
        return self.__add__(-int(operand))
    def __mul__(self, operand):
        return self.us * int(operand)
    def __div__(self, operand):
        return self.us / int(operand)
    
    def __int__(self): return int(self.us)
    def __long__(self): return long(self.us)

    def __repr__(self): return u"SaneTime(%s,%s)" % (self.us,repr(self.tz))
    def __str__(self): return unicode(self).encode('utf-8')
    def __unicode__(self): 
        dt = self.datetime
        micros = u".%06d"%dt.microsecond if dt.microsecond else ''
        time = u" %02d:%02d:%02d%s"%(dt.hour,dt.minute,dt.second,micros) if dt.microsecond or dt.second or dt.minute or dt.hour else ''
        return u"%04d-%02d-%02d%s +%s" % (dt.year, dt.month, dt.day, time, dt.tzinfo.zone)

    def clone(self): 
        """ cloning stuff """
        return self.__class__(self.us,self.tz)

    @property
    def ny_str(self): 
        """ a ny string """
        return self.ny_ndt.strftime('%I:%M:%S%p %m/%d/%Y')
    
    @property
    def utc_datetime(self): return SaneTime.us_to_utc_datetime(self.us)
    utc_dt = utc_datetime
    @property
    def utc_naive_datetime(self): return self.utc_datetime.replace(tzinfo=None)
    utc_ndt = utc_naive_datetime
    
    def to_timezoned_datetime(self, tz): return self.utc_datetime.astimezone(SaneTime.to_timezone(tz))
    def to_timezoned_naive_datetime(self, tz): return self.to_timezoned_datetime(tz).replace(tzinfo=None)

    @property
    def datetime(self): return self.to_timezoned_datetime(self.tz)
    dt = datetime
    @property
    def naive_datetime(self): return self.to_timezoned_naive_datetime(self.tz)
    ndt = naive_datetime

    @property
    def ny_datetime(self): return self.to_timezoned_datetime('America/New_York')
    ny_dt = ny_datetime
    @property
    def ny_naive_datetime(self): return self.to_timezoned_naive_datetime('America/New_York')
    ny_ndt = ny_naive_datetime



    @property
    def year(self): return self.dt.year
    @property
    def month(self): return self.dt.month
    @property
    def day(self): return self.dt.day
    @property
    def hour(self): return self.dt.hour
    @property
    def minute(self): return self.dt.minute
    @property
    def second(self): return self.dt.second
    @property
    def microsecond(self): return self.dt.microsecond

    #def add_datepart(self, months=None, years=None, auto_day_adjust=True):
        #months = (months or 0) + (years or 0) * 12
        #dt = self.utc_dt
        #day = dt.day
        #month = dt.month + months%12
        #year = dt.year + months/12
        #if auto_day_adjust:
            #if day>=29 and month==2:
                #leap_year = year%4==0 and (not year%100==0 or year%400==0)
                #day = 29 if leap_year else 28
            #elif day==31 and month in (4,6,9,11):
                #day = 30
        #return SaneTime(fucked_datetime(year,month,day,dt.hour,dt.minute,dt.second,dt.microsecond,tz=pytz.utc))

    @classmethod
    def utc_datetime_to_us(kls, dt):
        return calendar.timegm(dt.timetuple())*1000**2+dt.microsecond

    @classmethod
    def us_to_utc_datetime(kls, us):
        return pytz.utc.localize(datetime.utcfromtimestamp(us/10**6)).replace(microsecond = us%10**6)

    @classmethod
    def to_timezone(kls, tz):
        if not isinstance(tz, basestring): return tz
        return pytz.timezone(tz)


# null passthru utility
def ntime(*args, **kwargs): 
    if args:
        if args[0] is None: return None
    elif kwargs:
        if None in [v for k,v in kwargs.iteritems() if k!='tz']: return None
    return SaneTime(*args, **kwargs)

#primary aliases
time = sanetime = SaneTime
nsanetime = ntime


import calendar as shit_calendar
from datetime import datetime as fucked_datetime
from dateutil import parser as crap_parser
from error import SaneTimeError
import pytz

#TODO switch internals all over to microseconds since epoch-- and have millis an seconds as derived from that  (and make sure long's can handle that)
    # this should make things faster and simpler  - you could have the constructor take an s= or ms= or us= for the different constructor possibillities
    # okay so int is a long and long is an unlimited, so we only need int


class SaneTime(object):
    def __init__(self, *args, **kwargs):
        super(SaneTime,self).__init__()
        self.utc_micros = None
        self.tz = None
        tzs = []
        args = list(args)

        if kwargs.get('tz'):
            tzs.append(kwargs.pop('tz'))
        if kwargs.get('timezone'):
            tzs.append(kwargs.pop('timezone').zone)

        if kwargs.get('utc_micros') and len(args)==0:
            args.insert(0,kwargs.pop('utc_micros'))
        elif kwargs.get('utc_millis') and len(args)==0:
            args.insert(0,kwargs.pop('utc_millis')*1000)
        elif kwargs.get('utc_seconds') and len(args)==0:
            args.insert(0,kwargs.pop('utc_seconds')*1000**2)
            
        if len(args)>2 and len(args)<8:
            args = [fucked_datetime(*args)]

        if len(args)==0:
            dt = pytz.utc.localize(fucked_datetime.utcnow())
            args = [shit_calendar.timegm(dt.timetuple())*1000**2+dt.microsecond]

        if len(args)==1:
            arg = args[0]
            if type(arg) in (type(1L),type(1),type(1.0)):
                self.utc_micros = int(arg)
            elif type(arg) == type('2000-01-01'):
                arg = crap_parser.parse(arg)
            if type(arg) == type(fucked_datetime(1,1,1)):
                dt = arg
                if dt.tzinfo:
                    if getattr(dt.tzinfo,'zone',None):
                        tzs.append(dt.tzinfo.zone)
                    else:
                        dt = dt.replace(tzinfo=None)
                if not dt.tzinfo:
                    dt = pytz.timezone((tzs+['UTC'])[0]).localize(dt)
                self.__init_from_fucked_datetime(dt)


        if self.utc_micros is None or len(tzs)>1 or len(kwargs)>0:
            raise SaneTimeError('Unexpected constructor args')

        tzs.append('UTC')
        self.tz = self.tz or tzs[0]
        self.timezone = pytz.timezone(self.tz)

    def __init_from_fucked_datetime(self, dt):
        self.tz = dt.tzinfo.zone
        dt = dt.astimezone(pytz.utc)
        tt = dt.timetuple()
        epoch_seconds = shit_calendar.timegm(tt)
        self.utc_micros = epoch_seconds*1000**2+dt.microsecond

    def set_timezone(self, timezone):
        return self.set_tz(timezone.zone)

    def set_tz(self, tz):
        self.timezone = pytz.timezone(tz)
        self.tz = self.timezone.zone
        return self

    def new_timezone(self, timezone):
        return self.new_tz(timezone.zone)

    def new_tz(self, tz):
        return SaneTime(self.utc_micros, tz=tz)

    def to_datetime(self):
        dt = fucked_datetime.utcfromtimestamp(self.utc_micros/1000**2)
        dt = pytz.utc.localize(dt)
        dt = dt.replace(microsecond = self.utc_micros%1000**2)
        dt = dt.astimezone(self.timezone)
        return dt

    def strftime(self, *args, **kwargs):
        return self.to_datetime().strftime(*args, **kwargs)

    def __lt__(self, other):
        return self.utc_micros < other.utc_micros
    def __le__(self, other):
        return self.utc_micros <= other.utc_micros
    def __gt__(self, other):
        return self.utc_micros > other.utc_micros
    def __ge__(self, other):
        return self.utc_micros >= other.utc_micros

    def __repr__(self):
        return repr(self.to_datetime())
    def __str__(self):
        return str(self.to_datetime())

    def _get_utc_seconds(self):
        return (self.utc_micros+500000)/1000000
    def _get_utc_millis(self):
        return (self.utc_micros+500)/1000
    utc_seconds = property(_get_utc_seconds)
    utc_millis = property(_get_utc_millis)



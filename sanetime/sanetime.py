import calendar as shit_calendar
from datetime import datetime as fucked_datetime
from dateutil import parser as ok_parser
from error import SaneTimeError
import pytz

class SaneTime(object):
    def __init__(self, *args, **kwargs):
        super(SaneTime,self).__init__()
        self.utc_millis = None
        self.tz = None
        tzs = []
        args = list(args)

        if kwargs.get('tz'):
            tzs.append(kwargs.pop('tz'))
        if kwargs.get('timezone'):
            tzs.append(kwargs.pop('timezone').zone)

        if kwargs.get('utc_millis') and len(args)==0:
            args.insert(0,kwargs.pop('utc_millis'))
            
        if len(args)>2 and len(args)<8:
            args = [fucked_datetime(*args)]

        if len(args)==1:
            arg = args[0]
            if type(arg) in (type(1L),type(1)):
                self.utc_millis = long(arg)
            elif type(arg) == type('2000-01-01'):
                arg = ok_parser.parse(arg)
            if type(arg) == type(fucked_datetime(1,1,1)):
                dt = arg
                if dt.tzinfo:
                    tzs.append(dt.tzinfo.zone)
                else:
                    dt = pytz.timezone((tzs+['UTC'])[0]).localize(dt)
                self.__init_from_fucked_datetime(dt)

        if self.utc_millis == None or len(tzs)>1 or len(kwargs)>0:
            raise SaneTimeError('Unexpected constructor args')

        tzs.append('UTC')
        self.tz = self.tz or tzs[0]
        self.timezone = pytz.timezone(self.tz)

    def __init_from_fucked_datetime(self, dt):
        self.tz = dt.tzinfo.zone
        dt = dt.astimezone(pytz.utc)
        tt = dt.timetuple()
        epoch_seconds = long(shit_calendar.timegm(tt))
        self.utc_millis = epoch_seconds*1000L+(dt.microsecond+500)/1000

    def set_timezone(self, timezone):
        return self.set_tz(timezone.zone)

    def set_tz(self, tz):
        self.timezone = pytz.timezone(tz)
        self.tz = self.timezone.zone
        return self

    def new_timezone(self, timezone):
        return self.new_tz(timezone.zone)

    def new_tz(self, tz):
        return SaneTime(self.utc_millis, tz=tz)

    def to_datetime(self):
        return pytz.utc.localize(fucked_datetime.utcfromtimestamp(self.utc_millis/1000)).astimezone(self.timezone)


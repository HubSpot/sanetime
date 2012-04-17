from .error import Error

MILLI_MICROS = 10**3
SECOND_MICROS = MILLI_MICROS * 10**3
MINUTE_MICROS = SECOND_MICROS * 60
HOUR_MICROS = MINUTE_MICROS * 60
AVG_DAY_MICROS = HOUR_MICROS * 24
AVG_WEEK_MICROS = AVG_DAY_MICROS * 7
AVG_MONTH_MICROS = (AVG_DAY_MICROS * 365*4+1)/(12*4)
AVG_YEAR_MICROS = (AVG_DAY_MICROS * 365*4+1)/4

HALF_MILLI_MICROS = MILLI_MICROS / 2
HALF_SECOND_MICROS = SECOND_MICROS / 2
HALF_MINUTE_MICROS = MINUTE_MICROS / 2
HALF_HOUR_MICROS = HOUR_MICROS / 2
HALF_AVG_DAY_MICROS = AVG_DAY_MICROS / 2
HALF_AVG_WEEK_MICROS = AVG_WEEK_MICROS / 2
HALF_AVG_MONTH_MICROS = AVG_MONTH_MICROS / 2
HALF_AVG_YEAR_MICROS = AVG_YEAR_MICROS / 2

TRANSLATIONS = (
        (('ay','average_years','y','years'),AVG_YEAR_MICROS),
        (('am','average_months','m','months'),AVG_WEEK_MICROS),
        (('aw','average_weeks','w','weeks'),AVG_WEEK_MICROS),
        (('ad','average_days','d','days'),AVG_DAY_MICROS),
        (('h','hours'),HOUR_MICROS),
        (('m','mins','minutes'),MINUTE_MICROS),
        (('s','secs','seconds'),SECOND_MICROS),
        (('ms','millis','milliseconds'),MILLI_MICROS),
        (('us','micros','microseconds'),1) )
TRANSLATION_HASH = dict((alt,v) for k,v in TRANSLATIONS for alt in k)
SPECIAL_DESIGNATIONS = set(['y','years','m','months','w','weeks','d','days'])

class SaneDelta(object):
    def __init__(self, *args, **kwargs):
        self._d, self._m, self._y = None,None,None
        if args:
            self._us = int(args[0])
        else:
            self._us = sum(TRANSLATION_HASH[k]*(v or 0) for k,v in kwargs.iteritems())
            if SPECIAL_DESIGNATIONS & kwargs.keys():
                raise Error("Haven't implemented context aware deltas yet -- you'll have to get along with the 'average' versions for now")

    # rounded amounts
    @property
    def rounded_microseconds(self): return self._us
    @property
    def rounded_milliseconds(self): return (self._us + HALF_MILLI_MICROS) / MILLI_MICROS
    @property
    def rounded_seconds(self): return (self._us + HALF_SECOND_MICROS) / SECOND_MICROS
    @property
    def rounded_minutes(self): return (self._us + HALF_MINUTE_MICROS) / MINUTE_MICROS
    @property
    def rounded_hours(self): return (self._us + HALF_HOUR_MICROS) / HOUR_MICROS
    @property
    def rounded_average_days(self): return (self._us + HALF_AVG_DAY_MICROS) / AVG_DAY_MICROS
    @property
    def rounded_average_weeks(self): return (self._us + HALF_AVG_WEEK_MICROS) / AVG_WEEK_MICROS
    @property
    def rounded_average_months(self): return (self._us + HALF_AVG_MONTH_MICROS) / AVG_MONTH_MICROS
    @property
    def rounded_average_years(self): return (self._us + HALF_AVG_YEAR_MICROS) / AVG_YEAR_MICROS

    # aliases
    rus = rounded_microseconds
    rms = rounded_milliseconds
    rs = rounded_seconds
    rm = rounded_minutes
    rh = rounded_hours
    rad = rounded_average_days
    raw = rounded_average_weeks
    ram = rounded_average_months
    ray = rounded_average_years

    #rounded amounts are default aliases
    us = rus
    ms = rms
    s = rs
    m = rm
    h = rh
    ad = rad
    aw = raw
    am = ram
    ay = ray

    # unrounded amounts
    @property
    def whole_microseconds(self): return self._us
    @property
    def whole_milliseconds(self): return self._us / MILLI_MICROS
    @property
    def whole_seconds(self): return self._us / SECOND_MICROS
    @property
    def whole_minutes(self): return self._us / MINUTE_MICROS
    @property
    def whole_hours(self): return self._us / HOUR_MICROS
    @property
    def whole_average_days(self): return self._us / AVG_DAY_MICROS
    @property
    def whole_average_weeks(self): return self._us / AVG_WEEK_MICROS
    @property
    def whole_average_months(self): return self._us / AVG_MONTH_MICROS
    @property
    def whole_average_years(self): return self._us / AVG_YEAR_MICROS

    # aliases
    wus = whole_microseconds
    wms = whole_milliseconds
    ws = whole_seconds
    wm = whole_minutes
    wh = whole_hours
    wad = whole_average_days
    waw = whole_average_weeks
    wam = whole_average_months
    way = whole_average_years

    # float amounts
    @property
    def fractional_microseconds(self): return float(self.us)
    @property
    def fractional_milliseconds(self): return float(self.us) / MILLI_MICROS
    @property
    def fractional_seconds(self): return float(self.us) / SECOND_MICROS
    @property
    def fractional_minutes(self): return float(self.us)/ MINUTE_MICROS
    @property
    def fractional_hours(self): return float(self.us) / HOUR_MICROS
    @property
    def fractional_average_days(self): return float(self.us) / AVG_DAY_MICROS
    @property
    def fractional_average_weeks(self): return float(self.us) / AVG_WEEK_MICROS
    @property
    def fractional_average_months(self): return float(self.us) / AVG_MONTH_MICROS
    @property
    def fractional_average_years(self): return float(self.us) / AVG_YEAR_MICROS

    # aliases
    fus = fractional_microseconds
    fms = fractional_milliseconds
    fs = fractional_seconds
    fm = fractional_minutes
    fh = fractional_hours
    fad = fractional_average_days
    faw = fractional_average_weeks
    fam = fractional_average_months
    fay = fractional_average_years
    fms = fractional_microseconds


    def __cmp__(self, other): return cmp(self.us, int(other))
    def __hash__(self): return hash(self.us)

    def __int__(self): return self.us
    def __long__(self): return long(self.us)

    def __add__(self, operand): return SaneDelta(self.us + int(operand))
    def __sub__(self, operand): return SaneDelta(self.us - int(operand))
    def __mul__(self, operand): return SaneDelta(self.us * int(operand))
    def __div__(self, operand): return SaneDelta(self.us / int(operand))

    @property
    def _parts(self):
        days = self.wd
        hours = self.wh - self.wd*24
        minutes = self.wm - self.wh*60
        seconds = self.ws - self.wm*60
        millis = self.wms - self.ws*10**3
        micros = self.wus - self.ws*10**6
        parts = []
        if days: parts.append("%sd"%days)
        if hours: parts.append("%sh"%hours)
        if minutes: parts.append("%sm"%minutes)
        if seconds: parts.append("%ss"%seconds)
        if micros%1000: parts.append("%sus"%micros)
        elif millis: parts.append("%sms"%millis)
        return parts

    def __repr__(self): return 'SaneDelta(%s)'%self.us
    def __str__(self): return unicode(self).encode('utf-8')
    def __unicode__(self): return ''.join(self._parts)
    def abbr(self,limit=2): return ''.join(self._parts[:limit])


#TODO: implement
    #def ago(self):
        #"""
        #Get a datetime object or a int() Epoch timestamp and return a
        #pretty string like 'an hour ago', 'Yesterday', '3 months ago',
        #'just now', etc

        #copied from http://stackoverflow.com/questions/1551382/python-user-friendly-time-format
        #and then tweaked
        #"""
        #micro_delta = SaneTime().us - self.us
        #second_delta = (micro_delta+500*1000)/1000**2
        #day_delta = (micro_delta+1000**2*60**2*12)/(1000**2*60**2*24)

        #if micro_delta < 0:
            ## TODO: implement future times
            #return ''

        #if day_delta == 0:
            #if second_delta < 10:
                #return "just now"
            #if second_delta < 30:
                #return "%s seconds ago" % second_delta
            #if second_delta < 90:
                #return "a minute ago"
            #if second_delta < 30*60:
                #return "%s minutes ago" % ((second_delta+30)/60)
            #if second_delta < 90*60:
                #return "an hour ago"
            #return "%s hours ago" % ((second_delta+30*60)/60**2)
        #if day_delta < 2:
            #return "yesterday"
        #if day_delta < 7:
            #return "%s days ago" % day_delta
        #if day_delta < 11:
            #return "a week ago" % day_delta
        #if day_delta < 45:
            #return "%s weeks ago" % ((day_delta+3)/7)
        #if day_delta < 400:
            #return "%s months ago" % ((day_delta+15)/30)
        #return "%s years ago" % ((day_delta+182)/365)


sanedelta = SaneDelta
delta = SaneDelta

def nsanedelta(*args, **kwargs): 
    if args:
        if args[0] is None: return None
    elif kwargs:
        if set(kwargs.values()) == set([None]): return None
    return SaneDelta(*args, **kwargs)

ndelta = nsanedelta

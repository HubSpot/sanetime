MILLI_MICROS = 10**3
SECOND_MICROS = MILLI_MICROS * 10**3
MINUTE_MICROS = SECOND_MICROS * 60
HOUR_MICROS = MINUTE_MICROS * 60
DAY_MICROS = HOUR_MICROS * 24
WEEK_MICROS = DAY_MICROS * 7
AVG_MONTH_MICROS = (DAY_MICROS * 365*4+1)/(12*4)
AVG_YEAR_MICROS = (DAY_MICROS * 365*4+1)/4

HALF_MILLI_MICROS = MILLI_MICROS / 2
HALF_SECOND_MICROS = SECOND_MICROS / 2
HALF_MINUTE_MICROS = MINUTE_MICROS / 2
HALF_HOUR_MICROS = HOUR_MICROS / 2
HALF_DAY_MICROS = DAY_MICROS / 2
HALF_WEEK_MICROS = WEEK_MICROS / 2
HALF_AVG_MONTH_MICROS = AVG_MONTH_MICROS / 2
HALF_AVG_YEAR_MICROS = AVG_YEAR_MICROS / 2

TRANSLATIONS = (
        (('ay','avg_years'),AVG_YEAR_MICROS),
        (('am','avg_months'),WEEK_MICROS),
        (('w','weeks'),WEEK_MICROS),
        (('d','days'),DAY_MICROS),
        (('h','hours'),HOUR_MICROS),
        (('m','mins','minutes'),MINUTE_MICROS),
        (('s','secs','seconds'),SECOND_MICROS),
        (('ms','millis','milli_seconds'),MILLI_MICROS),
        (('us','micros','micro_seconds'),1) )
TRANSLATION_HASH = dict((alt,v) for k,v in TRANSLATIONS for alt in k)

class SaneDelta(object):
    def __init__(self, *args, **kwargs):
        if args:
            self.us = int(args[0])
        else:
            self.us = sum(TRANSLATION_HASH[k]*v for k,v in kwargs.iteritems())

    # rounded amounts
    @property
    def ms(self): return (self.us + HALF_MILLI_MICROS) / MILLI_MICROS
    @property
    def s(self): return (self.us + HALF_SECOND_MICROS) / SECOND_MICROS
    @property
    def m(self): return (self.us + HALF_MINUTE_MICROS) / MINUTE_MICROS
    @property
    def h(self): return (self.us + HALF_HOUR_MICROS) / HOUR_MICROS
    @property
    def d(self): return (self.us + HALF_DAY_MICROS) / DAY_MICROS
    @property
    def w(self): return (self.us + HALF_WEEK_MICROS) / WEEK_MICROS
    @property
    def am(self): return (self.us + HALF_AVG_MONTH_MICROS) / AVG_MONTH_MICROS
    @property
    def ay(self): return (self.us + HALF_AVG_YEAR_MICROS) / AVG_YEAR_MICROS

    # aliases
    @property
    def micros(self): return self.us
    microseconds = micros
    millis = ms
    milliseconds = ms
    seconds = s
    secs = s
    minutes = m
    mins = m
    hours = h
    days = d
    weeks = w
    avg_months = am
    avg_years = ay

    # unrounded amounts
    @property
    def _us(self): return self.us
    @property
    def _ms(self): return self.us / MILLI_MICROS
    @property
    def _s(self): return self.us / SECOND_MICROS
    @property
    def _m(self): return self.us / MINUTE_MICROS
    @property
    def _h(self): return self.us / HOUR_MICROS
    @property
    def _d(self): return self.us / DAY_MICROS
    @property
    def _w(self): return self.us / WEEK_MICROS
    @property
    def _am(self): return self.us / AVG_MONTH_MICROS
    @property
    def _ay(self): return self.us / AVG_YEAR_MICROS

    # aliases
    _micros = _us
    _microseconds = _micros
    _millis = _ms
    _milliseconds = _ms
    _seconds = _s
    _secs = _s
    _minutes = _m
    _mins = _m
    _hours = _h
    _days = _d
    _weeks = _w
    _avg_months = _am
    _avg_years = _ay

    # float amounts
    @property
    def fus(self): return float(self.us)
    @property
    def fms(self): return float(self.us) / MILLI_MICROS
    @property
    def fs(self): return float(self.us) / SECOND_MICROS
    @property
    def fm(self): return float(self.us)/ MINUTE_MICROS
    @property
    def fh(self): return float(self.us) / HOUR_MICROS
    @property
    def fd(self): return float(self.us) / DAY_MICROS
    @property
    def fw(self): return float(self.us) / WEEK_MICROS
    @property
    def fam(self): return float(self.us) / AVG_MONTH_MICROS
    @property
    def fay(self): return float(self.us) / AVG_YEAR_MICROS

    # aliases
    f_micros = fus
    f_microseconds = f_micros
    f_millis = fms
    f_milliseconds = fms
    f_seconds = fs
    f_secs = fs
    f_minutes = fm
    f_mins = fm
    f_hours = fh
    f_days = fd
    f_weeks = fw
    f_avg_months = fam
    f_avg_years = fay


    def __lt__(self, other): return self.us < int(other)
    def __le__(self, other): return self.us <= int(other)
    def __gt__(self, other): return self.us > int(other)
    def __ge__(self, other): return self.us >= int(other)
    def __eq__(self, other): return self.us == int(other)
    def __ne__(self, other): return self.us != int(other)

    def __hash__(self): return hash(self.us)

    def __int__(self): return self.us
    def __long__(self): return long(self.us)

    def __add__(self, operand): return SaneDelta(us = self.us + int(operand))
    def __sub__(self, operand): return SaneDelta(us = self.us - int(operand))
    def __mul__(self, operand): return SaneDelta(us = self.us * int(operand))
    def __div__(self, operand): return SaneDelta(us = self.us / int(operand))

    @property
    def _parts(self):
        days = self._d
        hours = self._h - self._d*24
        minutes = self._m - self._h*60
        seconds = self._s - self._m*60
        millis = self._ms - self._s*10**3
        micros = self._us - self._s*10**6
        parts = []
        if days: parts.append("%sd"%days)
        if hours: parts.append("%sh"%hours)
        if minutes: parts.append("%sm"%minutes)
        if seconds: parts.append("%ss"%seconds)
        if micros%1000: parts.append("%sus"%micros)
        elif millis: parts.append("%sms"%millis)
        return parts

    def __repr__(self): return 'SaneDelta(us=%s)'%self.us
    def __str__(self): return unicode(self).encode('utf-8')
    def __unicode__(self): return ' '.join(self._parts)
    def abbr(self,limit=2): return ''.join(self._parts[:limit])


sanedelta = SaneDelta
delta = SaneDelta

def nsanedelta(*args, **kwargs): 
    if args:
        if args[0] is None: return None
    else:
        if None in kwargs.values(): return None
    return SaneDelta(*args, **kwargs)

MILLI_MICROS = 10**3
SECOND_MICROS = MILLI_MICROS * 10**3
MINUTE_MICROS = SECOND_MICROS * 60
HOUR_MICROS = MINUTE_MICROS * 60
MEAN_DAY_MICROS = HOUR_MICROS * 24
MEAN_WEEK_MICROS = MEAN_DAY_MICROS * 7
MEAN_MONTH_MICROS = (MEAN_DAY_MICROS * (365*4+1)) / (12*4)
MEAN_YEAR_MICROS = (MEAN_DAY_MICROS * (365*4+1)) / 4

HALF_MILLI_MICROS = MILLI_MICROS / 2
HALF_SECOND_MICROS = SECOND_MICROS / 2
HALF_MINUTE_MICROS = MINUTE_MICROS / 2
HALF_HOUR_MICROS = HOUR_MICROS / 2
HALF_MEAN_DAY_MICROS = MEAN_DAY_MICROS / 2
HALF_MEAN_WEEK_MICROS = MEAN_WEEK_MICROS / 2
HALF_MEAN_MONTH_MICROS = MEAN_MONTH_MICROS / 2
HALF_MEAN_YEAR_MICROS = MEAN_YEAR_MICROS / 2

TRANSLATIONS = (
        (('my','mean_years'),MEAN_YEAR_MICROS),
        (('mm','mean_months'),MEAN_MONTH_MICROS),
        (('mw','mean_weeks'),MEAN_WEEK_MICROS),
        (('md','mean_days'),MEAN_DAY_MICROS),
        (('h','hours'),HOUR_MICROS),
        (('m','mins','minutes'),MINUTE_MICROS),
        (('s','secs','seconds'),SECOND_MICROS),
        (('ms','millis','milliseconds'),MILLI_MICROS),
        (('us','micros','microseconds'),1) )
TRANSLATION_HASH = dict((alt,v) for k,v in TRANSLATIONS for alt in k)

class SaneDelta(object):
    def __init__(self, *args, **kwargs):
        if args:
            self.us = int(args[0])
        else:
            self.us = sum(TRANSLATION_HASH[k]*(v or 0) for k,v in kwargs.iteritems())

    # rounded amounts
    @property
    def rounded_microseconds(self): return self.us
    @property
    def rounded_milliseconds(self): return (self.us + HALF_MILLI_MICROS) / MILLI_MICROS
    @property
    def rounded_seconds(self): return (self.us + HALF_SECOND_MICROS) / SECOND_MICROS
    @property
    def rounded_minutes(self): return (self.us + HALF_MINUTE_MICROS) / MINUTE_MICROS
    @property
    def rounded_hours(self): return (self.us + HALF_HOUR_MICROS) / HOUR_MICROS
    @property
    def rounded_mean_days(self): return (self.us + HALF_MEAN_DAY_MICROS) / MEAN_DAY_MICROS
    @property
    def rounded_mean_weeks(self): return (self.us + HALF_MEAN_WEEK_MICROS) / MEAN_WEEK_MICROS
    @property
    def rounded_mean_months(self): return (self.us + HALF_MEAN_MONTH_MICROS) / MEAN_MONTH_MICROS
    @property
    def rounded_mean_years(self): return (self.us + HALF_MEAN_YEAR_MICROS) / MEAN_YEAR_MICROS

    # aliases
    rus = rounded_micros = rounded_microseconds
    rms = rounded_millis = rounded_milliseconds
    rs = rounded_secs = rounded_seconds
    rm = rounded_mins = rounded_minutes
    rh = rounded_hours
    rmd = rounded_mean_days
    rmw = rounded_mean_weeks
    rmm = rounded_mean_months
    rmy = rounded_mean_years

    #rounded amounts are default aliases
    micros = microseconds = rus
    ms = millis = milliseconds = rms
    s = secs = seconds = rs
    m = mins = minutes = rm
    h = hours = rh
    md = mean_days = rmd
    mw = mean_weeks = rmw
    mm = mean_months = rmm
    my = mean_years = rmy

    # unrounded amounts
    @property
    def whole_microseconds(self): return self.us
    @property
    def whole_milliseconds(self): return self.us / MILLI_MICROS
    @property
    def whole_seconds(self): return self.us / SECOND_MICROS
    @property
    def whole_minutes(self): return self.us / MINUTE_MICROS
    @property
    def whole_hours(self): return self.us / HOUR_MICROS
    @property
    def whole_mean_days(self): return self.us / MEAN_DAY_MICROS
    @property
    def whole_mean_weeks(self): return self.us / MEAN_WEEK_MICROS
    @property
    def whole_mean_months(self): return self.us / MEAN_MONTH_MICROS
    @property
    def whole_mean_years(self): return self.us / MEAN_YEAR_MICROS

    # aliases
    wus = whole_micros = whole_microseconds
    wms = whole_millis = whole_milliseconds
    ws = whole_secs = whole_seconds
    wm = whole_mins = whole_minutes
    wh = whole_hours
    wmd = whole_mean_days
    wmw = whole_mean_weeks
    wmm = whole_mean_months
    wmy = whole_mean_years

    # float amounts
    @property
    def float_microseconds(self): return float(self.us)
    @property
    def float_milliseconds(self): return float(self.us) / MILLI_MICROS
    @property
    def float_seconds(self): return float(self.us) / SECOND_MICROS
    @property
    def float_minutes(self): return float(self.us)/ MINUTE_MICROS
    @property
    def float_hours(self): return float(self.us) / HOUR_MICROS
    @property
    def float_mean_days(self): return float(self.us) / MEAN_DAY_MICROS
    @property
    def float_mean_weeks(self): return float(self.us) / MEAN_WEEK_MICROS
    @property
    def float_mean_months(self): return float(self.us) / MEAN_MONTH_MICROS
    @property
    def float_mean_years(self): return float(self.us) / MEAN_YEAR_MICROS

    # aliases
    fus = float_micros = float_microseconds
    fms = float_millis = float_milliseconds
    fs = float_secs = float_seconds
    fm = float_mins = float_minutes
    fh = float_hours
    fmd = float_mean_days
    fmw = float_mean_weeks
    fmm = float_mean_months
    fmy = float_mean_years

    # positional amounts
    @property
    def positional_microseconds(self): return self.us % SECOND_MICROS
    @property
    def positional_milliseconds(self): return self.us % SECOND_MICROS / MILLI_MICROS
    @property
    def positional_seconds(self): return self.us % MINUTE_MICROS / SECOND_MICROS
    @property
    def positional_minutes(self): return self.us % HOUR_MICROS / MINUTE_MICROS
    @property
    def positional_hours(self): return self.us % MEAN_DAY_MICROS / HOUR_MICROS

    #aliases
    pus = positional_micros = positional_microseconds
    pms = positional_millis = positional_milliseconds
    ps = positional_secs = positional_seconds
    pm = positional_mins = positional_minutes
    ph = positional_hours

    # positional rounded amounts
    @property
    def positional_rounded_microseconds(self): return self.us % SECOND_MICROS
    @property
    def positional_rounded_milliseconds(self): return (self.us % SECOND_MICROS + HALF_MILLI_MICROS) / MILLI_MICROS
    @property
    def positional_rounded_seconds(self): return (self.us % MINUTE_MICROS + HALF_SECOND_MICROS) / SECOND_MICROS
    @property
    def positional_rounded_minutes(self): return (self.us % HOUR_MICROS + HALF_MINUTE_MICROS) / MINUTE_MICROS
    @property
    def positional_rounded_hours(self): return (self.us % MEAN_DAY_MICROS + HALF_HOUR_MICROS) / HOUR_MICROS

    #aliases
    prus = positional_rounded_micros = positional_rounded_microseconds
    prms = positional_rounded_millis = positional_rounded_milliseconds
    prs = positional_rounded_secs = positional_rounded_seconds
    prm = positional_rounded_mins = positional_rounded_minutes
    prh = positional_rounded_hours

    def clone(self): return SaneDelta(self.us)

    def __cmp__(self, other): return cmp(self.us, int(other))
    def __hash__(self): return hash(self.us)

    def __int__(self): return self.us
    def __long__(self): return long(self.us)

    def __add__(self, operand): return SaneDelta(self.us + int(operand))
    def __sub__(self, operand): return SaneDelta(self.us - int(operand))
    def __mul__(self, operand): return SaneDelta(self.us * int(operand))
    def __div__(self, operand): return SaneDelta(self.us / int(operand))

    def __neg__(self): return SaneDelta(-self.us)
    def __pos__(self): return SaneDelta(+self.us)
    def __abs__(self): return SaneDelta(abs(self.us))

    def __repr__(self): return 'SaneDelta(%s)'%self.us
    def __str__(self): return unicode(self).encode('utf-8')
    def __unicode__(self): return self.construct_str()


    @property
    def abbr(self): return self.construct_str(relative_resolution=2, absolute_resolution='s', separator='')

    #TODO: test this sucker
    #TODO; test negative deltas
    def construct_str(self, relative_resolution=None, absolute_resolution='us', separator=' '):
        parts = []
        delta = abs(self)
        relative_resolution = relative_resolution or 6
        if absolute_resolution == 'md' or len(parts)==relative_resolution-1 and delta.wmd:
            parts.append("%sd"%delta.rmd)
        else:
            if delta.wmd: parts.append("%sd"%delta.wmd)
            if absolute_resolution == 'h' or len(parts)==relative_resolution-1 and (delta.ph or len(parts)):
                parts.append("%sh"%delta.prh)
            else:
                if delta.ph or len(parts): parts.append("%sh"%delta.ph)
                if absolute_resolution == 'm' or len(parts)==relative_resolution-1 and (delta.pm or len(parts)):
                    parts.append("%sm"%delta.prm)
                else:
                    if delta.pm or len(parts): parts.append("%sm"%delta.pm)
                    if absolute_resolution == 's' or len(parts)==relative_resolution-1 and (delta.ps or len(parts)):
                        parts.append("%ss"%delta.prs)
                    else:
                        if absolute_resolution == 'ms' or len(parts)==relative_resolution-1 and (delta.pms or len(parts)):
                            parts.append("%s.%03ds" % (delta.ps,delta.prms))
                        else:
                            parts.append("%s.%06ds" % (delta.ps,delta.pus))
        return "%s%s" % ('' if self>=0 else '-', separator.join(parts))
 


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


def nsanedelta(*args, **kwargs): 
    if args:
        if args[0] is None: return None
    elif kwargs:
        if set(kwargs.values()) == set([None]): return None
    return SaneDelta(*args, **kwargs)

#aliases:
delta = sanedelta = SaneDelta
ndelta = nsanedelta

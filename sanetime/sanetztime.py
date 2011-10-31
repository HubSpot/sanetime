import re
from sanetime import sanetime
from error import SaneTimeError
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

# keeping lowercase so we can mimic datetime as much as is reasonable
class sanetztime(sanetime):
    """
    sanetztime is concerned with a particular moment in time AND which timezone that moment in time
    was experienced.  Two sanetztimes are not equal unless they are the same moment in time and
    they are in the same timezone as identified by the pytz timezone.  Even if these timezones
    appear to have the same definition, but have a different label they are considered different.
    They must have the same structure and the same label.

    In most other respects sanetztime is similar to sanetime.
    """

    STR_NATIVE_TZ_FORMAT = re.compile(r'^(\d+)([um]?s)\s(.*)$')

    def __init__(self, *args, **kwargs):
        if len(args)>0:
            args = list(args)
            if isinstance(args[0], sanetztime):
                kwargs['tz'] = args[0].tz
                args[0] = args[0].us
            elif isinstance(args[0], basestring):
                if self.__class__.STR_NATIVE_TZ_FORMAT.match(args[0]):
                    parts = args[0].split(' ')
                    kwargs['tz'] = parts[1]
                    args[0] = parts[0]
        super(sanetztime,self).__init__(*args, **kwargs)
        self.tz = self.to_datetime().tzinfo

    def set_tz(self, tz):
        return super(sanetztime,self)._set_tz(tz)

    def with_tz(self, tz):
        return sanetztime(self.us, tz=tz)

    def to_datetime(self):
        return self.to_utc_datetime().astimezone(self.tz)

    def to_naive_datetime(self):
        return self.to_datetime().replace(tzinfo=None)

    def to_sanetime(self):
        return sanetime(self.us)

    def strftime(self, *args, **kwargs):
        return self.to_datetime().strftime(*args, **kwargs)

    def _data(self):
        return (self.us, self.tz)

    def __eq__(self, other):
        return self._data() == other._data()
    def __ne__(self, other):
        return self._data() != other._data()

    def __hash__(self):
        return self._data().__hash__()

    def __add__(self, extra_us):
        if not isinstance(extra_us, Number):
            raise SaneTimeError('Can only add/sub microseconds (expecting a number)')
        return sanetztime(self.us + int(extra_us), tz = self.tz)

    def __repr__(self):
        return '%s %s' % (self.__repr_naive__(), self.tz_name)

    def __str__(self):
        return '%s %s' % (super(sanetztime,self).__str__(), self.tz_name)
    
    def _get_tz(self):
        return self._tz
    tz = property(_get_tz, set_tz)

    def _get_tz_name(self):
        return self.tz.zone
    tz_name = property(_get_tz_name)

    def _get_tz_abbr(self):
        return self.tz._tzname
    tz_abbr = property(_get_tz_abbr)
    


from sanetime import SaneTime

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

class SaneTzTime(SaneTime):
    """
    sanetztime is concerned with a particular moment in time AND which timezone that moment in time
    was experienced.  Two sanetztimes are not equal unless they are the same moment in time and
    they are in the same timezone as identified by the pytz timezone.  Even if these timezones
    appear to have the same definition, but have a different label they are considered different.
    They must have the same structure and the same label.

    In most other respects sanetztime is just like sanetime.
    """

    def __cmp__(self, other): 
        if not hasattr(other, '_tuple'): other = SaneTzTime(other)
        return cmp(self._tuple, other._tuple)
    def __hash__(self): return self._tuple.__hash__()
    def __repr__(self): return u"SaneTzTime(%s,%s)" % (self.us,repr(self.tz))

    @property
    def time(self): return SaneTime(self.us,self.tz)
    sanetime=time
    
# null passthrough utility
def nsanetztime(*args, **kwargs): 
    if not args or args[0] is None: return None
    return SaneTzTime(*args, **kwargs)

#primary aliases
tztime = sanetztime = SaneTzTime
ntztime = nsanetztime

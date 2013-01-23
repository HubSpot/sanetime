from . import time

class SaneSpan(object):
    def __init__(self, start, delta=None, end=None):
        super(SaneSpan,self).__init__()
        self.start = time(start)
        if delta is None:
            end = time(end or 0)
            self.start = min(self.start,end)
            self.delta = end-self.start
        else:
            self.delta = delta

    @property
    def end(self): return self.start+self.delta

    def overlaps(self, other):
        return self.start < other.end and self.end > other.start

    def __repr__(self): return 'SaneSpan(start=%s,delta=%s)'%(repr(self.start),repr(self.delta))
    def __str__(self): return unicode(self).encode('utf-8')
    def __unicode__(self): u"%s +%s" % (unicode(self.start), unicode(self.delta))

def nsanespan(*args, **kwargs): 
    if args and (args[0] is None or args[-1] is None): return None
    return SaneSpan(*args, **kwargs)

#aliases:
span = sanespan = SaneSpan
nspan = nsanespan


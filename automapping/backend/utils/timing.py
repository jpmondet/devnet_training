#! /usr/bin/env python3

from time import time
from functools import wraps


def timing(f):
    """ Can be used as a function decorator (@timing) to
    get the time the func took """
    @wraps(f)
    def wrap(*args, **kw):
        ts = time()
        result = f(*args, **kw)
        te = time()
        print('func:%r args:[%r, %r] took: %2.4f sec' % \
          (f.__name__, args, kw, te-ts))
        return result
    return wrap
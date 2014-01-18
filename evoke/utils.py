
# standard
from __future__ import absolute_import, print_function, division
import random
import types
import warnings

# local
#from .. import settings


def as_list(val):
    if isinstance(val, list):
        return val
    elif isinstance(val, (int, float, str)):
        return [val, ]
    elif val is None:
        return []
    elif isinstance(val, tuple):
        return list(val)
    elif isinstance(val, type.StringTypes):
        return [val, ]
    elif isinstance(val, types.DictionaryType):
        return val.items()
    else:
        raise ValueError('Unable to convert <%s> to list' % type(val))


def distribute(list1, list2):
    plan = list1 + list2
    random.shuffle(plan)
    return plan


def ms_to_frames(ms, freq, as_int=True):
    raw = ms * freq / 1000
    retval = int(round(raw)) if as_int else raw
#    if settings.DEBUG and retval != raw:
#        warnings.warn('Conversion from ms to frames resulted in '
#            'non-integer number of frames. The value was truncated '
#            'to an int and will not result in accurate timing.')
    return retval


def frames_to_ms(frames, freq):
    return frames / freq


def rand_frame_interval(start_ms, end_ms, freq):
    val = random.randint(start_ms, end_ms)
    return ms_to_frames(val, freq)

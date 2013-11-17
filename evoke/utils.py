
# standard
from __future__ import print_function, division
import random
import types


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

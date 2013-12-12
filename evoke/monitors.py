
#standard
from __future__ import print_function, division

# vendor
from psychopy.monitors import Monitor


_LAB_MONITORS = {
    'mac-13in': {
        'resolution': (1440, 900),
        'diagonal': 34
    },
    'run-station': {
        'resolution': (1920, 1200),
        'diagonal': 61
    }
}


def get(name):
    """
    Returns configured monitor object for known monitor names.
    """
    name = name.lower()
    if name not in _LAB_MONITORS:
        raise ValueError("Unknown monitor '%s'. Expecting %s" % _LAB_MONITORS.keys())
    mon = Monitor(name)
    mon.setDistance(62)
    mon.setSizePix(_LAB_MONITORS[name]['resolution'])
    mon.setWidth(_LAB_MONITORS[name]['diagonal'])
    return mon

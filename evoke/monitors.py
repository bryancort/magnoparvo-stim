
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
        'diagonal': 61,
        'response_time': 8
    }
}


def get(name, dist_cm=120):
    """
    Returns configured monitor object for known monitor names.
    """
    name = name.lower()
    if name not in _LAB_MONITORS:
        raise ValueError("Unknown monitor '%s'. Expecting %s" % _LAB_MONITORS.keys())

    try:
        mon = Monitor(name)
    except Exception as exc:
        raise IOError("Could not initialize monitor '%s': %s" % (name, exc))

    mon.setDistance(dist_cm)
    mon.setSizePix(_LAB_MONITORS[name]['resolution'])
    mon.setWidth(_LAB_MONITORS[name]['diagonal'])
    mon._response_time = _LAB_MONITORS[name].get('response_time', None)

    return mon

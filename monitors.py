
# vendor
from psychopy.monitors import Monitor


_LAB_MONITORS = {
    'mac-13in': {
        'resolution': (1440, 900),
        'diagonal': 13
    },
    'run-station': {
        'resolution': (1920, 1200),
        'diagonal': 14
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
    mon.setDistance(45)
    mon.setSizePix(_LAB_MONITORS[name]['resolution'])
    mon.setWidth(_LAB_MONITORS[name]['diagonal'])
    return mon

#standard
from __future__ import print_function, division

# vendor
import pyxid
from psychopy.core import Clock
from psychopy import event

# local
import utils


class Controller(object):

    def wait_for_response(self, buttons=None, timeout=None):
        raise NotImplementedError


class Keyboard(Controller):
    pass


class Mouse(Controller):
    pass


class Cedrus(Controller):

    def __init__(self):
        devices = pyxid.get_xid_devices()
        self._device = devices[0]
        if self._device.is_response_device():
            self._device.reset_base_timer()
            self._device.reset_rt_timer()

    def wait_for_response(self, buttons=None, timeout=None):
        buttons = utils.as_list(buttons)

        if timeout:
            timer = Clock()
            check = lambda: timer.getTime() < timeout
        else:
            check = lambda: True

        while check():
            self._device.poll_for_response()
            if self._device.response_queue_size() >= 2:
                response = self._device.get_next_response()
                self._device.clear_response_queue()
                if (buttons and response in buttons) or (not buttons and response):
                    return True


_LAB_CONTROLLERS = {
    'cedrus': {
        'class': Cedrus,
        'params': {}
    },
    'keyboard': {
        'class': Keyboard,
        'params': {}
    },
    'mouse': {
        'class': Mouse,
        'params': {}
    }
}


def get(name):
    name = name.lower()
    if name not in _LAB_CONTROLLERS:
        raise ValueError("Unknown controllers '%s'. Expecting %s" % _LAB_CONTROLLERS.keys())
    contr = _LAB_CONTROLLERS[name]['class']()
    return contr

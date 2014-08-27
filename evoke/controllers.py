
#standard
from __future__ import print_function, division
import time

# vendor
import pyxid
from psychopy.core import Clock
from psychopy import event

# local
import utils
from evoke import _IO_HUB


class Controller(object):

    def wait_for_response(self, buttons=None, timeout=None):
        raise NotImplementedError

    def poll_for_response(self, buttons=None):
        raise NotImplementedError

    def _wait_for_response(self):
        raise NotImplementedError


class Keyboard(Controller):

    def __init__(self, window=None):
        self._window = window

    def wait_for_response(self, buttons=None, timeout=None):
        while True:
            for key in self.poll():
                if not buttons:
                    break
                elif key in buttons:
                    break
            # self._window.flip(clearBuffer=False)
        return True

    def poll(self):
        return event.getKeys(timeStamped=False)


class Mouse(Controller):

    def __init__(self, window=None):
        self._window = window
        self._mouse = _IO_HUB.devices.mouse
        
    def hide(self):
        self._mouse.setSystemCursorVisibility(False)

    def wait_for_response(self, buttons=None, timeout=None):
        raise NotImplementedError('Need to define')

    def poll(self):
        raise NotImplementedError('Need to define')


class Cedrus(Controller):

    def __init__(self, window=None):
        self._device = self._catch_device()
        if self._device.is_response_device():
            self._device.reset_base_timer()
            self._device.reset_rt_timer()
        self._window = window

    def _catch_device(self, timeout=15.0):
        devices = []
        start_capture = time.time()
        while not devices:
            devices = pyxid.get_xid_devices()
            if (time.time() - start_capture) > timeout:
                raise IOError('Could not capture Cedrus device')
            time.sleep(0.1)
        device = devices[0]
        return device

    def wait_for_response(self, buttons=None, timeout=None):
        buttons = utils.as_list(buttons)

        if timeout:
            timer = Clock()
            check = lambda: timer.getTime() < timeout
        else:
            check = lambda: True

        self._clear()

        while check():
            response = self._get_buttons()
            if (buttons and response in buttons) or (not buttons and response):
                break
            # self._window.flip(clearBuffer=False)

        self._clear()  # This should really happen as async thread
        return True

    def _get_buttons(self):
        buttons = []
        self._device.poll_for_response()
        self._device.poll_for_response()
        for response in self._device.response_queue:
            if response['pressed'] is False:
                buttons.append(response['key'])
        self._device.clear_response_queue()
        return buttons

    def _clear(self):
        self._device.poll_for_response()
        while self._device.response_queue_size() > 0:
            self._device.clear_response_queue()
            self._device.poll_for_response()


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


def get(name, **kwargs):
    name = name.lower()
    if name not in _LAB_CONTROLLERS:
        raise ValueError("Unknown controllers '%s'. Expecting %s" % _LAB_CONTROLLERS.keys())
    try:
        contr = _LAB_CONTROLLERS[name]['class'](**kwargs)
    except Exception as exc:
        raise IOError("Could not initialize control '%s': %s" % (name, exc))
    return contr

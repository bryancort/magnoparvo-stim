
# standard
from __future__ import print_function, division
import os

# vendor
from psychopy import visual, logging, core
import egi.simple as egi
# import egi.threaded as egi

# local
from evoke import controllers
from evoke import monitors


class Experiment(object):

    def __init__(self, debug=False):
        self._monitor = None
        self._window = None
        self._netstation = None
        self._controller = None
        self._debug = debug

        if debug:
            logging.console.setLevel(logging.DEBUG)
        else:
            logging.console.setLevel(logging.WARNING)

    def init_display(self, monitor, width=1920, height=1200):
        self._monitor = monitors.get(monitor)
        self._window = visual.Window(size=[width, height],
                                     monitor=self._monitor,
                                     allowGUI=False)

        if self._debug:
            self._window.setRecordFrameIntervals(True)
            self._window._refreshThreshold = 1/60.0 + 0.004

    def init_controller(self, controller):
        self._controller = controllers.get(controller)

    def start_netstation(self):
        self._netstation = egi.Netstation()
        self._netstation.connect('10.0.0.42', 55513)
        self._netstation.BeginSession()
        self._netstation.sync()
        self._netstation.StartRecording()

    def stop_netstation(self):
        self._netstation.StopRecording()
        self._netstation.EndSession()
        self._netstation.disconnect()

    def send_event(self, key='evt_', label=None, description=None, table=None):
        self._netstation.send_event(key,
                    label=label,
                    timestamp=egi.ms_localtime(),
                    description=description,
                    table=table)

    def timed_func(self, frames, func=None):
        # Assumes a refresh rate of 60 kHz
        for _ in range(frames):
            if func:
                func()
            else:
                pass
            self._window.flip()

    def load_still_images(self, dirpath, pos=(0.0, 0.0)):
        images = []
        for fname in os.listdir(dirpath):
            if fname.endswith('.jpg'):
                img = self.load_still_image(os.path.join(dirpath, fname), pos)
                images.append(img)
        return images

    def load_still_image(self, fpath, pos=(0.0, 0.0)):
        return visual.ImageStim(self._window, image=fpath, pos=pos)

    def wait_for_response(self, buttons=None):
        return self._controller.wait_for_response()

    def run(self):
        raise NotImplementedError()

    def release(self):
        self._windows.close()
        core.quit()

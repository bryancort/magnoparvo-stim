#!/usr/bin/env python

# standard
import random
import os
import time

# vendor
from psychopy import visual, logging, event, core
import egi.simple as egi
# import egi.threaded as egi

# local
import monitors
import utils


def get_current_dir(append=None):
    path = os.path.dirname(os.path.abspath(__file__))
    if append:
        path = os.path.join(path, append)
    return path


class Experiment(object):

    def __init__(self, debug=False):
        self._monitor = None
        self._window = None
        self._netstation = None
        self._control_box = ControlBox()

        if debug:
            logging.console.setLevel(logging.DEBUG)
        else:
            logging.console.setLevel(logging.INFO)

    def start_netstation(self):
        self._netstation = egi.Netstation()
        self._netstation.connect('10.0.0.42', 55513)
        self._netstation.BeginSession()
        self._netstation.sync()
        self._netstation.StartRecording()

    def stop_netstation(self):
        self._netstat.StopRecording()
        self._netstat.EndSession()
        self._netstat.disconnect()

    def send_event(self, key='evt_', label=None, table=None):
        self._netstat.send_event('evt_',
                    label=label,
                    timestamp=egi.ms_localtime(),
                    table=table)

    def timed_func(self, frames, func=None):
        # Assumes a refresh rate of 60 kHz
        for _ in range(frames):
            if func:
                func()
            else:
                pass
            self._window.flip()

    def init_display(self, monitor, width=1920, height=1200):
        self._monitor = monitors.get_monitor(monitor)
        self._window = visual.Window(size=[width, height],
                                     monitor=self._monitor,
                                     allowGUI=False)

    def load_still_images(self, dirpath, pos=(0.0, 0.0)):
        images = []
        for fname in os.listdir(dirpath):
            if fname.endswith('.bmp'):
                img = self.load_image_stim(self._window,
                                           os.path.join(dirpath, fname),
                                           pos)
                images.append(img)
        return images

    def load_still_image(self, fpath, pos=(0.0, 0.0)):
        return visual.ImageStim(self._window, image=fpath, pos=pos)

    def wait_for_response(self, buttons=None):
        return self._control_box.wait_for_keys()

    def run(self):
        raise NotImplementedError()

    def release(self):
        self._windows.close()
        core.quit()


class ControlBox(object):

    def __init__(self):
        pass

    def connect(self):
        pass

    def wait_for_buttons(self, buttons=None, timeout=None):
        buttons = util.as_list(keys)
        time.sleep(6)
        return True


def Magno(Experiment):

    def run(self):

        segments = [random.randint(36, 60) for _ in range (200)]
        still_images = self.load_still_images(get_current_dir('img'))

        plan = utils.distribute(segments, still_images)

        horizontal_sine = visual.GratingStim(self._window,
                                             tex='sin',
                                             units='deg',
                                             sf=1.5,
                                             size=2)
        self.start_netstation()

        clock = core.Clock()

        def move():
            # horizontal_sine.setPhase(4*t)
            horizontal_sine.setPhase(0.06666666666666667, '+')
            horizontal_sine.draw()

        for current in plan:
            if not isinstance(current, int):
                # Show image
                self.timed_op(500)

                # Wait for the response
                self.wait_for_response()

                # Wait a random interval
                timed_op(random.randint(36, 60), move)
            else:
                # Move for 100 ms / 6 frames
                timed_op(6, move)

                # Pause for however long plan says
                timed_op(current)

                # optionally can perform additional synchronization # ns.sync()
                self.send_event('evt_',
                    label="event",
                    timestamp=egi.ms_localtime(),
                    table=None)

        self.stop_netstation()


if __name__ == '__main__':
    exp = Experiment()
    exp.run()

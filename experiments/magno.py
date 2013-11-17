#!/usr/bin/env python

# standard
from __future__ import print_function, division
import random
import os

# vendor
from psychopy import visual, logging, core
import egi.simple as egi
# import egi.threaded as egi

# local
import controllers
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
        return self._control_box.wait_for_response()

    def run(self):
        raise NotImplementedError()

    def release(self):
        self._windows.close()
        core.quit()


class Magno(Experiment):

    def run(self):

        # Create stimuli
        segments = [random.randint(36, 60) for _ in range(324)]
        still_images = self.load_still_images(get_current_dir('img'))[:32]
        while len(still_images) < 32:
            still_images.append(random.choice(still_images))

        plan = utils.distribute(segments, still_images)

        horizontal_sine = visual.GratingStim(self._window,
                                             tex='sin',
                                             texRes=256,
                                             units='deg',
                                             sf=1.5,
                                             size=2)
        horizontal_sine.setUseShader(True)

        self.start_netstation()

        def move():
            # horizontal_sine.setPhase(4*t)
            horizontal_sine.setPhase(0.06666666666666667, '+')
            horizontal_sine.draw()

        def still():
            horizontal_sine.draw()

        self.timed_func(60 * 3, still)

        for current in plan:
            if not isinstance(current, int):
                # Show image
                self.timed_func(15, current.draw)

                # Wait for the response
                self.wait_for_response()
                self.send_event('resp', label="responded", description='Participant responded to cartoon', table=None)

                # Wait a random interval
                post_cartoon = random.randint(36, 60)
                self.timed_func(post_cartoon, still)
                self.send_event('move', label="moved", description='Sine grating finished moving', table={'frms': post_cartoon})
            else:
                # Move for 100 ms / 6 frames
                self.timed_func(6, move)
                self.send_event('stop', label="stopped", description='Sine grating finished pausing', table={'frms': 6})

                # Pause for however long plan says
                self.timed_func(current, still)
                self.send_event('move', label="moved", description='Sine grating finished moving', table={'frms': current})

        self.stop_netstation()


if __name__ == '__main__':
    exp = Magno(debug=True)
    exp.init_display('run-station', 800, 600)
    exp.init_controller('cedrus')
    exp.run()

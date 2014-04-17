
# standard
from __future__ import print_function, division
import os

# vendor
from psychopy import visual, logging, core, gamma
# import egi.simple as egi
import egi.threaded as egi

# local
from evoke import controllers
from evoke import monitors


class BaseExperiment(object):

    def __init__(self, debug=False, as_timing_test=False):
        self._monitor = None
        self._window = None
        self._netstation = None
        self._controller = None
        self._debug = debug
        self._as_timing_test = as_timing_test

        if debug:
            logging.console.setLevel(logging.DEBUG)
        else:
            logging.console.setLevel(logging.WARNING)

    def init_display(self, monitor, width=800, height=600):
        self._monitor = monitors.get(monitor)
        self._window = visual.Window(
            size=[width, height],
            monitor=self._monitor,
            winType='pyglet',
            waitBlanking=True,  # Default is True
            allowStencil=True,
            fullscr=False,  # True is faster
            allowGUI=False,
            rgb=(0, 0, 0),  # Gray
            gamma=2.2,
        )

        gamma.createLinearRamp(self._window, rampType=None)

        if self._debug:
            self._window.setRecordFrameIntervals(True)
            self._window._refreshThreshold = 1/60.0 + 0.004

    def init_controller(self, controller):
        self._controller = controllers.get(controller, window=self._window)

    def start_netstation(self):
        try:
            self._netstation = egi.Netstation()
            self._netstation.connect('10.0.0.42', 55513)
            self._netstation.BeginSession()
            self._netstation.sync()
            self._netstation.StartRecording()
        except Exception as exc:
            if self._debug:
                logging.debug('Unable to access Netstation: %s' % exc)
            else:
                raise

    def stop_netstation(self):
        self._netstation.StopRecording()
        # self._netstation.EndSession()
        self._netstation.disconnect()

    def send_event(self, key='evt_', label=None, description=None, table=None):
        self._netstation.send_event(key,
            label=label,
            timestamp=egi.ms_localtime(),
            description=description,
            table=table)

    def timed_func(self, frames, func=None):
        for _ in range(frames):
            if func:
                func()
                self._window.flip()
            else:
                self._window.flip(clearBuffer=False)

    def load_still_images(self, dirpath, pos=(0.0, 0.0), size=None):
        images = []
        for fname in os.listdir(dirpath):
            if fname.lower().endswith('.png') or fname.lower().endswith('.jpg'):
                img = self.load_still_image(os.path.join(dirpath, fname),
                                            pos, size)
                images.append(img)
            else:
                continue
        return images

    def load_still_image(self, fpath, pos=(0.0, 0.0), size=None):
        img = visual.ImageStim(self._window,
            image=fpath,
            pos=pos,
            units='deg')
        if size:
            img.size = 2
        return img

    def wait_for_response(self, buttons=None):
        return self._controller.wait_for_response(buttons=buttons)

    def release(self):
        self._windows.close()
        core.quit()

    def load_text_slide(self, text, pos=(0, 0)):
        slide = visual.TextStim(self._window,
            text=text,
            height=0.1,
            wrapWidth=1.5,
            font=('Times', 'Times New Roman'),
            color='black',
            pos=pos,
            alignHoriz='center',
            alignVert='center')
        return slide

    def load_fixation_cross(self, pos=(0, 0)):
        fixation = visual.TextStim(self._window,
            height=0.4,
            text=u'+',
            font=('Times', 'Times New Roman'),
            color='black',
            pos=pos,
            alignHoriz='center',
            alignVert='center')
        return fixation

    def load_timing_box(self, pos=(0, 0)):
        timing_box = visual.GratingStim(
            self._window,
            color=(1, 1, 1),
            colorSpace='rgb',
            pos=(-1, 1),
            sf=0)
        return timing_box

    def run(self):
        raise NotImplementedError()

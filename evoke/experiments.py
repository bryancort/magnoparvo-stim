
# standard
from __future__ import print_function, division
import os
import random

# vendor
from psychopy import visual, logging, core, gamma, sound, gui
# import egi.simple as egi
import egi.threaded as egi

# local
from evoke import controllers
from evoke import monitors
from evoke import _IO_HUB


class BaseExperiment(object):

    def __init__(self, debug=False, as_timing_test=False):
        self._monitor = None
        self._window = None
        self._netstation = None
        self._controller = None
        self._paused = False
        self._debug = debug
        self._as_timing_test = as_timing_test
        self._keyboard = None
        self._is_full_screen = None

        if debug:
            logging.console.setLevel(logging.DEBUG)
        else:
            logging.console.setLevel(logging.WARNING)

    def init_display(self, monitor, width=None, height=None, background_rgb=(0, 0, 0)):
        self._monitor = monitors.get(monitor)
        width = width or _IO_HUB.devices.display.getPixelResolution()[0]
        height = height or _IO_HUB.devices.display.getPixelResolution()[1]
        self._is_full_screen = (
            True if self._monitor.getSizePix() == (width, height)
            else False
        )
        background_rgb =(
            (-1, -1, -1) if self._as_timing_test
            else background_rgb
        )
        self._window = visual.Window(
            size=[width, height],
            monitor=self._monitor,
            winType='pyglet',
            waitBlanking=True,  # Better for vsync?
            allowStencil=True,
            fullscr=self._is_full_screen,
            allowGUI=not self._is_full_screen,
            rgb=background_rgb,
            # gamma=2.2,
            useFBO=True
        )
        gamma.createLinearRamp(self._window, rampType=None)

        self._mouse = controllers.get('mouse', window=self._window)
        self._keyboard = controllers.get('keyboard', window=self._window)
        if self._is_full_screen:
            self._mouse.hide()

        if self._debug:
            self._window.setRecordFrameIntervals(True)
            self._window._refreshThreshold = 1/60.0 + 0.004

    def init_controller(self, controller):
        self._controller = controllers.get(controller, window=self._window)

    def start_netstation(self, ip, port):
        try:
            self._netstation = egi.Netstation()
            self._netstation.initialize(ip, port)
            self._netstation.BeginSession()
            self._netstation.sync()
            self._netstation.StartRecording()
        except Exception as exc:
            if self._debug:
                logging.debug('Unable to access Netstation: %s' % exc)
                self._netstation = None
            else:
                raise

    def stop_netstation(self, close_netstation=False):
        if self._netstation is not None:
            self._netstation.StopRecording()
            if close_netstation:
                self._netstation.EndSession()
            self._netstation.finalize()

    def send_event(self, key='evt_', label=None, description=None, table=None):
        if self._netstation is not None:
            self._netstation.send_event(
                key,
                label=label,
                timestamp=egi.ms_localtime(),
                description=description,
                table=table
            )

    def timed_func(self, frames, func=None, start_event_args=None, end_event_args=None):
        if start_event_args is not None:
            self._window.callOnFlip(self.send_event, **start_event_args)
        for _ in range(frames):
            if func:
                func()
                self._window.flip()
            else:
                self._window.flip(clearBuffer=False)
        if end_event_args is not None:
            self.send_event(**end_event_args)
            
    def wait(self, ms):
        core.wait(ms / 1000.0)

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
            img.size = size
        return img

    def wait_for_response(self, buttons=None):
        if self._as_timing_test:
            return
        if self._controller is None:
            icontrol = self._keyboard
        else:
            icontrol = self._controller
        return icontrol.wait_for_response(buttons=buttons)

    def handle_pause_and_quit(self):
        self._check_pause_and_quit()
        while True:
            if self._paused:
                self._window.flip(clearBuffer=False)
                self._check_pause_and_quit()
            else:
                break

    def _check_pause_and_quit(self):
        for key in self._keyboard.poll():
            if key.lower() == 'p':
                self.toggle_pause()
            elif key.lower() == 'q' and self._paused:
                self.quit()

    def toggle_pause(self):
        self._paused = not self._paused

    def quit(self):
        self._window.close()
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
            pos=(0, 0),
            sf=0)
        return timing_box
        
    def get_participant_info(self):
        participant = {'subject':''}
        if not gui.DlgFromDict(participant, order=['subject', ]).OK:
            core.quit()
        return participant

    def pre_run(self):
        raise NotImplementedError()

    def run(self):
        raise NotImplementedError()

    def post_run(self):
        raise NotImplementedError()


class Frame(object):

    def __init__(self):
        pass

    def draw(self):
        pass

    def add_image(self, filename):
        pass

    def add_text(self, text):
        pass

    def set_interval(self, ms):
        pass


class SoundFile(object):

    def __init__(self, filepath):
        self._sound = sound.Sound(value=filepath)

    def play(self, log=True):
        self._sound.play(log=log)

    def stop(self, log=True):
        self._sound.stop(log=log)

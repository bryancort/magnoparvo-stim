#!/usr/bin/env python

from __future__ import random
import os
import random
from psychopy import visual, logging, event, core, monitors
import egi.simple as egi
# import egi.threaded as egi


class Experiment(object):

    def __init__(self):
        self._window = get_displayport()

    def _run(self):
        segments = [random.randint(600, 1000)/1000.0 for _ in range (200)]
        still_images = load_image_stims(self._window, '/home/gaelen/workspace/magnoparvo-stim/img')
        still_images = still_images * 10

        plan = segments + still_images
        random.shuffle(plan)

        #create a window to draw in
        logging.console.setLevel(logging.DEBUG)

        #window = get_displayport()

        horizontal_sine = visual.GratingStim(self._window,
                                             tex='sin',
                                             units='deg',
                                             sf=1.5,
                                             size=2)
        netstat = start_netstation()
        # ms_localtime = egi.egi_internal.ms_localtime
        # ms_localtime = egi.ms_localtime

        trialClock = core.Clock()
        # t = 0

        def move():
            t = trialClock.getTime()
            horizontal_sine.setPhase(4*t)
            horizontal_sine.draw()
            self._window.flip()

        for current in plan:
            if not isinstance(plan, float):
                # Show image
                current.draw()
                self._windows.flip()

                # Wait for the response
                pass

                # Wait a random interval
                timed_op(random.randint(600, 1000)/1000.0)
            else:

                # Move for 100 ms
                timed_op(0.1, lambda: move())

                # Pause for however long plan says
                timed_op(current)

                # optionally can perform additional synchronization # ns.sync()
                netstat.send_event('evt_',
                    label="event",
                    timestamp=egi.ms_localtime(),
                    table=None)

        stop_netstation(netstat)


def timed_op(secs, op=None):
    clock = core.Clock()
    stop_at = clock.getTime()
    clock.add(secs)

    while clock.getTime() <= stop_at:
        if op:
            op()
        else:
            pass


def get_monitor():
    mon = monitors.Monitor('Laptop')
    mon.setDistance(60)
    mon.setSizePix([1440, 900])
    mon.setWidth(13)
    return mon


def get_displayport(width=800, height=600):
    monitor = get_monitor()
    display = visual.Window(size=[width, height], monitor=monitor, allowGUI=False)
    return display


def start_netstation():
    netstat = egi.Netstation()
    netstat.connect('192.168.0.1', 55513)
    netstat.BeginSession()
    netstat.sync()
    netstat.StartRecording()
    return netstat


def stop_netstation(netstat):
    netstat.StopRecording()
    netstat.EndSession()
    netstat.disconnect()


def load_image_stims(window, dirpath, pos=(-0.5, 0.5)):
    images = []
    for fname in os.listdir(dirpath):
        images.append(window, os.path.join(dirpath, fname), pos)


def load_image_stim(window, fpath, pos=(-0.5, 0.5)):
    return visual.ImageStim(window, image=fpath, pos=pos)

if __name__ == '__main__':
    Experiment()._run()

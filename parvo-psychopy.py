#!/usr/bin/env python

from __future__ import random
import random
from psychopy import visual, logging, event, core, monitors
import egi.simple as egi
# import egi.threaded as egi


class Experiment(object):

    def __init__(self):
        self._monitor = get_monitor()
        self._window = get_displayport()

    def _run():
        segments = [random.randint(600, 1000) / 1000 for _ in range(200)]
        still_images = []  # ['image' for _ in range(6)]
        plan = segments + still_images
        random.shuffle(plan)

        #create a window to draw in
        logging.console.setLevel(logging.DEBUG)

        window = get_displayport()

        horizontal_sine = visual.GratingStim(window,
                                             tex='sin',
                                             units='deg',
                                             sf=1.5,
                                             size=2)
        netstat = start_netstation()
        # ms_localtime = egi.egi_internal.ms_localtime
        # ms_localtime = egi.ms_localtime

        trialClock = core.Clock()
        t = 0
        for part in range(300):

            if random.random() > .9:
                old = trialClock.getTime()
                trialClock.add(part)

                while trialClock.getTime() <= old:
                    pass

            t = trialClock.getTime()

            horizontal_sine.setPhase(4*t)  # drift at 1Hz
            horizontal_sine.draw()
            window.flip()

            # optionally can perform additional synchronization # ns.sync()
            # netstat.send_event( 'evt_', label="event", timestamp=egi.ms_localtime(), table = {'fld1' : 123, 'fld2' : "abc", 'fld3' : 0.042} )

            for keys in event.getKeys():
                if keys in ['escape', 'q']:
                    core.quit()

        stop_netstation(netstat)


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


if __name__ == '__main__':
    Experiment()._run()

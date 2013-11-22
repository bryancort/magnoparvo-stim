#!/usr/bin/env python

# standard
from __future__ import print_function, division
import random
import os
import sys
if sys.platform == 'win32':
    sys.path.append('C:\\gaelen\\magnoparvo-stim')

# vendor
from psychopy import visual

# local
from evoke.experiments import Experiment
from evoke import controllers
from evoke import monitors
from evoke import utils


def get_current_dir(append=None):
    path = os.path.dirname(os.path.abspath(__file__))
    if append:
        path = os.path.join(path, append)
    return path


class Magno(Experiment):

    def run(self):

        # Create stimuli
        segments = [random.randint(36, 60) for _ in range(320)]
        still_images = self.load_still_images(get_current_dir('img'))[:32]

        while len(still_images) < 32:
            still_images = 2 * still_images
        still_images = still_images[:32]
        random.shuffle(still_images)

        plan = utils.distribute(segments, still_images)

        horizontal_sine = visual.GratingStim(self._window,
                                             tex='sin',
                                             texRes=256,
                                             units='deg',
                                             sf=1.5,
                                             size=2)
        # horizontal_sine.setUseShader(True)

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

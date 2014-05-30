# standard
from __future__ import print_function, division
import random
import os

os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# vendor
from psychopy import visual

# local
from evoke.experiments import BaseExperiment
from evoke import utils


def get_current_dir(append=None):
    path = os.path.dirname(os.path.abspath(__file__))
    if append:
        path = os.path.join(path, append)
    return path


class Magno(BaseExperiment):

    def run(self):

        # Create stimuli
        segments = [random.randint(36, 60) for _ in range(320)]
        still_images = self.load_still_images(get_current_dir('img/set1'), size=2)[:32]

        while len(still_images) < 32:
            still_images = 2 * still_images
        still_images = still_images[:32]
        random.shuffle(still_images)

        plan = utils.distribute(segments, still_images) if not self._as_timing_test else segments

        horizontal_sine = visual.GratingStim(self._window,
                                             tex='sin',
                                             texRes=256,
                                             units='deg',
                                             sf=1.5,
                                             size=2)
        horizontal_sine.contrast = 0.04

        timing_box = None if not self._as_timing_test else self.load_timing_box()

        self.start_netstation()

        def move():
            timing_box and timing_box.draw()
            horizontal_sine.phase += 0.3425
            horizontal_sine.draw()

        def still():
            horizontal_sine.draw()

        event_args = {'key': 'move'}  # These will never change, so just create them once

        # Directions
        slide1 = self.load_text_slide("Welcome and thank you\nfor coming today.")
        slide2 = self.load_text_slide("You will see a box in the center of the "
            "screen or a Toy Story character. When you see a Toy Story "
            "character push the button on the button box.\n\nThat's all "
            "you have to do. When you are ready, push the button to "
            "begin.")
        self.timed_func(utils.ms_to_frames(4000, 60), slide1.draw)
        slide2.draw()
        self._window.flip()
        self.wait_for_response()

        # Fixation
        fixation = self.load_fixation_cross()
        self.timed_func(utils.ms_to_frames(2000, 60), lambda: fixation.draw())

        # Pre-stim
        self.timed_func(utils.ms_to_frames(random.randint(600, 1000), 60), still)

        self._window.setRecordFrameIntervals()
        trials = 1
        stills = 1
        for idx, current in enumerate(plan):
            if not isinstance(current, int):
                # Show image
                self.timed_func(15, current.draw)

                # Wait for the response
                self.wait_for_response()

                # Wait a random interval
                post_cartoon = random.randint(36, 60)
                print("Posting cartoon %s" %  still)
                self.timed_func(post_cartoon, still)
                stills += 1
            else:
                # Move for 100 ms / 6 frames
                self.timed_func(6, move, start_event_args=event_args)

                # Pause for however long plan says
                self.timed_func(current, still)
                trials += 1

        self.stop_netstation()


if __name__ == '__main__':
    exp = Magno(debug=False, as_timing_test=False)
    exp.init_display('run-station', 1920, 1200)
    exp.init_controller('cedrus')
    exp.run()


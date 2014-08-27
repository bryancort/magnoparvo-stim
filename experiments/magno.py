# standard
from __future__ import print_function, division
import random
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# vendor
from psychopy import visual

# local
from evoke.experiments import BaseExperiment, SoundFile
from evoke import utils


def get_current_dir(append=None):
    path = os.path.dirname(os.path.abspath(__file__))
    if append:
        path = os.path.join(path, append)
    return path


class Magno(BaseExperiment):

    def run(self):
        # Create stimuli
        segments = [random.choice([36, 42, 48, 54, 60]) for _ in range(320)]
        still_images = self.load_still_images(get_current_dir('img/set1'), size=2)[:32]

        # Opening / closing
        opening_audio = SoundFile(filepath=get_current_dir('audio/opening.wav'))
        opening_frame = self.load_still_image(fpath=get_current_dir('img/opening.png'))
        closing_audio = SoundFile(filepath=get_current_dir('audio/closing.wav'))
        closing_frame = self.load_still_image(fpath=get_current_dir('img/closing.png'))

        while len(still_images) < 32:
            still_images = 2 * still_images
        still_images = still_images[:32]
        random.shuffle(still_images)

        plan = utils.distribute(segments, still_images) if not self._as_timing_test else segments

        horizontal_sine = visual.GratingStim(
            self._window,
            tex='sin',
            texRes=128,
            units='deg',
            sf=1.5,
            size=2
        )
        horizontal_sine.contrast = 0.04
        horizontal_sine.setUseShaders(True)

        timing_box = None if not self._as_timing_test else self.load_timing_box()

        self.start_netstation('11.0.0.42', 55513)

        def move():
            timing_box and timing_box.draw()
            horizontal_sine.phase += 0.3425
            horizontal_sine.draw()

        def still():
            horizontal_sine.draw()
    
        # Directions
        # opening_audio.play()
        self.timed_func(1*60, lambda: opening_frame.draw())
        self.wait_for_response()

        # Fixation
        fixation = self.load_fixation_cross()
        self.timed_func(utils.ms_to_frames(2000, 60), lambda: fixation.draw())

        # Pre-stim
        self.timed_func(utils.ms_to_frames(random.randint(600, 1000), 60), still)

        self._window.setRecordFrameIntervals()
        trials = 0
        stills = 0
        for idx, current in enumerate(plan):
            self.handle_pause_and_quit()  # Need to move this to post flip hook
            if not isinstance(current, int):
                # Show image
                stills += 1
                self.timed_func(15, current.draw)

                # Wait for the response
                self.wait_for_response()

                # Wait a random interval
                post_cartoon = random.randint(36, 60)
                self.timed_func(post_cartoon, still)
            else:
                # Move for 100 ms / 6 frames
                trials += 1
                event_args = {
                    'key': 'move',
                    'label': "Move",
                    'description': 'Starting to move for 100ms',
                    'table': {'obs#': trials}
                }
                self.timed_func(6, move, start_event_args=event_args)

                # Pause for however long plan says
                self.timed_func(current, still)

        self.stop_netstation()

        # Closing
        # closing_audio.play()
        self.timed_func(15*60, lambda: closing_frame.draw())


if __name__ == '__main__':
    DEBUG = False
    exp = Magno(debug=DEBUG, as_timing_test=False)
    exp.init_display('pa241w', width=1024, height=800)
    # exp.init_display('mac-13in', 800, 600)
    exp.init_controller('cedrus')
    exp.run()

# standard
from __future__ import print_function, division
import random
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# vendor
import numpy
from psychopy import visual
from psychopy.tools.colorspacetools import dkl2rgb

# local
from evoke.experiments import BaseExperiment, SoundFile
from evoke import utils


def get_current_dir(append=None):
    path = os.path.dirname(os.path.abspath(__file__))
    if append:
        path = os.path.join(path, append)
    return path


def _create_square_texture(color1, color2, size=(128, 128)):
    """
    Creates a multidimensional numpy array of size using the two
    colors.
    """
    def _pow_of_2(num):
        return ((num & (num - 1)) == 0) and num > 0

    if not(size[0]) or not(size[1]):
        raise ValueError("Texture should be power of 2")

    texture = numpy.zeros((size[0], size[1], 3))
    for x in range(size[0]):
        for y in range(size[1]):
            if y >= (size[0] / 2):
                texture[x][y] = color2
            else:
                texture[x][y] = color1
    return texture


class Parvo(BaseExperiment):

    def run(self):
        # Create stimuli
        segments = [random.choice([36, 42, 48, 54, 60]) for _ in range(320)]
        still_images = self.load_still_images(get_current_dir('img/set2'))[:32]

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

        red_rgb = numpy.array((-0.78, -1, -1))
        green_rgb = numpy.array((-1, -0.875, -1))
        blue_rgb = numpy.array((-1, -1, 0.85))

        red_green_tex = _create_square_texture(red_rgb, green_rgb)
        blue_green_tex = _create_square_texture(blue_rgb, green_rgb)

        std_stim = visual.GratingStim(
            self._window,
            tex=blue_green_tex,
            texRes=128,
            units='deg',
            sf=5.25,
            size=2,
            colorSpace='rgb',
        )

        dev_stim = visual.GratingStim(
            self._window,
            tex=red_green_tex,
            texRes=128,
            units='deg',
            sf=5.25,
            size=2,
            colorSpace='rgb',
        )
        std_stim.setUseShaders(True)
        dev_stim.setUseShaders(True)

        timing_box = None if not self._as_timing_test else self.load_timing_box()

        self.start_netstation('11.0.0.42', 55513)

        # Directions
        # opening_audio.play()
        self.timed_func(1*60, lambda: opening_frame.draw())
        self.wait_for_response()

        # Fixation
        fixation = self.load_fixation_cross()
        self.timed_func(utils.ms_to_frames(2000, 60), fixation.draw)

        # Pre-stim
        self.timed_func(utils.ms_to_frames(random.randint(600, 1000), 60), std_stim.draw)

        trials = 0
        stills = 0
        for current in plan:
            self.handle_pause_and_quit()  # Need to move this to post flip hook
            if not isinstance(current, int):
                # Show image
                stills += 1
                self.timed_func(15, current.draw)

                # Wait for the response
                self.wait_for_response()

                # Wait a random interval
                post_cartoon = random.randint(36, 60)
                self.timed_func(post_cartoon, std_stim.draw)
            else:
                trials += 1
                event_args = {
                    'key': 'flsh',
                    'label': "Flash",
                    'description': 'Starting the red bar flash',
                    'table': {'obs#': trials}
                }
                # Flash for 100 ms / 6 frames
                self.timed_func(6, dev_stim.draw, start_event_args=event_args)
                stills += 1

                # Pause for however long plan says
                self.timed_func(current, std_stim.draw)

        self.stop_netstation()
        
        # Closing
        # closing_audio.play()
        self.timed_func(15*60, lambda: closing_frame.draw())


if __name__ == '__main__':
    DEBUG = True
    exp = Parvo(debug=DEBUG, as_timing_test=False)
    exp.init_display('pa241w')
    # exp.init_display('mac-13in', 800, 600)
    exp.init_controller('cedrus')
    exp.run()

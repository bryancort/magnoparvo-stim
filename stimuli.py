
# standard
import colorsys
from collections import namedtuple
import math
import random
import time

# local
import PresPy

STIM_WIDTH = 640
STIM_HEIGHT = 480
BARS_COUNT = 64

Position = namedtuple('Position', ['x', 'y'])

# Create presentation controller
pc = PresPy.Presentation_control()

# Set headers
pc.set_header_parameter("scenario_type", "trials")
pc.set_header_parameter('default_background_color', '0,0,0')
# pc.set_header_parameter('screen_height', 768)
# pc.set_header_parameter('screen_width', 1024)
# pc.set_header_parameter('screen_bit_depth', 32)
pc.set_header_parameter('write_codes', True)
# pc.set_header_parameter('pulse_width', 8)
# pc.set_header_parameter('active_buttons', 4)
# pc.set_header_parameter('button_codes', '1,2,101,101')

# Open experiment file
pc.open_experiment("C:\\gaelen-pypres\my-experiment.exp")
# pc.set_subject_id(1)

# Run scenario
scene = pc.run(0)  # (pc.PRESCONTROL1_SHOW_STATUS | pc.PRESCONTROL1_USER_CONTROL | pc.PRESCONTROL1_WRITE_OUTPUT, 0)

nv = lambda x: x / 239.0

RED_RGB = PresPy.rgb_color(colorsys.hls_to_rgb(0.0, 0.5, 1.0))
GREEN_RGB = PresPy.rgb_color(colorsys.hls_to_rgb(0.334, 0.5, 1.0))
BLUE_RGB = PresPy.rgb_color(colorsys.hls_to_rgb(0.667, 0.5, 1.0))


class StripeColors(object):

    def __init__(self, colors, interval):
        """
        Color should be a list of RGB colors.
        Interval should be a float or a function that returns a float
        """
        self.colors = colors
        self._interval = interval

    @property
    def interval(self):
        return self._interval() if callable(self._interval) else self._interval


bluegreen = StripeColors(colors=(BLUE_RGB, GREEN_RGB), interval=lambda: random.randint(600, 1000) / 1000.0)
redgreen = StripeColors(colors=(RED_RGB, GREEN_RGB), interval=0.1)

bar_colors = (bluegreen, redgreen)


def make_bars(scene, width, height, num_bars, colors):
    bar_width = width / num_bars
    bar_map = zip(range(num_bars), colors * int(math.ceil(num_bars / len(colors))))
    far_left = -width / 2.0
    for bar_idx, color in bar_map:
        bar = scene.box(width=bar_width, height=height, color=color)
        pos = Position(int(bar_idx * bar_width + far_left), 0)
        yield bar, pos


for _ in range(60):
    for stripes in bar_colors:
        pic = scene.picture()
        for bar, pos in make_bars(scene, STIM_WIDTH, STIM_HEIGHT, BARS_COUNT, stripes.colors):
            pic.add_part(bar, pos.x, pos.y)
        pic.present()
        time.sleep(stripes.interval)

# Cleanup (Is this really necessary?)
del scene
del pc


# standard
import colorsys
from collections import namedtuple
import math
import random
import time

# local
import PresPy

STIM_WIDTH = 1024
STIM_HEIGHT = 768
BARS_COUNT = 64

Position = namedtuple('Position', ['x', 'y'])

# Create presentation controller
pc = PresPy.Presentation_control()

# Set headers
# pc.set_header_parameter("scenario_type", "trials")
# pc.set_header_parameter('default_background_color', '0,0,0')
# pc.set_header_parameter('screen_height', 768)
# pc.set_header_parameter('screen_width', 1024)
# pc.set_header_parameter('screen_bit_depth', 32)
# pc.set_header_parameter('write_codes', True)
# pc.set_header_parameter('pulse_width', 8)
# pc.set_header_parameter('active_buttons', 4)
# pc.set_header_parameter('button_codes', '1,2,101,101')

# Open experiment file
pc.open_experiment("C:\\gaelen-pypres\my-experiment.exp")
pc.set_subject_id('number 1')

# Run scenario
scene = pc.run(0)  # (pc.PRESCONTROL1_SHOW_STATUS | pc.PRESCONTROL1_USER_CONTROL | pc.PRESCONTROL1_WRITE_OUTPUT, 0)

nv = lambda x: x / 239.0

red = PresPy.rgb_color(colorsys.hls_to_rgb(0.0, 0.5, 1.0))
green = PresPy.rgb_color(colorsys.hls_to_rgb(0.334, 0.5, 1.0))
blue = PresPy.rgb_color(colorsys.hls_to_rgb(0.667, 0.5, 1.0))
bar_colors = ((red, green), (red, blue),)

#green = scen.rgb_color(0, 255, 0)  # Maybe PresPy.rgb_color()
# box_red = scene.box(1024, 768, red)
# box_green = scene.box(1024, 768, green)
# box_blue = scene.box(1024, 768, blue)


def make_bars(scene, width, height, num_bars, colors):
    bar_width = width / num_bars
    bar_map = zip(range(num_bars), colors * int(math.ceil(num_bars / len(colors))))
    for bar_idx, color in bar_map:
        bar = scene.box(width=bar_width, height=height, color=color)
        pos = Position(int(bar_idx * bar_width - bar_width / 2), height // 2)
        yield bar, pos


for _ in range(15):
    for colors in bar_colors:
        pic = scene.picture()
        for bar, pos in make_bars(scene, STIM_WIDTH, STIM_HEIGHT, BARS_COUNT, colors):
            pic.add_part(bar, pos.x, pos.y)
        pic.present()
        time.sleep(random.random() * 1.5)

# Cleanup (Is this really necessary?)
del scene
del pc

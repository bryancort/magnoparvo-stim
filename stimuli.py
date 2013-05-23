
# standard
from __future__ import division
import colorsys
from collections import namedtuple
import math

# local
import PresPy

Position = namedtuple('Position', ['x', 'y'])


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

    def __len__(self):
        return len(self.colors)

    @property
    def interval(self):
        return self._interval() if callable(self._interval) else self._interval


def make_bars(scenario, width, height, num_bars, colors):
    bar_width = width / num_bars
    bar_map = zip(range(num_bars), colors * int(math.ceil(num_bars / len(colors))))
    far_left = -width / 2.0
    for bar_idx, color in bar_map:
        bar = scenario.box(width=bar_width, height=height, color=color)
        pos = Position(int(bar_idx * bar_width + far_left), 0)
        yield bar, pos


def make_sine_colors(width, phase=(0, 0, 0), amp=128, mid=127):
    colors = []
    interval = 2 * math.pi / width
    for x in range(width):
        rv = math.sin(interval * x + phase[0]) * amp + mid
        gv = math.sin(interval * x + phase[1]) * amp + mid
        bv = math.sin(interval * x + phase[2]) * amp + mid
        colors.append(PresPy.rgb_color(_rgb_clamp(rv), _rgb_clamp(gv), _rgb_clamp(bv)))
    return colors


def _rgb_clamp(v):
    return int(max(min(255, v), 0))

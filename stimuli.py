
# standard
from __future__ import division, print_function
import colorsys
from collections import namedtuple
import math
import time

# local
import PresPy

Position = namedtuple('Position', ['x', 'y'])


RED_RGB = PresPy.rgb_color(colorsys.hls_to_rgb(0.0, 0.5, 1.0))
GREEN_RGB = PresPy.rgb_color(colorsys.hls_to_rgb(0.334, 0.5, 1.0))
BLUE_RGB = PresPy.rgb_color(colorsys.hls_to_rgb(0.667, 0.5, 1.0))


class Experiment(object):

    def __init__(self, exp_path, **headers):
        self._control = PresPy.Presentation_control()
        self._control.open_experiment(exp_path)
        self._scenario = None

        for header, val in headers.items():
            self.set_header(header, val)

    def close(self):
        if self._scenario:
            del self._scenario
        del self._control

    def new_scenario(self):
        self._scenario = self._control.run(0)
        # Consider (pc.PRESCONTROL1_SHOW_STATUS | pc.PRESCONTROL1_USER_CONTROL | pc.PRESCONTROL1_WRITE_OUTPUT, 0)
        return self._scenario

    def set_header(self, header, value):
        self._control.set_header_parameter(header, value)

    def set_subject(self, subject_id):
        self._control.set_subject_id(1)


class Scenario(object):

    def __init__(self):
        pass


class ColorFunction(object):

    def __init__(self, func, input_min, input_max, interval_rate=1):
        self._func = func
        self.input_range = (input_min, input_max)
        self._expand_offset = 0
        self._interval_rate = interval_rate

    def get_color(self, val, *args):
        if val < self.input_range[0] or val > self.input_range[1]:
            print('Warning: ColorFunction input value %r is outside of range %r' % (val, self.input_range))
        return self._func(val, *args)

    def expand(self, pixels_part, pixels_total):
        colors = []
        offset = self._expand_offset
        interval = (self.input_range[1] - self.input_range[0]) / pixels_part
        print(pixels_part, pixels_total, interval)

        for pixel in range(pixels_part):
            colors.append(self.get_color((offset + pixel) * interval))

        self._expand_offset += self._interval_rate
        return colors


class ColorList(object):

    def __init__(self, colors):
        self._colors = tuple(colors)

    def __len__(self):
        return len(self._colors)

    def __getitem__(self, i):
        return self._colors[i]


class Pattern(object):

    def __init__(self, colors, num_parts, interval):
        """
        Color should be a list of RGB colors.
        Interval should be a float or a function that returns a float
        """
        self.colors = colors
        self.num_parts = num_parts
        self._interval = interval

    def __len__(self):
        return len(self.colors) if isinstance(self.colors, ColorList) else None

    @property
    def interval(self):
        return self._interval() if callable(self._interval) else self._interval

    def get_parts(self, *args, **kw):
        raise NotImplemented('Subclass should implement this method.')


class RadialPattern(Pattern):

    def get_parts(self, scenario, width, height):
        num_parts = self.num_parts or width
        part_width = width / 2 // num_parts
        part_height = height / 2 // num_parts

        if isinstance(self.colors, ColorList):
            expanded_colors = (self.colors._colors * int(math.ceil(num_parts / len(self.colors))))[:num_parts]
        elif isinstance(self.colors, ColorFunction):
            expanded_colors = self.colors.expand(part_width, width)

        for idx, color in reversed(list(enumerate(expanded_colors))):
            eclipse = scenario.ellipse_graphic()
            eclipse.eclipse_width = idx*part_width
            eclipse.eclipse_height = idx*part_height
            eclipse.color = color
            pos = Position(0, 0)
            yield eclipse, pos


class HorizontalPattern(Pattern):

    def get_parts(self, scenario, width, height):
        num_parts = self.num_parts or width
        part_width = width // num_parts

        if isinstance(self.colors, ColorList):  # fix .colors.colors
            expanded_colors = (self.colors._colors * int(math.ceil(num_parts / len(self.colors))))[:num_parts]

            left_edge = -width // 2.0
            for bar_idx, color in enumerate(expanded_colors):
                bar = scenario.box(width=part_width, height=height, color=color)
                pos = Position(int(bar_idx * part_width + left_edge), 0)
                yield bar, pos

        elif isinstance(self.colors, ColorFunction):
            expanded_colors = self.colors.expand(part_width, width)

            left_edge = -width // 2.0
            for bar_idx, color in enumerate(expanded_colors):
                bar = scenario.box(width=1, height=height, color=color)
                pos = Position(int(bar_idx * 1 + left_edge), 0)
                yield bar, pos


class VerticalPattern(Pattern):
    pass


class Display(object):

    def __init__(self, width, height, patterns):
        self.width = width
        self.height = height
        self.patterns = tuple(patterns) if isinstance(patterns, (list, tuple)) else (patterns, )
        self._next_pattern_idx = 0

    def show(self, scenario):
        pattern = self.patterns[self._next_pattern_idx]
        pic = scenario.picture()
        for part, pos in pattern.get_parts(scenario, self.width, self.height):
            pic.add_part(part, pos.x, pos.y)
        pic.present()
        self._next_pattern_idx = (self._next_pattern_idx + 1) % len(self.patterns)
        #time.sleep(pattern.interval)


def get_sine_color(x, phase=(0, 0, 0), amp=128, mid=127):
    """
    x should be between 0 and 2pi
    """
    rv = math.sin(x + phase[0]) * amp + mid
    gv = math.sin(x + phase[1]) * amp + mid
    bv = math.sin(x + phase[2]) * amp + mid
    return PresPy.rgb_color(_rgb_clamp(rv), _rgb_clamp(gv), _rgb_clamp(bv))


def _rgb_clamp(v):
    return int(max(min(255, v), 0))

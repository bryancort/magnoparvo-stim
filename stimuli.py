
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
        self._expand_call_count = 0
        self._interval_rate = interval_rate
        self._generated_colors = None

    def get_color(self, val, *args):
        if val < self.input_range[0] or val > self.input_range[1]:
            print('Warning: ColorFunction input value %r is outside of range %r' % (val, self.input_range))
        return self._func(val, *args)

    def __lshift__(self, shift):
        self._generated_colors << shift

    def __rshift__(self):
        self._generated_colors >> shift

    def expand(self, pixels_part, pixels_total):
        if not self._generated_colors:
            colors = []
            interval = (self.input_range[1] - self.input_range[0]) / pixels_part

            for _ in range(int(math.ceil(pixels_total / pixels_part))):
                for pixel in range(pixels_part):
                    colors.append(self.get_color(pixel * interval))

            self._generated_colors = ColorList(colors)
        else:
            #self._generated_colors = self._generated_colors[-self._interval_rate:] + self._generated_colors[:-self._interval_rate]
            self._generated_colors >> self._interval_rate

        self._expand_call_count += 1
        return self._generated_colors


class ColorList(object):

    def __init__(self, colors):
        self._colors = tuple(colors)

    def __len__(self):
        return len(self._colors)

    def __getitem__(self, i):
        return self._colors[i]

    def __lshift__(self, shift):
        if not isinstance(shift, int):
            raise ValueError('<< value needs to be an int')
        self._colors = self._colors[shift:] + self._colors[:shift]

    def __rshift__(self, shift):
        if not isinstance(shift, int):
            raise ValueError('>> value needs to be an int')
        self._colors = self._colors[-shift:] + self._colors[:-shift]


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
            ellipse = scenario.ellipse_graphic()
            ellipse.set_dimensions(ellipse_width=idx*part_width, ellipse_height=idx*part_height)
            ellipse.set_size(width=idx*part_width, height=idx*part_height)
            ellipse.set_color(color)
            pos = Position(0, 0)
            yield ellipse, pos


class HorizontalPattern(Pattern):

    _generated_boxes = []

    def get_parts(self, scenario, width, height):
        num_parts = self.num_parts or width
        part_width = width // num_parts

        if not self._generated_boxes:
            if isinstance(self.colors, ColorList):
                expanded_colors = (self.colors._colors * int(math.ceil(num_parts / len(self.colors))))[:num_parts]

            elif isinstance(self.colors, ColorFunction):
                expanded_colors = self.colors.expand(part_width, width)
                part_width = 1

            left_edge = -width // 2.0
            for bar_idx, color in enumerate(expanded_colors):
                bar = scenario.box(width=part_width, height=height, color=color)
                pos = Position(int(bar_idx * part_width + left_edge), 0)
                self._generated_boxes.append(bar)
                yield bar, pos
        else:
            left_edge = -width // 2.0
            pixel_rate = self.colors._interval_rate
            self._generated_boxes = self._generated_boxes[-pixel_rate:] + self._generated_boxes[:-pixel_rate]
            for idx, box in enumerate(self._generated_boxes):
                pos = Position(int(idx + left_edge), 0)
                yield box, pos


class VerticalPattern(Pattern):
    pass


class Display(object):

    def __init__(self, width, height, patterns):
        self.width = width
        self.height = height
        self.patterns = tuple(patterns) if isinstance(patterns, (list, tuple)) else (patterns, )
        self._next_pattern_idx = 0

    def show(self, scenario):
        start = time.time()
        pattern = self.patterns[self._next_pattern_idx]
        start_pic = time.time()
        pic = scenario.picture()
        start_gen = time.time()
        for part, pos in pattern.get_parts(scenario, self.width, self.height):
            pic.add_part(part, pos.x, pos.y)
        start_present = time.time()
        pic.present()
        self._next_pattern_idx = (self._next_pattern_idx + 1) % len(self.patterns)
        end = time.time()
        total = end - start
        #print('\nTotal:', total, '\nPicture:', start_gen-start_pic, '\nGenerate:', start_present-start_gen, '\nPresent:', end-start_present)
        if total < pattern.interval:
            time.sleep(pattern.interval-total)
        else:
            print('Running to slow to keep up with interval. actual: %r, expected: %r' % (total, pattern.interval))


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

# trial {
#    trial_duration = stimuli_length;
#    stimulus_event {
#       picture pic1;
#       duration = 200;
#       code = "switch";
# #      port_code=99;port=2;
#    } main_stim;
# } main_trial;

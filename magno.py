# Motion

# standard
from __future__ import division
import math

# local
from stimuli import Experiment, HorizontalPattern, ColorFunction, Display
from stimuli import get_sine_color

STIM_WIDTH = 800
STIM_HEIGHT = 600
WAVE_COUNT = 6

SINE_PHASE = (0, 0, 0)


# Create presentation controller
exp = Experiment('C:\\gaelen-pypres\magnoparvo-stim\my-experiment.exp',
                 scenario_type="trials",
                 default_background_color='0,0,0',
                 default_draw_mode='draw_mode_standard',
                 # screen_height=768,
                 # screen_width=1024,
                 # screen_bit_depth=32,
                 write_codes=True,
                 # pulse_width=8,
                 # active_buttons=4,
                 # button_codes='1,2,101,101'
                 )


# Run scenario
scenario = exp.new_scenario()
time_interval = 0.1
pixels_per_interval = int(math.ceil(STIM_WIDTH / WAVE_COUNT / time_interval))
sine_patt = HorizontalPattern(colors=ColorFunction(get_sine_color, 0, 2*math.pi, interval_rate=pixels_per_interval),
                              num_parts=WAVE_COUNT,
                              interval=time_interval)


display = Display(STIM_WIDTH, STIM_HEIGHT, sine_patt)

for _ in range(60):
    display.show(scenario)

exp.close()

# Color

# standard
import random

# local
from stimuli import Experiment, RadialPattern, HorizontalPattern, ColorList, Display
from stimuli import RED_RGB, GREEN_RGB, BLUE_RGB

STIM_WIDTH = 640
STIM_HEIGHT = 480
BARS_COUNT = 32


# Create presentation controller
exp = Experiment('C:\\gaelen-pypres\magnoparvo-stim\my-experiment.exp',
                 scenario_type="trials",
                 default_background_color='0,0,0',
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

bluegreen_patt = RadialPattern(colors=ColorList([BLUE_RGB, GREEN_RGB]),
                                   num_parts=BARS_COUNT,
                                   interval=lambda: random.randint(600, 1000) / 1000.0)
redgreen_patt = RadialPattern(colors=ColorList([RED_RGB, GREEN_RGB]),
                                  num_parts=BARS_COUNT,
                                  interval=0.1)

patterns = (bluegreen_patt, redgreen_patt)

display = Display(STIM_WIDTH, STIM_HEIGHT, patterns)

for _ in range(60):
    display.show(scenario)

exp.close()

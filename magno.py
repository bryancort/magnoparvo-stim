# Motion

# standard
import random
import time

# local
import PresPy
from stimuli import StripeColors, make_bars, make_sine_colors

STIM_WIDTH = 640
STIM_HEIGHT = 480
BARS_COUNT = 64

SINE_PHASE = (0, 0, 0)


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
scenario = pc.run(0)  # (pc.PRESCONTROL1_SHOW_STATUS | pc.PRESCONTROL1_USER_CONTROL | pc.PRESCONTROL1_WRITE_OUTPUT, 0)

#bluegreen = StripeColors(colors=(BLUE_RGB, GREEN_RGB), interval=lambda: random.randint(600, 1000) / 1000.0)

gradients = make_sine_colors(STIM_WIDTH / BARS_COUNT, phase=SINE_PHASE)

bar_colors = []
for idx in range(BARS_COUNT):
    gradients = gradients[1:] + gradients[0]
    bar_colors.append(StripeColors(colors=gradients, interval=0.1))


for _ in range(60):
    for stripes in bar_colors:
        pic = scenario.picture()
        for bar, pos in make_bars(scenario, STIM_WIDTH, STIM_HEIGHT, BARS_COUNT, stripes.colors):
            pic.add_part(bar, pos.x, pos.y)
        pic.present()
        time.sleep(stripes.interval)

# Cleanup (Is this really necessary?)
del scenario
del pc

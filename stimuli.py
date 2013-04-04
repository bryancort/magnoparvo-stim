
# standard
import colorsys
import time

# local
import PresPy

# Create presentation controller
pc = PresPy.Presentation_control()

# Set headers
pc.set_header_parameter("scenario_type", "trials")
pc.set_header_parameter('default_background_color', '0,0,0')
pc.set_header_parameter('screen_height', 768)
pc.set_header_parameter('screen_width', 1024)
pc.set_header_parameter('screen_bit_depth', 32)
pc.set_header_parameter('write_codes', True)
pc.set_header_parameter('pulse_width', 8)
pc.set_header_parameter('active_buttons', 4)
pc.set_header_parameter('button_codes', '1,2,101,101')

# Open experiment file
pc.open_experiment("C:\\my_experiment.exp")

# Run scenario
scen = pc.run(0)  # (pc.PRESCONTROL1_SHOW_STATUS | pc.PRESCONTROL1_USER_CONTROL | pc.PRESCONTROL1_WRITE_OUTPUT, 0)
#surface1 = scen.graphic_surface(100, 100)

# # Create display thingie
# txt1 = scen.text()
# txt1.set_font_size(48)
# txt1.set_caption("Hello world!", redraw=True)

# pic1 = scen.picture()
# pic1.add_part(txt1, 0, 0)

# for i in range(100):
#     pic1.set_part_y(1, 50 - i)
#     pic1.present()

nv = lambda x: x / 239.0

red = PresPy.rgb_color(colorsys.hls_to_rgb(0.0, 0.5, 1.0))
green = PresPy.rgb_color(colorsys.hls_to_rgb(0.334, 0.5, 1.0))
blue = PresPy.rgb_color(colorsys.hls_to_rgb(0.667, 0.5, 1.0))

#green = scen.rgb_color(0, 255, 0)  # Maybe PresPy.rgb_color()
box_red = scen.box(1024, 768, red)
box_green = scen.box(1024, 768, green)
box_blue = scen.box(1024, 768, blue)

pic = scen.picture()
pic.add_part(box_red)
pic.present()
time.sleep(5)
pic.add_part(box_green)
pic.present()
time.sleep(5)
pic.add_part(box_blue)
pic.present()
time.sleep(5)

# Cleanup (Is this really necessary?)
del scen
del pc

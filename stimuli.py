import PresPy

# Create presentation controller
pc = PresPy.Presentation_control()
pc.set_header_parameter("scenario_type", "trials")
pc.open_experiment("C:\\my_experiment.exp")

# Create scenario
scen = pc.run(0)  # (pc.PRESCONTROL1_SHOW_STATUS | pc.PRESCONTROL1_USER_CONTROL | pc.PRESCONTROL1_WRITE_OUTPUT, 0)
#surface1 = scen.graphic_surface(100, 100)

# Create video
txt1 = scen.text()
txt1.set_font_size(48)
txt1.set_caption("Hello world!", redraw=True)

pic1 = scen.picture()
pic1.add_part(txt1, 0, 0)

for i in range(100):
    pic1.set_part_y(1, 50 - i)
    pic1.present()

# Cleanup (Is this really necessary?)
del scen
del pc


from __future__ import print_function, division
import math

dist = float(input('Distance between center of eyes and screen in centimeters: '))
deg_w = float(input('Width of box in degrees: '))
deg_h = float(input('Height of box in degrees: '))

def convert_monitor_res(res):
    parts = res.split('x')
    if len(parts) != 2:
        raise ValueError('Resolution format needs to be WIDTHxHEIGHT')
    return (float(parts[0]), float(parts[1]))

mon_res = input('Pixel resolution of monitor [default is 1440x900]: ') or '1440x900'
mon_res = convert_monitor_res(mon_res)

mon_w = float(input('Width of monitor in centimeters: '))
mon_h = float(input('Height of monitor in centimeters: '))

print('\n-- Input --')
print('Distance:%.2f\n%.2f\u00B0x%.2f\u00B0 on %dx%d monitor' % (dist, deg_w, deg_h,
                                                                 mon_res[0], mon_res[1]))

ratio_w = mon_res[0] / mon_w
ratio_h = mon_res[1] / mon_h
print('Monitor width: %.2f px per cm\nMonitor height: %.2f px per cm\n' % (ratio_w, ratio_h))

# Formula: tan(theta) * distance * 2
stim_w = math.tan(math.radians(deg_w)) * dist * 2
stim_h = math.tan(math.radians(deg_h)) * dist * 2

print('-- Result --')
print('Stimuli should be %.2fx%.2f cm' % (stim_w, stim_h))
print('Stimuli should be %dx%d px' % (stim_w * ratio_w, stim_h * ratio_h))

if stim_w == stim_h and (stim_w * ratio_w != stim_h * ratio_h):
    print(' ** Note: It is unusual for monitors to have different vertical '
          'and horizontal pixel densities. The stimuli pixel width and height '
          'should probably be equal.')


# standard
from __future__ import print_function
import time

# vendor
import pyxid


devices = []
while not devices:
    devices = pyxid.get_xid_devices()
    time.sleep(0.25)

device = devices[0]
print('Using devices', device)
if device.is_response_device():
    device.reset_base_timer()
    device.reset_rt_timer()

print('Listening for button pushes')
while True:
    device.poll_for_response()
    for response in device.response_queue:
        print("Response is", device.get_next_response())
    device.clear_response_queue()
    time.sleep(0.1)

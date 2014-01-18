
# standard
from __future__ import print_function
import time

# vendor
import pyxid


devices = pyxid.get_xid_devices()
device = devices[0]
if device.is_response_device():
    device.reset_base_timer()
    device.reset_rt_timer()

while True:
    device.poll_for_response()
    print("Queue on size", device.response_queue_size())
    print("Response is", device.get_next_response())
    device.clear_response_queue()
    time.sleep(5)

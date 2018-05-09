from fri3d.blynk import Blynk
from fri3d.net import Wifi

from machine import Pin

import _thread as thread
import time

# -- initialize the LED pin
LED = Pin(2, Pin.OUT)

# -- Connect to wifi
wifi = Wifi("area3001", "")
wifi.connect()
wifi.wait_until_connected()
print("Wifi connected as %s" % wifi.ip())

blynk = Blynk("", "iot.area3001.com", 8080)


def v4_write_handler(value):
    print('V4: ', value)


blynk.add_virtual_pin(4, write=v4_write_handler)

thread.start_new_thread("blynk", blynk.run, ())
time.sleep(3)
blynk.virtual_write(0, '     ESP32')
blynk.virtual_write(1, '  MicroPython')
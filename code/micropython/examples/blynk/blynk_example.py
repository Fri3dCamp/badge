from fri3d.blynk import Blynk
from fri3d.badge import Wifi

import _thread as thread
import time

# -- Connect to wifi
wifi = Wifi("area3001", "")
wifi.connect()
wifi.wait_until_connected()
print("Wifi connected as %s" % wifi.ip())

blynk = Blynk("", "iot.area3001.com", 8080)

blynk.add_virtual_pin(4, write=lambda value: {
    print('Servo: ', value)
})

thread.start_new_thread("blynk", blynk.run, ())
time.sleep(3)
blynk.virtual_write(0, '     ESP32')
blynk.virtual_write(1, '  MicroPython')
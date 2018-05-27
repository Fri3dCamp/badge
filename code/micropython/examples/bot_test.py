from fri3d.kits import robot
from fri3d import badge
from fri3d.blynk import Blynk

import _thread as thread
import time

eyes = robot.eyes()
wifi = badge.wifi()

# -- Connect to wifi
wifi.connect("ORBI28", "phobicviolin114")
wifi.wait_until_connected()
print("Wifi connected as %s" % wifi.ip())

# -- Blynk
# blynk = Blynk("44c2b93ff14548148cbe0bb9787eeaff", "iot.area3001.com", 8080)


# def servo_left_handler(value):
#     robot.turn_left()
#
#
# def servo_front_handler(value):
#     robot.step_forward()
#
#
# def servo_right_handler(value):
#     robot.turn_right()
#
#
# def servo_back_handler(value):
#     robot.step_backward()
#
#
# def servo_reset_handler(value):
#     robot.reset_legs()
#
#
# blynk.add_virtual_pin(4, write=servo_front_handler)
# blynk.add_virtual_pin(5, write=servo_left_handler)
# blynk.add_virtual_pin(6, write=servo_back_handler)
# blynk.add_virtual_pin(7, write=servo_right_handler)
# blynk.add_virtual_pin(8, write=servo_reset_handler)
#
# thread.start_new_thread("blynk", blynk.run, ())
# time.sleep(3)

from fri3d.ext import Servo
import utime

# -- create a new servo instance
s1 = Servo(25)

# -- center the servo
s1.angle(90)

# -- move the servo from left to right
while True:
    # -- move the servo to 50 degrees and sleep for a second
    s1.angle(50)
    utime.sleep(1)

    # -- move the servo to 130 degrees and sleep for a second
    s1.angle(130)
    utime.sleep(1)

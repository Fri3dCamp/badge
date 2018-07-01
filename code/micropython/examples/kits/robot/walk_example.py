from fri3d.kits import robot
from fri3d import Badge
import utime

b = Badge(enable_eyes=True)
legs = robot.legs()

while True:
    utime.sleep(2)
    b.eyes.blink()

    utime.sleep_ms(500)
    legs.say_hello_left()

    utime.sleep_ms(500)
    b.eyes.blink()

    utime.sleep_ms(250)
    legs.turn_left()

    b.eyes.blink()
    utime.sleep(1)
    b.eyes.blink()

    legs.turn_right()
    legs.turn_right()

    utime.sleep(1)
    b.eyes.blink()

    utime.sleep_ms(250)
    legs.turn_left()

    utime.sleep(1)
    b.eyes.blink()

    legs.shake_right()
    b.eyes.blink()

from fri3d.kits import robot
import utime

l = robot.legs()
e = robot.eyes()

while True:
    utime.sleep(2)
    e.blink()

    utime.sleep_ms(500)
    l.say_hello_left()

    utime.sleep_ms(500)
    e.blink()

    utime.sleep_ms(250)
    l.turn_left()

    e.blink()
    utime.sleep(1)
    e.blink()

    l.turn_right()
    l.turn_right()

    utime.sleep(1)
    e.blink()

    utime.sleep_ms(250)
    l.turn_left()

    utime.sleep(1)
    e.blink()

    l.shake_right()
    e.blink()

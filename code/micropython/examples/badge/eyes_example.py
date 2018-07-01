from fri3d import Badge
import utime
import machine

b = Badge()

while True:
    b.eyes.pupil(machine.random(5), machine.random(3))

    # -- sleep for 100 millis
    utime.sleep_ms(3000)
    b.eyes.blink()
    utime.sleep_ms(3000)

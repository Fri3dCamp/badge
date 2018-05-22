from fri3d import badge
import utime

while True:
    s = badge.accelero().sample(True)
    print("x[%.3f]\ty[%.3f]\tz[%.3f]" % (s['x'], s['y'], s['z']))
    utime.sleep_ms(250)

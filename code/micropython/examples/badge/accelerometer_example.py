from fri3d import badge
import utime

while True:
    s = badge.accelero().sample(True)
    print("x[%.1f]\ty[%.1f]\tz[%.1f]" % (s['x'], s['y'], s['z']))
    utime.sleep_ms(250)

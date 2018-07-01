from fri3d import Badge
import utime

b = Badge(enable_accelero=True)

while True:
    s = b.accelero.sample(True)
    print("x[%.1f]\ty[%.1f]\tz[%.1f]" % (s['x'], s['y'], s['z']))
    utime.sleep_ms(250)

from fri3d import badge
import utime

# -- go through the 0 - 4100Hz range
while True:
    # -- go from 0Hz to 4100Hz in steps of 50Hz at a time.
    for i in range(0, 4100, 50):
        badge.buzzer().set(i)
        utime.sleep_ms(50)

    # -- go from 4100Hz back to 0Hz in steps of 50Hz at a time.
    for i in range(4100, 0, -50):
        badge.buzzer().set(i)
        utime.sleep_ms(50)

from fri3d.kits import robot
import utime
import array

eyes = robot.eyes()

e = [
    array.array('I', [127, 127, 127, 127, 127]),
    array.array('I', [8, 28, 28, 28, 8]),
    array.array('I', [0, 28, 20, 28, 0]),
    array.array('I', [62, 65, 73, 65, 62]),
]

to_render = 0

while True:
    to_render %= 4

    print("Rendering eye ", to_render)
    eyes.draw_pupil(e[to_render], 0, 1)

    utime.sleep(3)

    to_render += 1

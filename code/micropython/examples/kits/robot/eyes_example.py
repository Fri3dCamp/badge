from fri3d.kits import robot
import utime

eyes = robot.eyes()


x = 0
y = 0

while True:
    x %= 7
    y %= 5

    eyes.draw_pupil(x, y, robot.RIGHT_EYE, robot.LEFT_EYE)

    x += 1
    y += 1

    utime.sleep(3)

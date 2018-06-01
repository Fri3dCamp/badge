from fri3d.kits import robot
import utime

l = robot.legs()


def say_hello_left():
    l.lean_to_left()

    for i in range(0, 3):
        l.servos.step_angle(60, 120, 25, 5, l.right_ankle)
        utime.sleep_ms(50)
        l.servos.step_angle(120, 60, 25, 5, l.right_ankle)
        utime.sleep_ms(50)

    l.undo_lean_to_left()


from fri3d.badge import Matrices
from fri3d.jewels.servo_jewel import ServoJewel

import utime


class Eyes:
    ALL = [0, 1]

    def __init__(self):
        self.matrices = Matrices()
        self.eyes = [(0, 0), (0, 0)]

    def draw_pupil(self, x, y, *eye_ids):
        if len(eye_ids) == 0:
            eye_ids = Eyes.ALL

        if x > 5:
            print("Illegal x value")
            return

        if y > 3:
            print("Illegal y value")
            return

        for i in eye_ids:
            self.eyes[i] = (x, y)
            self.matrices.clear(i)
            self.matrices.set(i, x, y)
            self.matrices.set(i, x + 1, y)
            self.matrices.set(i, x, y + 1)
            self.matrices.set(i, x + 1, y + 1)


class Legs:
    def __init__(self, left_hip=0, left_ankle=1, right_hip=2, right_ankle=3):
        self.left_hip = left_hip
        self.left_ankle = left_ankle
        self.right_hip = right_hip
        self.right_ankle = right_ankle

        self.servos = ServoJewel()
        self.servos.center()

# -- Utilities --------------------------------------------------------------------------------------------------------

    def reset(self):
        self.servos.center()

    def stepper(self, from_angle, to_angle, interval, step=1, *servos):
        if from_angle < to_angle:
            r = list(range(from_angle, to_angle + step, step))
        else:
            r = list(range(from_angle, to_angle - step, -step))

        for i in r:
            for s in servos:
                s.set_angle(i)

            utime.sleep_ms(interval)

# -- Leaning ----------------------------------------------------------------------------------------------------------

    def lean_to_left(self):
        self.servos.step_angle(90, 60, 8, 5, self.right_ankle)
        self.servos.step_angle(90, 60, 10, 5, self.left_ankle)

    def lean_to_right(self):
        self.servos.step_angle(90, 120, 8, 5, self.left_ankle)
        self.servos.step_angle(90, 120, 10, 5, self.right_ankle)

    def undo_lean_to_left(self):
        self.servos.step_angle(60, 90, 8, 5, self.right_ankle)
        self.servos.step_angle(60, 90, 10, 5, self.left_ankle)

    def undo_lean_to_right(self):
        self.servos.step_angle(120, 90, 8, 5, self.left_ankle)
        self.servos.step_angle(120, 90, 10, 5, self.right_ankle)

# -- Pointing Feet ----------------------------------------------------------------------------------------------------

    def center_to_front_right(self):
        self.servos.step_angle(90, 120, 8, 5, self.right_hip, self.left_hip)

    def front_right_to_center(self):
        self.servos.step_angle(120, 90, 8, 5, self.right_hip, self.left_hip)

    def center_to_front_left(self):
        self.servos.step_angle(90, 60, 8, 5, self.right_hip, self.left_hip)

    def front_left_to_center(self):
        self.servos.step_angle(60, 90, 8, 5, self.right_hip, self.left_hip)

# -- Walking ----------------------------------------------------------------------------------------------------------

    def step_forward(self):
        self.lean_to_right()
        self.front_right_to_center()
        self.center_to_front_left()
        self.undo_lean_to_right()

        #checkproximity();

        self.lean_to_left()
        self.front_left_to_center()
        self.center_to_front_right()
        self.undo_lean_to_left()

        #checkproximity();

    def step_backward(self):
        self.lean_to_right()
        self.front_left_to_center()
        self.center_to_front_right()
        self.undo_lean_to_right()

        # checkproximity();

        self.lean_to_left()
        self.front_right_to_center()
        self.center_to_front_left()
        self.undo_lean_to_left()

        # checkproximity();

    def turn_left(self):
        self.servos.set_angle(90, self.left_hip, self.right_hip)

        self.lean_to_right()
        self.servos.step_angle(90, 120, 15, 10, self.right_hip)
        self.undo_lean_to_right()

        self.lean_to_left()
        self.servos.set_angle(90, self.right_hip)
        utime.sleep_ms(100)
        self.undo_lean_to_left()

    def turn_right(self):
        self.servos.set_angle(90, self.left_hip, self.right_hip)

        self.lean_to_left()
        self.servos.step_angle(90, 60, 15, 10, self.left_hip)
        self.undo_lean_to_left()

        self.lean_to_right()
        self.servos.set_angle(90, self.left_hip)
        utime.sleep_ms(100)
        self.undo_lean_to_right()


RIGHT_EYE = 0
LEFT_EYE = 1

_eyes = None
_legs = None


def eyes():
    global _eyes

    if not _eyes:
        _eyes = Eyes()

    return _eyes


def legs():
    global _legs

    if not _legs:
        _legs = Legs()

    return _legs

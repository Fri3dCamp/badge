from fri3d.badge import Matrices
from fri3d.jewels.servo_jewel import ServoJewel
from machine import Timer

import utime
import array


class Eyes:
    ALL = [0, 1]
    LOOKUP = [
        # -- first line
        array.array('I', [112, 80, 112, 32, 0]),
        array.array('I', [56, 40, 56, 16, 0]),
        array.array('I', [28, 20, 28, 8, 0]),
        array.array('I', [14, 10, 14, 4, 0]),
        array.array('I', [7, 5, 7, 2, 0]),

        # -- second line
        array.array('I', [32, 112, 80, 112, 32]),
        array.array('I', [16, 56, 40, 56, 16]),
        array.array('I', [8, 28, 20, 28, 8]),
        array.array('I', [4, 14, 10, 14, 4]),
        array.array('I', [2, 7, 5, 7, 2]),

        # -- third line
        array.array('I', [0, 32, 112, 80, 112]),
        array.array('I', [0, 16, 56, 40, 56]),
        array.array('I', [0, 8, 28, 20, 28]),
        array.array('I', [0, 4, 14, 10, 14]),
        array.array('I', [0, 2, 7, 5, 7]),

        # -- closed
        array.array('I', [0, 0, 62, 0, 0]),
    ]

    BLINK_MASK = [31, 14, 4, 0, 4, 14, 31]

    def __init__(self):
        self.matrices = Matrices(refresh_interval=2)
        self.lookup_pupil(7, 0, 1)
        # self.tm = Timer(1)
        # self.tm.init(period=6000, callback=lambda timer: {
        #     self.blink(0, 1)
        # })

    def draw_pupil(self, eye, *eye_ids):
        for i in eye_ids:
            self.matrices.buffer[i] = eye

    def lookup_pupil(self, index, *eye_ids):
        if len(eye_ids) == 0:
            eye_ids = Eyes.ALL

        if index > len(Eyes.LOOKUP):
            print("Illegal index")
            return

        for i in eye_ids:
            self.matrices.buffer[i] = Eyes.LOOKUP[index]

    def blink(self, *eye_ids):
        for m in Eyes.BLINK_MASK:
            for i in eye_ids:
                self.matrices.mask[i] = m

            utime.sleep_ms(50)


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

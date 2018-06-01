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
        if len(eye_ids) == 0:
            eye_ids = [0, 1]

        for m in Eyes.BLINK_MASK:
            for i in eye_ids:
                self.matrices.mask[i] = m

            utime.sleep_ms(50)


class Legs:
    def __init__(self, left_hip=1, left_ankle=0, right_hip=2, right_ankle=3):
        self.left_hip = left_hip
        self.left_ankle = left_ankle
        self.right_hip = right_hip
        self.right_ankle = right_ankle

        self.servos = ServoJewel()
        self.servos.center()

# -- Utilities --------------------------------------------------------------------------------------------------------

    def reset(self):
        self.servos.center()

# -- Leaning ----------------------------------------------------------------------------------------------------------

    def lean_to_left(self, speed=ServoJewel.SPEED_MEDIUM):
        self.servos.step_angle(60, speed, self.right_ankle)
        self.servos.step_angle(60, speed, self.left_ankle)

    def lean_to_right(self, speed=ServoJewel.SPEED_MEDIUM):
        self.servos.step_angle(120, speed, self.left_ankle)
        self.servos.step_angle(120, speed, self.right_ankle)

    def undo_lean_to_left(self, speed=ServoJewel.SPEED_SLOW):
        self.servos.step_angle(90, speed, self.right_ankle)
        self.servos.step_angle(90, int(speed * 2), self.left_ankle)

    def undo_lean_to_right(self, speed=ServoJewel.SPEED_SLOW):
        self.servos.step_angle(90, speed, self.left_ankle)
        self.servos.step_angle(90, int(speed * 2), self.right_ankle)

# -- Twisting ---------------------------------------------------------------------------------------------------------

    def twist_left(self, speed=ServoJewel.SPEED_FAST):
        self._twist(120, speed)

    def twist_center(self, speed=ServoJewel.SPEED_FAST):
        self._twist(90, speed)

    def twist_right(self, speed=ServoJewel.SPEED_FAST):
        self._twist(60, speed)

    def _twist(self, angle, speed=ServoJewel.SPEED_FAST):
        self.servos.step_angle(angle, speed, self.right_hip, self.left_hip)

# -- Pointing Feet ----------------------------------------------------------------------------------------------------

    def center_to_front_right(self):
        self.servos.step_angle(120, ServoJewel.SPEED_FAST, self.right_hip, self.left_hip)

    def front_right_to_center(self):
        self.servos.step_angle(90, ServoJewel.SPEED_FAST, self.right_hip, self.left_hip)

    def center_to_front_left(self):
        self.servos.step_angle(60, ServoJewel.SPEED_FAST, self.right_hip, self.left_hip)

    def front_left_to_center(self):
        self.servos.step_angle(90, ServoJewel.SPEED_FAST, self.right_hip, self.left_hip)

# -- Cuties -----------------------------------------------------------------------------------------------------------

    def say_hello_left(self):
        self.lean_to_left(ServoJewel.SPEED_SLOW)

        for i in range(0, 3):
            self.servos.step_angle(120, ServoJewel.SPEED_SLOW, self.right_ankle)
            utime.sleep_ms(50)
            self.servos.step_angle(60, ServoJewel.SPEED_SLOW, self.right_ankle)
            utime.sleep_ms(50)

        self.undo_lean_to_left(ServoJewel.SPEED_SLOW)

    def say_hello_right(self):
        self.lean_to_right(ServoJewel.SPEED_SLOW)

        for i in range(0, 3):
            self.servos.step_angle(120, ServoJewel.SPEED_SLOW, self.left_ankle)
            utime.sleep_ms(50)
            self.servos.step_angle(60, ServoJewel.SPEED_SLOW, self.left_ankle)
            utime.sleep_ms(50)

        self.undo_lean_to_right(ServoJewel.SPEED_SLOW)

    def shake_left(self):
        self.lean_to_left(ServoJewel.SPEED_SLOW)

        for i in range(0, 3):
            self.servos.step_angle(120, ServoJewel.SPEED_FAST, self.right_hip)
            utime.sleep_ms(50)
            self.servos.step_angle(60, ServoJewel.SPEED_FAST, self.right_hip)
            utime.sleep_ms(50)

        self.servos.step_angle(90, ServoJewel.SPEED_FAST, self.right_hip)
        self.undo_lean_to_left(ServoJewel.SPEED_SLOW)

    def shake_right(self):
        self.lean_to_right(ServoJewel.SPEED_SLOW)

        for i in range(0, 3):
            self.servos.step_angle(120, ServoJewel.SPEED_FAST, self.left_hip)
            utime.sleep_ms(50)
            self.servos.step_angle(60, ServoJewel.SPEED_FAST, self.left_hip)
            utime.sleep_ms(50)

        self.servos.step_angle(90, ServoJewel.SPEED_FAST, self.left_hip)
        self.undo_lean_to_right(ServoJewel.SPEED_SLOW)


# -- Jumping ----------------------------------------------------------------------------------------------------------

    def jump(self, delay_between_setting=200):
        self.servos.set_angle(30, self.right_ankle)
        self.servos.set_angle(150, self.left_ankle)
        utime.sleep_ms(delay_between_setting)
        self.servos.set_angle(90, self.right_ankle, self.left_ankle)

# -- Walking ----------------------------------------------------------------------------------------------------------

    def walk_forward(self, speed=ServoJewel.SPEED_MEDIUM):
        self.lean_to_right(speed)
        self.twist_right(speed)
        self.undo_lean_to_right(speed)

        #checkproximity();

        self.lean_to_left(speed)
        self.twist_left(speed)
        self.undo_lean_to_left(speed)

        #checkproximity();

    def walk_backward(self, speed=ServoJewel.SPEED_MEDIUM):
        self.lean_to_right(speed)
        self.twist_left(speed)
        self.undo_lean_to_right(speed)

        # checkproximity();

        self.lean_to_left(speed)
        self.twist_right(speed)
        self.undo_lean_to_left(speed)

        # checkproximity();

# -- Stepping ----------------------------------------------------------------------------------------------------------

    def step_backward(self, speed=ServoJewel.SPEED_MEDIUM):
        self.lean_to_right(speed)
        self.twist_left(speed)
        self.undo_lean_to_right(speed)

        #checkproximity();

        self.lean_to_left(speed)
        self.twist_center(speed)
        self.undo_lean_to_left(speed)

        #checkproximity();

    def step_forward(self, speed=ServoJewel.SPEED_MEDIUM):
        self.lean_to_right(speed)
        self.twist_right(speed)
        self.undo_lean_to_right(speed)

        # checkproximity();

        self.lean_to_left(speed)
        self.twist_center(speed)
        self.undo_lean_to_left(speed)

        # checkproximity();

# -- Turning ----------------------------------------------------------------------------------------------------------

    def turn_right(self, speed=ServoJewel.SPEED_MEDIUM):
        self.lean_to_right(speed)
        self.servos.step_angle(60, speed, self.right_hip)
        self.undo_lean_to_right(speed)

        self.lean_to_left(speed)
        self.servos.step_angle(90, speed, self.right_hip)
        self.undo_lean_to_left(speed)

    def turn_left(self, speed=ServoJewel.SPEED_MEDIUM):
        self.lean_to_left(speed)
        self.servos.step_angle(120, speed, self.left_hip)
        self.undo_lean_to_left(speed)

        self.lean_to_right(speed)
        self.servos.step_angle(90, speed, self.left_hip)
        self.undo_lean_to_right(speed)


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

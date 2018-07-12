from fri3d.jewels.servo_jewel import ServoJewel

import utime

MIN = 60
CENTER = 90
MAX = 120


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
        self.servos.angle(MIN, speed, self.right_ankle)
        self.servos.angle(MIN, speed, self.left_ankle)

    def lean_to_right(self, speed=ServoJewel.SPEED_MEDIUM):
        self.servos.angle(MAX, speed, self.left_ankle)
        self.servos.angle(MAX, speed, self.right_ankle)

    def undo_lean_to_left(self, speed=ServoJewel.SPEED_SLOW):
        self.servos.angle(CENTER, speed, self.right_ankle)
        self.servos.angle(CENTER, int(speed * 2), self.left_ankle)

    def undo_lean_to_right(self, speed=ServoJewel.SPEED_SLOW):
        self.servos.angle(CENTER, speed, self.left_ankle)
        self.servos.angle(CENTER, int(speed * 2), self.right_ankle)

# -- Twisting ---------------------------------------------------------------------------------------------------------

    def twist_left(self, speed=ServoJewel.SPEED_FAST):
        self._twist(MAX, speed)

    def twist_center(self, speed=ServoJewel.SPEED_FAST):
        self._twist(CENTER, speed)

    def twist_right(self, speed=ServoJewel.SPEED_FAST):
        self._twist(MIN, speed)

    def _twist(self, angle, speed=ServoJewel.SPEED_FAST):
        self.servos.angle(angle, speed, self.right_hip, self.left_hip)

# -- Pointing Feet ----------------------------------------------------------------------------------------------------

    def center_to_front_right(self):
        self.servos.angle(MAX, ServoJewel.SPEED_FAST, self.right_hip, self.left_hip)

    def front_right_to_center(self):
        self.servos.angle(CENTER, ServoJewel.SPEED_FAST, self.right_hip, self.left_hip)

    def center_to_front_left(self):
        self.servos.angle(MIN, ServoJewel.SPEED_FAST, self.right_hip, self.left_hip)

    def front_left_to_center(self):
        self.servos.angle(CENTER, ServoJewel.SPEED_FAST, self.right_hip, self.left_hip)

# -- Cuties -----------------------------------------------------------------------------------------------------------

    def say_hello_left(self):
        self.lean_to_left(ServoJewel.SPEED_SLOW)

        for i in range(0, 3):
            self.servos.angle(MAX, ServoJewel.SPEED_SLOW, self.right_ankle)
            utime.sleep_ms(50)
            self.servos.angle(MIN, ServoJewel.SPEED_SLOW, self.right_ankle)
            utime.sleep_ms(50)

        self.undo_lean_to_left(ServoJewel.SPEED_SLOW)

    def say_hello_right(self):
        self.lean_to_right(ServoJewel.SPEED_SLOW)

        for i in range(0, 3):
            self.servos.angle(MAX, ServoJewel.SPEED_SLOW, self.left_ankle)
            utime.sleep_ms(50)
            self.servos.angle(MIN, ServoJewel.SPEED_SLOW, self.left_ankle)
            utime.sleep_ms(50)

        self.undo_lean_to_right(ServoJewel.SPEED_SLOW)

    def shake_left(self):
        self.lean_to_left(ServoJewel.SPEED_SLOW)

        for i in range(0, 3):
            self.servos.angle(MAX, ServoJewel.SPEED_FAST, self.right_hip)
            utime.sleep_ms(50)
            self.servos.angle(MIN, ServoJewel.SPEED_FAST, self.right_hip)
            utime.sleep_ms(50)

        self.servos.angle(CENTER, ServoJewel.SPEED_FAST, self.right_hip)
        self.undo_lean_to_left(ServoJewel.SPEED_SLOW)

    def shake_right(self):
        self.lean_to_right(ServoJewel.SPEED_SLOW)

        for i in range(0, 3):
            self.servos.angle(MAX, ServoJewel.SPEED_FAST, self.left_hip)
            utime.sleep_ms(50)
            self.servos.angle(MIN, ServoJewel.SPEED_FAST, self.left_hip)
            utime.sleep_ms(50)

        self.servos.angle(CENTER, ServoJewel.SPEED_FAST, self.left_hip)
        self.undo_lean_to_right(ServoJewel.SPEED_SLOW)


# -- Jumping ----------------------------------------------------------------------------------------------------------

    def jump(self, delay_between_setting=200):
        self.servos.angle(30, self.right_ankle)
        self.servos.angle(150, self.left_ankle)
        utime.sleep_ms(delay_between_setting)
        self.servos.angle(90, self.right_ankle, self.left_ankle)

# -- Walking ----------------------------------------------------------------------------------------------------------

    def walk_forward(self, speed=ServoJewel.SPEED_MEDIUM):
        self.lean_to_right(speed)
        self.twist_right(speed)
        self.undo_lean_to_right(speed)

        self.lean_to_left(speed)
        self.twist_left(speed)
        self.undo_lean_to_left(speed)

    def walk_backward(self, speed=ServoJewel.SPEED_MEDIUM):
        self.lean_to_right(speed)
        self.twist_left(speed)
        self.undo_lean_to_right(speed)

        self.lean_to_left(speed)
        self.twist_right(speed)
        self.undo_lean_to_left(speed)

# -- Stepping ----------------------------------------------------------------------------------------------------------

    def step_backward(self, speed=ServoJewel.SPEED_MEDIUM):
        self.lean_to_right(speed)
        self.twist_left(speed)
        self.undo_lean_to_right(speed)

        self.lean_to_left(speed)
        self.twist_center(speed)
        self.undo_lean_to_left(speed)

    def step_forward(self, speed=ServoJewel.SPEED_MEDIUM):
        self.lean_to_right(speed)
        self.twist_right(speed)
        self.undo_lean_to_right(speed)

        self.lean_to_left(speed)
        self.twist_center(speed)
        self.undo_lean_to_left(speed)

# -- Turning ----------------------------------------------------------------------------------------------------------

    def turn_right(self, speed=ServoJewel.SPEED_MEDIUM):
        self.lean_to_right(speed)
        self.servos.angle(MIN, speed, self.right_hip)
        self.undo_lean_to_right(speed)

        self.lean_to_left(speed)
        self.servos.angle(CENTER, speed, self.right_hip)
        self.undo_lean_to_left(speed)

    def turn_left(self, speed=ServoJewel.SPEED_MEDIUM):
        self.lean_to_left(speed)
        self.servos.angle(MAX, speed, self.left_hip)
        self.undo_lean_to_left(speed)

        self.lean_to_right(speed)
        self.servos.angle(CENTER, speed, self.left_hip)
        self.undo_lean_to_right(speed)


RIGHT_EYE = 0
LEFT_EYE = 1

_eyes = None
_legs = None


def legs():
    global _legs

    if not _legs:
        _legs = Legs()

    return _legs

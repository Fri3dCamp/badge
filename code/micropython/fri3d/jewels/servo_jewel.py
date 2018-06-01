from fri3d.ext import Servo
import utime


class ServoJewel:
    ALL = [0, 1, 2, 3]
    SPEED_FAST = 8
    SPEED_MEDIUM = 15
    SPEED_SLOW = 25
    SPEED_LAZY = 50

    def __init__(self):
        self.servos = [Servo(32), Servo(25), Servo(26), Servo(27)]

    def center(self, *servo_ids):
        if len(servo_ids) == 0:
            servo_ids = ServoJewel.ALL

        for s in servo_ids:
            self.servos[s].center()

    def min(self, *servo_ids):
        if len(servo_ids) == 0:
            servo_ids = ServoJewel.ALL

        for s in servo_ids:
            self.servos[s].min()

    def max(self, *servo_ids):
        if len(servo_ids) == 0:
            servo_ids = ServoJewel.ALL

        for s in servo_ids:
            self.servos[s].max()

    def set(self, pos, *servo_ids):
        if len(servo_ids) == 0:
            servo_ids = ServoJewel.ALL

        for i in servo_ids:
            self.servos[i].set(pos)

    def set_angle(self, angle, *servo_ids):
        if len(servo_ids) == 0:
            servo_ids = ServoJewel.ALL

        for i in servo_ids:
            self.servos[i].set_angle(angle)

    def set_percentage(self, pct, *servo_ids):
        if len(servo_ids) == 0:
            servo_ids = ServoJewel.ALL

        for i in servo_ids:
            self.servos[i].set_percentage(pct)

    def step_angle(self, to_angle, speed, *servo_ids):
        if len(servo_ids) == 0:
            servo_ids = ServoJewel.ALL

        longest_range = 0
        ranges = {}
        for s in servo_ids:
            from_angle = self.servos[s].angle()
            if from_angle < to_angle:
                ranges[s] = list(range(from_angle, to_angle + 5, 5))
            else:
                ranges[s] = list(range(from_angle, to_angle - 5, -5))

            if longest_range < len(ranges[s]):
                longest_range = len(ranges[s])

        for i in range(0, longest_range):
            for s in servo_ids:
                if i >= len(ranges[s]):
                    continue

                self.servos[s].set_angle(ranges[s][i])

            utime.sleep_ms(speed)

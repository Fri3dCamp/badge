from fri3d.ext import Servo
import utime


class ServoJewel:
    ALL = [0, 1, 2, 3]

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

    def step_angle(self, from_angle, to_angle, interval, step, *servo_ids):
        if len(servo_ids) == 0:
            servo_ids = ServoJewel.ALL

        if from_angle < to_angle:
            r = list(range(from_angle, to_angle + step, step))
        else:
            r = list(range(from_angle, to_angle - step, -step))

        for i in r:
            for s in servo_ids:
                self.servos[s].set_angle(i)

            utime.sleep_ms(interval)

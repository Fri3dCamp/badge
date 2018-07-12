from fri3d.ext import Servo
import utime
import machine


class ServoJewel:
    ALL = [0, 1, 2, 3]
    SPEED_FAST = 8
    SPEED_MEDIUM = 15
    SPEED_SLOW = 25
    SPEED_LAZY = 50

    def __init__(self):
        self.servos = [Servo(32, timer=0), Servo(25, timer=1), Servo(26, timer=2), Servo(27, timer=3)]
        for i in range(4):
            settings = machine.nvs_getstr('servo_' + str(i))

            if settings is None:
                continue

            print("initializing servo " + str(i) + " with settings " + settings)

            s = settings.split()
            self.servos[i].tune(float(s[0]), float(s[1]))

    def tune(self, servo_id, min_pct, max_pct):
        self.servos[servo_id].tune(min_pct, max_pct)
        machine.nvs_setstr('servo_' + str(servo_id), str(min_pct) + " " + str(max_pct))
        self.servos[servo_id].angle(90)

    def center(self, *servo_ids):
        if len(servo_ids) == 0:
            servo_ids = ServoJewel.ALL

        for s in servo_ids:
            self.servos[s].angle(90)

    def angle(self, to_angle, speed=None, *servo_ids):
        if len(servo_ids) == 0:
            servo_ids = ServoJewel.ALL

        if speed is None:
            for s in servo_ids:
                self.servos[s].angle(to_angle)

        else:
            longest_range = 0
            ranges = {}
            for s in servo_ids:
                from_angle = self.servos[s].angle()
                if from_angle < to_angle:
                    ranges[s] = list(range(int(from_angle), to_angle + 5, 5))
                else:
                    ranges[s] = list(range(int(from_angle), to_angle - 5, -5))

                if longest_range < len(ranges[s]):
                    longest_range = len(ranges[s])

            for i in range(0, longest_range):
                for s in servo_ids:
                    if i >= len(ranges[s]):
                        continue

                    self.servos[s].angle(ranges[s][i])

                utime.sleep_ms(speed)

from machine import PWM


SERVO_FREQUENCY = 50
SERVO_MIN_PCT = 4.5
SERVO_MAX_PCT = 13.2


class Servo:
    def __init__(self, pin, freq=SERVO_FREQUENCY, timer=2):
        """
        Create a new Servo instance

        @param pin: 	    the machine.Pin on which the servo is connected
        @param freq:        the frequency at which the PWM signal should be generated
        """
        self.min_pct = SERVO_MIN_PCT
        self.max_pct = SERVO_MAX_PCT
        self.freq = freq

        self.pct_per_degree = (self.max_pct - self.min_pct) / float(180)

        self.pwm = PWM(pin, freq=freq, timer=timer)
        self.angle(90)

    def tune(self, min_pct, max_pct):
        self.min_pct = min_pct
        self.max_pct = max_pct

        self.pct_per_degree = (self.max_pct - self.min_pct) / float(180)

    def angle(self, angle=None):
        if angle is None:
            return (self.pwm.duty() - self.min_pct) / self.pct_per_degree
        else:
            if 0 <= angle <= 180:
                self.pwm.duty(angle * self.pct_per_degree + self.min_pct)

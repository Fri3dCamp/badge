from machine import PWM


class Servo:
    def __init__(self, pin, lower_duty=512, upper_duty=1953.5, freq=50):
        """
        Create a new Servo instance

        The lower and upper duty values may be tweaked depending on the servo model being used.

        @param pin: 	    the machine.Pin on which the servo is connected
        @param lower_duty: 	the lower duty value
        @param upper_duty:	the upper duty value
        @param freq:        the frequency at which the PWM signal should be generated
        """
        self.pwm = PWM(pin, freq=freq)
        self.lower_duty = (lower_duty * freq) / 10000
        self.upper_duty = (upper_duty * freq) / 10000

    def set(self, pos):
        """
        Set the position as a value between -1 and 1

        the position ranges from -1 to 1 where -1 equals 0 degrees and 1 equals 180 degrees

        @param pos: 	an float between -1 and 1, both inclusive
        """
        self.set_percentage((pos + 1) * 50)

    def set_angle(self, angle):
        """
        Set the position as an angle between 0 and 180 degrees

        @param angle: 	an integer between 0 and 180
        """
        self.set_percentage(angle / 180)

    def angle(self):
        """
        Get the servo's angle

        :return:    the angle expressed as degrees
        """
        return int(self.pos() * 180)

    def pos(self):
        """
        Get the servo's position

        :return:    the position of the servo as a float between 0 and 1
        """
        return int((self.pwm.duty() - self.lower_duty) / (self.upper_duty - self.lower_duty) * 100) / 100

    def center(self):
        """
        Set the servo to it's center position.
        """
        self.set_percentage(0.5)

    def min(self):
        """
        Set the servo to it's minimum position.
        """
        self.set_percentage(0)

    def max(self):
        """
        Set the servo to it's maximum position.
        """
        self.set_percentage(1)

    def set_percentage(self, pct):
        """
        Set the position as a percentage

        freq=50: cycle=1s/50=20ms=0.02: lower=0.001 upper=0.0025

        @param pct: 	a float between 0 and 1
        """
        self.pwm.duty(self.lower_duty + (pct * (self.upper_duty - self.lower_duty)))
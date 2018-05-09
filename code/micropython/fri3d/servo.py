import machine

SERVO_1_PIN = machine.Pin(15, machine.Pin.OUT)
SERVO_2_PIN = machine.Pin(2, machine.Pin.OUT)
SERVO_3_PIN = machine.Pin(19, machine.Pin.OUT)
SERVO_4_PIN = machine.Pin(18, machine.Pin.OUT)


class Servo:
    def __init__(self, pin, lower_duty=37, upper_duty=129):
        """
        Create a new Servo instance

        The lower and upper duty values may be tweaked depending on the servo model being used.

        @param pin 	the machine.Pin on which the servo is connected
        @param lower_duty 	the lower duty value
        @param upper_duty	the upper duty value
        """
        self.pwm = machine.PWM(pin)
        self.pwm.freq(50)
        self.lower_duty = lower_duty
        self.upper_duty = upper_duty
        self.range = self.upper_duty - self.lower_duty

    def set(self, pos):
        """
        Set the position as a value between -1 and 1

        the position ranges from -1 to 1 where -1 equals 0 degrees and 1 equals 180 degrees

        @param pos 	an float between -1 and 1, both inclusive
        """
        self.set_percentage((pos + 1) * 50)

    def set_angle(self, angle):
        """
        Set the position as an angle between 0 and 180 degrees

        @param angle 	an integer between 0 and 180
        """

        self.set_percentage(angle / 180)

    def set_percentage(self, pct):
        """
        Set the position as a percentage

        @param pct 	a float between 0 and 1
        """
        self.pwm.duty(self.lower_duty + int(pct * self.range))

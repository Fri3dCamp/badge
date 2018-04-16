import machine

SERVO_1_PIN = 15
SERVO_2_PIN = 2
SERVO_3_PIN = 19
SERVO_4_PIN = 18

class Servo:
    def __init__(self, pin):
    	self.pwm = machine.PWM(machine.Pin(pin), freq=50)
        pass

    def turn(self, angle, interval):
        pass

    def turn_to(self, angle, interval):
        pass

    def angle(self):
        pass
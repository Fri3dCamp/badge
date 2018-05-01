import machine

class Pins:
	PIN_SERVO_1 = machine.Pin(15, machine.Pin.OUT)
	PIN_SERVO_2 = machine.Pin(2, machine.Pin.OUT)
	PIN_SERVO_3 = machine.Pin(19, machine.Pin.OUT)
	PIN_SERVO_4 = machine.Pin(18, machine.Pin.OUT)

	PIN_BUTTON_A = machine.Pin(12, machine.Pin.IN)
	PIN_BUTTON_B = machine.Pin(4, machine.Pin.IN)

	PIN_MATRIX_LATCH 	= machine.Pin(21, machine.Pin.OUT, value=1)
	PIN_MATRIX_CLOCK 	= machine.Pin(4, machine.Pin.OUT, value=0),
	PIN_MATRIX_DATA 	= machine.Pin(2, machine.Pin.OUT, value=0),
	PIN_MATRIX_ENABLE 	= machine.Pin(22, machine.Pin.OUT, value=0)
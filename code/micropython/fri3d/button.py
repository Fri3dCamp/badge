import machine

BUTTON_A_PIN = machine.Pin(12, machine.Pin.IN)
BUTTON_B_PIN = machine.Pin(4, machine.Pin.IN)
BUTTON_D_PIN = machine.Pin(0, machine.Pin.IN)


class Button:
	def __init__(self, pin):
		self.pin = pin

	def on_press(self, button_pin, callback):
		"""
		Invoke the callback when the button is pressed.
		"""
		self.pin.irq(trigger=machine.Pin.IRQ_FALLING, handler=callback)

	def on_release(self, button_pin, callback):
		"""
		Invoke the callback when the button is released.
		"""
		self.pin.irq(trigger=machine.Pin.IRQ_RISING, handler=callback)
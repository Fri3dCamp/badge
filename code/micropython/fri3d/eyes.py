
from fri3d.display import Matrices
from fri3d.badge import Pins


class Eyes:
	def __init__(self, latch=21, clock=4, data=2, enable=22):
		self.matrices = Matrices(latch, clock, data, enable)
		self.left_eye_pos = (0, 0)
		self.right_eye_pos = (0, 0)

	def draw_pupil(self, eye, x, y):
		if (x > 5):
			print("Illegal x value")
			return

		if (y > 3):
			print("Illegal y value")
			return

		if (eye == 0):
			left_eye_pos[0] = x
			left_eye_pos[1] = y
		else:
			right_eye_pos[0] = x
			right_eye_pos[1] = y

		self.matrices.clear(eye)
		self.matrices.set(eye, x, y)
		self.matrices.set(eye, x+1, y)
		self.matrices.set(eye, x, y+1)
		self.matrices.set(eye, x+1, y+1)
		
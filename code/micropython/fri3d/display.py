import machine
import _thread
import array


class Matrices:
    def __init__(self, latch=21, clock=4, data=2, enable=22, register_count=3):
        self.latch = machine.Pin(latch, machine.Pin.OUT, value=1)
        self.clock = machine.Pin(clock, machine.Pin.OUT, value=0)
        self.data = machine.Pin(data, machine.Pin.OUT, value=0)
        self.enable = machine.Pin(enable, machine.Pin.OUT, value=0)

        self.register_count = register_count

        self.enable.value(0)
        self.left_matrix = array.array('I', [ 0 for _ in range(0, 5)]) 
        self.right_matrix = array.array('I', [ 0 for _ in range(0, 5)])

        _thread.start_new_thread(
            "video", video_thread_fn, (self.data, self.clock, self.latch, self.left_matrix, self.right_matrix)
        )

    def set(self, matrix, x, y):
        if matrix == 0:
            self.left_matrix[y] |= (1 << x)
        else:
            self.right_matrix[y] |= (1 << x)

    def clear(self, matrix):
        for i in range(0, 5):
            if matrix == 0:
                self.left_matrix[i] = 0
            else:
                self.right_matrix[i] = 0


def video_thread_fn(data, clock, latch, left_matrix, right_matrix):
    print("video_thread: started")
    _thread.allowsuspend(True)

    def shiftbit(bit):
        data.value(bit)
        clock.value(1)
        clock.value(0)

    while True:
        for y in range(0, 5):
            
            for x in range(0, 7):
                shiftbit(~(right_matrix[y] >> x) & 1)
            
            for j in range(0, 5):
                shiftbit(j == y)
            
            for x in range(0, 7):
                shiftbit(~(left_matrix[y] >> x) & 1)
            
            for j in range(0, 5):
                shiftbit(j == y)

            latch.value(0)
            latch.value(1)



import machine
import math
import _thread
import time
import array


class Eyes:
    def __init__(self, latch=21, clock=4, data=2, enable=22, register_count=3):
        self.latch = machine.Pin(latch, machine.Pin.OUT, value=1)
        self.clock = machine.Pin(clock, machine.Pin.OUT, value=0)
        self.data = machine.Pin(data, machine.Pin.OUT, value=0)
        self.enable = machine.Pin(enable, machine.Pin.OUT, value=0)

        self.register_count = register_count

        self.enable.value(0)
        self.left_matrix = array.array('I', [ 0 for _ in range(0, 5)]) 
        self.right_matrix = array.array('I', [ 0 for _ in range(0, 5)])

        def video_refresher():
            while True:
                self.render()
                # time.sleep_us(200)

        _thread.start_new_thread(video_refresher, ())


    def render(self):
        # -- left eye first
        # for y in range(0, 5):
        # # i = 4
        #     for x in range(0, 7):
        #         self.shiftbit(~(self.right_matrix[y] >> x) & 1)
        #     # print(" ")
        #     for j in range(0, 5):
        #         if (i == y):
        #             self.shiftbit(1)
        #         else:
        #             self.shiftbit(0)

        #     # print("---")
        #     for x in range(0, 7):
        #         self.shiftbit(~(self.left_matrix[y] >> x) & 1)
        #     # print(" ")
        #     for j in range(0, 5):
        #         if (i == y):
        #             self.shiftbit(1)
        #         else:
        #             self.shiftbit(0)
        for y in range(0, 5):
            
            for x in range(0, 7):
                self.shiftbit(~(self.right_matrix[y] >> x) & 1)
            # print(" ")
            for j in range(0, 5):
                self.shiftbit(j == y)
            # print("---")
            for x in range(0, 7):
                self.shiftbit(~(self.left_matrix[y] >> x) & 1)
            # print(" ")
            for j in range(0, 5):
                self.shiftbit(j == y)

            self.latch.value(0)
            self.latch.value(1)
  
    def shiftbit(self, bit):
        # print(bit)
        self.data.value(bit)
        self.clock.value(1)
        self.clock.value(0)

    def shiftout(self, bits):
        for i in range(0, self.register_count * 8):
            # print("shifting " + str(bits & ( 1 << i ) & 1))
            self.shiftbit((bits >> i) & 1)

        self.latch.value(0)
        self.latch.value(1)

    def set(self, eye, x, y):
        if (eye == 0):
            self.left_matrix[y] |= (1 << x)
        else:
            self.right_matrix[y] |= (1 << x)

    def clear(self):
        for i in range(0, 5):
            self.left_matrix[i] = 0
            self.right_matrix[i] = 0

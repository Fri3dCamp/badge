# import machine
# import math
# import _thread
# import time
import array


class Eyes:
    def __init__(self, latch=21, clock=4, data=2, enable=22, register_count=3):
        # self.latch = machine.Pin(latch, machine.Pin.OUT)
        # self.clock = machine.Pin(clock, machine.Pin.OUT)
        # self.data = machine.Pin(data, machine.Pin.OUT)
        # self.enable = machine.Pin(enable, machine.Pin.OUT)

        # self.register_count = register_count

        # self.enable.value(0)
        self.matrix = array.array('I', [ 0 for _ in range(0, 5)]) 
        self.out = 0
        # def video_refresher():
        #     while True:
        #         self.render()
        #         time.sleep_us(200)

        # _thread.start_new_thread(video_refresher, ())


    def render(self):
        # self.latch.value(0)

        # -- left eye first
        for i in range(0, 5):
            self.out = 0
            # print(" row " + str(i))
            x_mask = (1 << i)
            # print("mask: " + bin(y_mask))             

            for eye in range(0, 2):
                for j in range(0, 7):
                    self.shiftbit(~(self.matrix[i] >> (j  + (eye * 7))) & 1)       
                # print("eye " + str(eye))
                for k in range(0, 5):
                    self.shiftbit(1)
                # print("--")
                

            print(bin(self.out | (2**25)))

        # self.latch.value(1)
  
    def shiftbit(self, bit):
        self.out = self.out << 1 | bit
        # print(bit)
        # self.clock.value(0)
        # self.data.value(bit)
        # self.clock.value(1)
        # self.clock.value(0)

    def shiftout(self, bits):
        for i in range(0, self.register_count * 8):
            shiftbit(bits & ( 1 << i ) & 1)

    def set(self, eye, x, y):
        self.matrix[y] |= (1 << (x + (eye * 7)))

    def clear(self):
        for i in range(0, 5):
            self.matrix[i] = 0


eyes = Eyes()
eyes.set(0,0,1)
eyes.render()
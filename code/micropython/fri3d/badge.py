from machine import I2C, Pin, PWM
import _thread
import array
import network
import utime


i2c_bus = I2C(id=0, scl=Pin(22), sda=Pin(21), freq=100000)


class AcceleroMeter:
    """
    Control the built-in accelerometer
    """
    address = None

    BW_RATE_1600HZ = [0x0F]
    BW_RATE_800HZ = [0x0E]
    BW_RATE_400HZ = [0x0D]
    BW_RATE_200HZ = [0x0C]
    BW_RATE_100HZ = [0x0B]
    BW_RATE_50HZ = [0x0A]
    BW_RATE_25HZ = [0x09]

    RANGE_2G = 0x00
    RANGE_4G = 0x01
    RANGE_8G = 0x02
    RANGE_16G = 0x03

    MEASURE = [0x08]
    AXES_DATA = 0x32

    DATA_FORMAT = 0x31
    BW_RATE = 0x2C
    POWER_CTL = 0x2D

    def __init__(self, bus=i2c_bus, address=0x53):
        self.bus = bus
        self.address = address
        self.set_bandwidth_rate(AcceleroMeter.BW_RATE_100HZ)
        self.set_range(AcceleroMeter.RANGE_2G)
        self.enable_measurement()

    def enable_measurement(self):
        self.bus.writeto_mem(self.address, AcceleroMeter.POWER_CTL, bytearray(AcceleroMeter.MEASURE))

    def set_bandwidth_rate(self, rate_flag):
        """
        Set the bandwidth at which the accelerometer will update

        :param rate_flag:   one of the AcceleroMeter.BW_RATE_*** flags
        :return:
        """
        self.bus.writeto_mem(self.address, AcceleroMeter.BW_RATE, bytearray(rate_flag))

    # set the measurement range for 10-bit readings
    def set_range(self, range_flag):
        """
        Set the measurement range for 10-bit readings

        :param range_flag:   one of the AcceleroMeter.RANGE_*** flags
        """
        value = self.bus.readfrom_mem(self.address, AcceleroMeter.DATA_FORMAT, 1)

        val2 = value[0]
        val2 &= ~0x0F
        val2 |= range_flag
        val2 |= 0x08
        buf = [val2]

        self.bus.writeto_mem(self.address, AcceleroMeter.DATA_FORMAT, bytearray(buf))

    def sample(self, gforce=False):
        """
        Read the current reading from the sensor for each axis

        :param gforce: result in m/s^2 if False (default) or result in gs if True
        :return: {"x": x-value, "y": y-value, "z": z-value}
        """
        b = self.bus.readfrom_mem(self.address, AcceleroMeter.AXES_DATA, 6)

        x = b[0] | (b[1] << 8)
        if x & (1 << 16 - 1):
            x = x - (1 << 16)

        y = b[2] | (b[3] << 8)
        if y & (1 << 16 - 1):
            y = y - (1 << 16)

        z = b[4] | (b[5] << 8)
        if z & (1 << 16 - 1):
            z = z - (1 << 16)

        x = x * 0.004
        y = y * 0.004
        z = z * 0.004

        if not gforce:
            x = x * 9.80665
            y = y * 9.80665
            z = z * 9.80665

        x = round(x, 4)
        y = round(y, 4)
        z = round(z, 4)

        return {"x": x, "y": y, "z": z}


class Button:
    def __init__(self, pin):
        self.pin = pin

    def on_press(self, callback):
        """
        Invoke the callback when the button is pressed.

        :param callback:    the function to call when the button is pressed
        """
        self.pin.irq(trigger=Pin.IRQ_FALLING, handler=callback)

    def on_release(self, callback):
        """
        Invoke the callback when the button is released.

        :param callback:    the function to call when the button is released
        """
        self.pin.irq(trigger=Pin.IRQ_RISING, handler=callback)


class Buzzer:
    def __init__(self, pin=Pin(33)):
        """
        Create a new Buzzer instance

        @param pin: 	the machine.Pin on which the servo is connected
        """
        self.pwm = PWM(pin, freq=3000)

    def enable(self):
        """
        Enable the output of the buzzer
        """
        self.pwm.resume()

    def disable(self):
        """
        Disable the output of the buzzer
        """
        self.pwm.pause()

    def set(self, freq):
        """
        Set the frequency

        @param freq:     the frequency to set
        """
        self.pwm.duty(freq)


class Matrices:
    def __init__(self, latch=Pin(15), clock=Pin(4), data=Pin(2), enable=Pin(13), register_count=3):
        self.latch = latch
        self.latch.init(value=1, mode=Pin.OUT)

        self.clock = clock
        self.clock.init(value=0, mode=Pin.OUT)

        self.data = data
        self.data.init(value=0, mode=Pin.OUT)

        self.enable = enable
        self.enable.init(value=0, mode=Pin.OUT)

        self.register_count = register_count

        self.left_matrix = array.array('I', [0 for _ in range(0, 5)])
        self.right_matrix = array.array('I', [0 for _ in range(0, 5)])

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


class Wifi:
    def __init__(self, ssid, pwd):
        self.ssid = ssid
        self.pwd = pwd
        self.wlan = None

    def connected(self):
        if not self.wlan:
            return False

        return self.wlan.isconnected()

    def connect(self):
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)
        self.wlan.connect(self.ssid, self.pwd)

    def wait_until_connected(self):
        while not self.wlan.isconnected():
            print(".")

    def ip(self):
        return self.wlan.ifconfig()[0]


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

        utime.sleep_ms(5)

_accelero = None
_btn0 = None
_btn1 = None
_matrix = None
_buzzer = None


def btn_0():
    global _btn0

    if not _btn0:
        _btn0 = Button(Pin(36))

    return _btn0


def btn_1():
    global _btn1

    if not _btn1:
        _btn1 = Button(Pin(39))

    return _btn1


def buzzer():
    global _buzzer

    if not _buzzer:
        _buzzer = Buzzer()

    return _buzzer


def accelero():
    global _accelero

    if not _accelero:
        _accelero = AcceleroMeter()

    return _accelero


def matrix():
    global _matrix

    if not _matrix:
        _matrix = Matrices()

    return _matrix

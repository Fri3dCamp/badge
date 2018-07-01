import network
import utime
import machine
import _thread
import array


class Feedback:
    ERR_TIMEOUT_WIFI = "WIFI Timeout!"
    ERR_TIMEOUT_MQTT = "MQTT Timeout!"
    ERR_WRONG_X_COORDINATE = "Invalid X coordinate"
    ERR_WRONG_Y_COORDINATE = "Invalid Y coordinate"
    INF_EYES_ENABLED = "Eyes Enabled"
    INF_BUZZER_ENABLED = "Buzzer Enabled"
    INF_ACCELERO_ENABLED = "Accelerometer Enabled"


class Badge:
    def __init__(self, data_cb=None, enable_eyes=False, enable_buzzer=False, enable_accelero=False):
        self.client_id = machine.nvs_getstr('token')
        self.wifi_ssid = machine.nvs_getstr('ssid')
        self.wifi_password = machine.nvs_getstr('pwd')
        self.mqtt_server = machine.nvs_getstr('mqtt_server')
        self.mqtt_user = machine.nvs_getstr('mqtt_user')
        self.mqtt_password = machine.nvs_getstr('mqtt_password')

        self.wifi = network.WLAN(network.STA_IF)
        self.mqtt = network.mqtt(self.client_id, self.mqtt_server,
                                 user=self.mqtt_user,
                                 password=self.mqtt_password,
                                 cleansession=True,
                                 data_cb=data_cb)

        self.button_0 = Button(machine.Pin(36))
        self.button_1 = Button(machine.Pin(39))
        self.touch_0 = machine.TouchPad(machine.Pin(12))
        self.touch_1 = machine.TouchPad(machine.Pin(14))

        i2c_bus = machine.I2C(id=0, scl=machine.Pin(22), sda=machine.Pin(21), freq=100000)

        if enable_eyes:
            self.eyes = Eyes()
            print(Feedback.INF_EYES_ENABLED)

        if enable_buzzer:
            self.buzzer = Buzzer()
            print(Feedback.INF_BUZZER_ENABLED)

        if enable_accelero:
            self.accelero = AcceleroMeter(i2c_bus)
            print(Feedback.INF_ACCELERO_ENABLED)

    def connect(self, timeout=5000):
        self.wifi.active(True)
        self.wifi.connect(self.wifi_ssid, self.wifi_password)

        # -- wait until connected
        tmo = timeout/100
        while not self.wifi.isconnected():
            utime.sleep_ms(100)
            tmo -= 1
            if tmo == 0:
                print(Feedback.ERR_TIMEOUT_WIFI)
                return False

        # -- start mqtt
        if self.mqtt.status()[0] == 0:
            self.mqtt.start()

        tmo = timeout / 100
        while not self.mqtt.status()[0] == 2:
            utime.sleep_ms(100)
            tmo -= 1
            if tmo == 0:
                print(Feedback.ERR_TIMEOUT_MQTT)
                return False

        return True

    def status(self):
        return (
            self.wifi.isconnected(),
            self.mqtt.status()
        )

    def disconnect(self, timeout=5000):
        self.mqtt.stop()

        tmo = timeout / 100
        while not self.mqtt.status()[0] == 0:
            utime.sleep_ms(100)
            tmo -= 1
            if tmo == 0:
                print(Feedback.ERR_TIMEOUT_MQTT)
                return False

        if self.wifi.isconnected():
            self.wifi.disconnect()

        tmo = timeout / 100
        while self.wifi.isconnected():
            utime.sleep_ms(100)
            tmo -= 1
            if tmo == 0:
                print(Feedback.ERR_TIMEOUT_WIFI)
                return False

        self.wifi.active(False)

        return True


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

    def __init__(self, bus, address=0x53):
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
        self.pin.irq(trigger=machine.Pin.IRQ_FALLING, handler=callback)

    def on_release(self, callback):
        """
        Invoke the callback when the button is released.

        :param callback:    the function to call when the button is released
        """
        self.pin.irq(trigger=machine.Pin.IRQ_RISING, handler=callback)


class Buzzer:
    def __init__(self, pin=machine.Pin(33)):
        """
        Create a new Buzzer instance

        @param pin: 	the machine.Pin on which the servo is connected
        """
        self.pwm = machine.PWM(pin, freq=3000)

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


class Eyes:
    ALL = [0, 1]
    LOOKUP = [[
            array.array('I', [112, 80, 112, 32, 0]),
            array.array('I', [56, 40, 56, 16, 0]),
            array.array('I', [28, 20, 28, 8, 0]),
            array.array('I', [14, 10, 14, 4, 0]),
            array.array('I', [7, 5, 7, 2, 0])
        ], [
            array.array('I', [32, 112, 80, 112, 32]),
            array.array('I', [16, 56, 40, 56, 16]),
            array.array('I', [8, 28, 20, 28, 8]),
            array.array('I', [4, 14, 10, 14, 4]),
            array.array('I', [2, 7, 5, 7, 2]),
        ], [
            array.array('I', [0, 32, 112, 80, 112]),
            array.array('I', [0, 16, 56, 40, 56]),
            array.array('I', [0, 8, 28, 20, 28]),
            array.array('I', [0, 4, 14, 10, 14]),
            array.array('I', [0, 2, 7, 5, 7]),
        ], [
            # -- specials
            array.array('I', [0, 0, 62, 0, 0]),     # closed
            array.array('I', [0, 0, 28, 0, 0]),     # closed
        ]
    ]

    BLINK_MASK = [31, 14, 4, 0, 4, 14, 31]

    def __init__(self):
        self.latch = machine.Pin(15)
        self.latch.init(value=1, mode=machine.Pin.OUT)

        self.clock = machine.Pin(4)
        self.clock.init(value=0, mode=machine.Pin.OUT)

        self.data = machine.Pin(2)
        self.data.init(value=0, mode=machine.Pin.OUT)

        self.enable = machine.Pin(13)
        self.enable.init(value=0, mode=machine.Pin.OUT)

        self.register_count = 3

        self.mask = array.array('I', [31, 31])

        self.buffer = [
            array.array('I', [0 for _ in range(0, 5)]),
            array.array('I', [0 for _ in range(0, 5)])
        ]

        _thread.start_new_thread(
            "video", video_thread_fn, (self.data, self.clock, self.latch, self.buffer, self.mask, 2)
        )

    def pupil(self, x, y, *eye_ids):
        if len(eye_ids) == 0:
            eye_ids = Eyes.ALL

        if x < 0 or x > 5:
            print(Feedback.ERR_WRONG_X_COORDINATE)
            return False

        if y < 0 or y > 3:
            print(Feedback.ERR_WRONG_Y_COORDINATE)
            return False

        for i in eye_ids:
            self.buffer[i] = Eyes.LOOKUP[y][x]

    def blink(self, *eye_ids):
        if len(eye_ids) == 0:
            eye_ids = [0, 1]

        for m in Eyes.BLINK_MASK:
            for i in eye_ids:
                self.mask[i] = m

            utime.sleep_ms(50)

    def thinking(self):
        for i in Eyes.ALL:
            self.buffer[i] = Eyes.LOOKUP[4][1]

    def reset(self):
        self.pupil(1, 3)


def video_thread_fn(data, clock, latch, buffer, mask, refresh_interval):
    _thread.allowsuspend(True)

    d = [
        [1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 0, 1, 0],
        [0, 0, 0, 0, 1]
    ]

    r = [0, 1, 2, 3, 4, 5, 6]

    row = 0

    while True:
        row %= 5
        for x in r:
            # (mask[1][row] >> x)
            data.value(1 - ((buffer[1][row] >> x & 1) & (mask[1] >> row & 1)))
            clock.value(1)
            clock.value(0)

        for j in d[row]:
            data.value(j)
            clock.value(1)
            clock.value(0)

        for x in r:
            data.value(1 - ((buffer[0][row] >> x & 1) & (mask[0] >> row & 1)))
            clock.value(1)
            clock.value(0)

        for j in d[row]:
            data.value(j)
            clock.value(1)
            clock.value(0)

        latch.value(0)
        latch.value(1)

        row += 1
        _thread.wait(refresh_interval)

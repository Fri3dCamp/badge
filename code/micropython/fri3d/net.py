import network


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
            pass

    def ip(self):
        return self.wlan.ifconfig()[0]
import network

wlan = None


def connect(ssid="area3001", pwd=""):
    global wlan

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, pwd)

    while not wlan.isconnected():
        pass

    print('IPAddress: {}'.format(wlan.ifconfig()[0]))


def get_ip():
    return wlan.ifconfig()[0]

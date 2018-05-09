from fri3d.net import Wifi

# -- Connect to wifi
wifi = Wifi("area3001", "")
wifi.connect()
wifi.wait_until_connected()
print("Wifi connected as %s" % wifi.ip())
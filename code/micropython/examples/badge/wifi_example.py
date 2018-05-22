from fri3d.badge import Wifi

# -- Set the SSID and the password to get access
ssid = "area3001"
password = ""

# -- Create a new wifi instance
wifi = Wifi(ssid, password)

# -- Connect to wifi
wifi.connect()

# -- Wait for the wifi to be connected
wifi.wait_until_connected()

print("Wifi connected as %s" % wifi.ip())

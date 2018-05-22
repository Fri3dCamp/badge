# Getting Started

## Connect the badge to your laptop or pc
You can connect the badge to your laptop or pc using a micro-usb cable. In some cases you may need to install a driver as well for the badge to be recognized. That driver can be found at ```https://www.silabs.com/products/development-tools/software/usb-to-uart-bridge-vcp-drivers```

## Micropython on the badge

Get the micropython image for the ESP32 from ```https://micropython.org/download/#esp32```

In order to flash the image file to the badge, you will need a python tool called ```esptool.py```. Luckily you can install this tool using pip:

```
pip install esptool
```

Once we have installed esptool and downloaded the image, we can start the flashing process. The first time we will need to clean the flash memory of the badge by using the esptool.py script:

```
esptool.py --chip esp32 --port /dev/cu.SLAB_USBtoUART erase_flash
```

```
esptool.py --chip esp32 --port /dev/cu.SLAB_USBtoUART write_flash -z 0x1000 <path to the .bin file>
```

Once the process has finished you will have micropython available on the badge.

## Invoking python commands
A repl (python commandline) is available when connecting to the badge over usb. on mac and linux, the screen command allows you to access the repl by invoking:

```
screen /dev/cu.SLAB_USBtoUART 115200
```

## Deploying programs

To make interacting with the badge a bit easier, we are going to install a tool called ```ampy```. It was developed by adafruit to make interacting with circuitpython (a micropython adoption by adafruit) easier to work with.

Installing ampy is pretty straightforward as it is available using pip:
```
pip install adafruit-ampy
```

Once ampy is installed, you may run the following command to get an overview of the files that are available on the badge:

```
ampy -p /dev/cu.SLAB_USBtoUART ls
```

you will notice a file called ```boot.py```. This is the default file that is being ran when the badge is powered on. You can overwrite this file with your own version to execute your program.

## Blinking LED example

Create a file on your computer, `blink.py` with the following contents:

```
import time
from machine import Pin
led = Pin(2, Pin.OUT)
while True:
    led(1)
    time.sleep(1)
    led(0)
    time.sleep(1)
```

This little python program sets pin 2 (connected to an LED) as an output pin and indefinitely blinks the LED.

You can run this program on the ESP32 by executing the following `ampy` command:

`ampy --port /dev/tty.SLAB_USBtoUART run blink.py`

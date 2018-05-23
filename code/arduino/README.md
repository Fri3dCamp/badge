# Arduino IDE tutorial

This tutorial shows how to program the Fri3d Camp badge using the Arduino IDE.

## Installation

* Download the Arduino IDE from https://www.arduino.cc/en/Main/Software
* Follow the installation instructions from https://github.com/espressif/arduino-esp32 to install Arduino tools so you can program the ESP32 chip on the Fri3d Camp badge
* (Re)Start the Arduino IDE
* Connect the Fri3d Camp badge to your computer with a USB cable
* Under Tools > Board, select the ESP32 Dev Module
* Under Tools > Port, make sure that the correct port is selected (on Mac, this is usually `/dev/cu.SLAB_USBtoUART`)

You can now flash your C++ firmware for the Fri3d Camp badge with the Arduino IDE.

## Example code

### Blink an LED

As a our first "Hello World!" example, load the [blinking LED example](examples/blink/) and flash it to the ESP32. The status LED should now blink.

### Use multiple cores

The ESP32 has 2 cores and is built with FreeRTOS, which allows multiple processes to run simultaneously on these cores. [This YouTube video](https://www.youtube.com/watch?v=k_D_Qu0cgu8) provides a great introduction on how to run multiple processes, use semaphores and communicate between processes with the ESP32. 

The [dual core example](examples/dual_core) provides a simple example of multiple tasks running on different cores.

### Animate the eyes

TODO

### Connect to WiFi

TODO
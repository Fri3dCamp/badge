# Arduino library + Visual Studio Code + PlatformIO (PIO) tutorial

This tutorial shows how to program the Fri3d Camp badge using the Arduino
library in [Visual Studio Code](https://code.visualstudio.com/)
(VS Code for short), Microsoft's open source / freeware code editor in combination
with [PlatformIO](https://platformio.org/), an open source ecosystem for IoT
development.

This combination creates a powerful, fast, easy to use and cross platform IDE
for programming the Fri3d Camp badge.
PlatformIO will automatically download the necessary toolchain, compilers and
libraries and supports powerfull dependency management for Arduino libraries
(DHT, Servo, ...).
This way anyone can quickly set up a homogeneous, platform independent build
environment (Mac, Linux, Windows) and get started hacking the badge.


## Installation

* Download and install [Visual Studio Code](https://code.visualstudio.com/).
* Install the [PlatformIO IDE extension](https://platformio.org/install/ide?install=vscode)
in Visual Studio Code. You will be asked to reload VS Code a couple of times.
If everything went well you should be greated by the PIO Home screen in VS Code.
* You can read up on the PlatformIO documentation, browse through the supported
IoT platforms or check out some of the example projects.

## Configuration

PlatfromIO will generate a
[platformio.ini file](http://docs.platformio.org/en/latest/projectconf.html)
per project that you create.
In this file you can configure which IoT board your project uses (Arduino Uno,
ESP8266, ESP32, ...), which framework you use (Arduino, ESP-IDF, ...) and
optionally which libraries (and more importantly which version of those
libraries) your project uses (DHT temperature sensor, Servo library etc.).

This makes your project very portable between build environments.
Check out [the documentation at PlatfromIO](http://docs.platformio.org/en/latest/projectconf.html) for more information.

The Fri3d Camp badge uses the [espressif32 platform](http://docs.platformio.org/en/latest/platforms/espressif32.html).

## Example code

### Blink an LED

* Clone or download this Fri3d Camp repository if you haven't already done so.
* Open the blink example by opening the 'blink' folder under
/code/vscode-pio/examples in VS Code.
* Build the project by clicking the
checkmark in the PlatformIO toolbar at the bottom of the VS Code screen,
use the keyboard shortcut (Ctrl+Alt+b on Windows, Cmd+Shift+B on Mac) or
through the VS Code command palette (platformIO:Build).
PlatformIO should automatically download the ESP32 toolchain and its
dependencies and build the blink example without errors.
* Upload the program to your badge by clicking the right arrow icon in the
PlatformIO toolbar at the bottom, use the keyboard shortcut (Ctrl+Alt+u on
Windows, Option+Ctrl+u on Mac) or through the VS Code command palette
(platformIO:Upload).
If your badge is connected to your computer, PlatformIO should automatically
detect the port it's connected to and upload the program. The led on your
badge should start blinking.


### Use multiple cores

The ESP32 has 2 cores and is built with FreeRTOS, which allows multiple processes to run simultaneously on these cores. [This YouTube video](https://www.youtube.com/watch?v=k_D_Qu0cgu8) provides a great introduction on how to run multiple processes, use semaphores and communicate between processes with the ESP32.

The [dual core example](examples/dual_core) provides a simple example of multiple tasks running on different cores.

### Animate the eyes

TODO

### Connect to WiFi

TODO

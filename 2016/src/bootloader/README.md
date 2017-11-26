# Fri3d Camp Badge Bootloader

Een bootloader zorgt er voor dat de eerste software die op de microcontroller
de microcontroller toegankelijk maakt om er nieuwe software op te zetten zonder
een volledige programmerinfrastructuur. Concreet laat de Arduino bootloader toe
om via de Arduino IDE software te installeren op de microcontroller via de USB
kabel.

## Selecteren

Er zijn verschillende booloaders voor Arduino, maar slechts enkele komen in aanmerking voor onze microcontroller, de ATmega32u4.

We zijn vertrokken van de Arduino Micro Pro 3.3V vertrokken. Deze module werd ontworpen door Sparkfun en ze stellen ook een bootloader ter beschikking voor deze modules. We kunnen ze daarom ook hergebruiken. De bootloader voor deze module is een versie van de "caterina" bootloader.

Alle verschillende bootloaders zijn te vinden via [https://github.com/sparkfun/Arduino_Boards/tree/master/sparkfun/avr/bootloaders/caterina](https://github.com/sparkfun/Arduino_Boards/tree/master/sparkfun/avr/bootloaders/caterina)

Voorlopig hebben we na wat proberen gekozen voor de bootloader van de "[LilyPad USB](https://www.sparkfun.com/products/12049)". Deze module is ook gebaseerd op de ATmega32u4 en gebruikt ook de 3.3V opstelling aan 8MHz. Mogelijk zijn andere bootloaders ook mogelijk. We bekijken dit nog, maar voorlopig werkt deze keuze prima :-)

## Installeren

De Makefile in deze folder automatiseert de installatie aan de hand van de Atmel JTAGICE MkII programmer. Ze stuurt `avrdude` aan. Installatie van een bootloader vraagt twee stappen:

1. Het instellen van de `fuses` zodat de bootloader kan ingesteld worden.
2. Het effectief uploaden van de bootloader en het blokkeren ervan.

Wanneer je de Arduino IDE geïnstalleerd hebt, beschik je over een `boards.txt` bestand. Daarin vind je alle instellingen om de verschillende microcontrollers te programmeren. Je kan de instellingen die wij hier gebruiken ook hierin terugvinden:

Bv op Mac OS X kan je in de `Arduino.app` bundle het `boards.txt` bestand terugvinden als `Arduino.app/Contents/Java/hardware/arduino/avr/boards.txt`. Hierin vind je bv. een sectie over de Lilypad USB:

```
LilyPadUSB.bootloader.tool=avrdude
LilyPadUSB.bootloader.low_fuses=0xff
LilyPadUSB.bootloader.high_fuses=0xd8
LilyPadUSB.bootloader.extended_fuses=0xce
LilyPadUSB.bootloader.file=caterina-LilyPadUSB/Caterina-LilyPadUSB.hex
LilyPadUSB.bootloader.unlock_bits=0x3F
LilyPadUSB.bootloader.lock_bits=0x2F
```

We zien hier inderdaad dat de LilyPad voldoet aan onze mogelijkheden:

```
LilyPadUSB.build.mcu=atmega32u4
LilyPadUSB.build.f_cpu=8000000L
```

In het `boards.txt` bestand vinden we niet direct een andere module terug die de `atmega32u4` combineert met `8MHz`. Normaal gezien zou een "Arduino Micro Pro 3.3V" ook moeten lukken, maar dat is voorlopig nog niet bewezen ;-)

Om te installeren (met de zelfde programmer en instellingen als wij) volstaat een gewone `make`:

```bash
 make
*** unlocking MCU
!!! please toggle the power of the programmer
    Press any key to continue...
*** uploading bootloader
```

Normaal gezien zou de tussentijse reset van de programmer niet nodig mogen zijn, maar voorlopig geeft deze procedure de stabielste werking.

De twee commando's die onderliggend al het werk doen zijn:

```bash
$ avrdude -c jtag2isp -p atmega32u4 -P usb:5a:cb -b 19200 -e -U efuse:w:0xce:m -U hfuse:w:0xD8:m -U lfuse:w:0xFF:m -U lock:w:0x3f:m
$ avrdude -c jtag2isp -p atmega32u4 -P usb:5a:cb -b 19200 -e -U flash:w:Caterina-lilypadusb.hex -U lock:w:0x2F:m
```

## Zie ook ...

* [Arduino Hacking - Bootloader](https://www.arduino.cc/en/Hacking/Bootloader?from=Tutorial.Bootloader)
* [Sparkfun Tutorial on installing a bootloader](https://learn.sparkfun.com/tutorials/installing-an-arduino-bootloader)

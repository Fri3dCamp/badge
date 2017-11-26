AVRDUDE     ?= avrdude

PROGRAMMER  ?= jtag2isp
USB					?= usb:5a:cb

MCU         ?= atmega32u4
BAUD        ?= 19200

BOOTLOADER  ?= Caterina-lilypadusb.hex
EFUSE       ?= 0xce
HFUSE       ?= 0xd8
LFUSE       ?= 0xff
UNLOCK      ?= 0x3f
LOCK        ?= 0x2f

PROGRAM=$(AVRDUDE) -c $(PROGRAMMER) -p $(MCU) -P $(USB) -b $(BAUD) -e

all: unlock reset flash

unlock:
	@echo "*** unlocking MCU"
	-@$(PROGRAM) -U efuse:w:$(EFUSE):m \
               -U hfuse:w:$(HFUSE):m \
               -U lfuse:w:$(LFUSE):m \
               -U lock:w:$(UNLOCK):m

reset:
	@echo "!!! wait for the programmer to become ready"
	@read -p "    Press any key to continue... " -n1

flash:
	@echo "*** uploading bootloader"
	-$(PROGRAM) -U flash:w:$(BOOTLOADER) -U lock:w:$(LOCK):m

.PHONY: all unlock reset flash

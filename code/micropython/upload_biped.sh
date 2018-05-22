#!/bin/bash

ampy -p /dev/cu.SLAB_USBtoUART reset
sleep 2
ampy -p /dev/cu.SLAB_USBtoUART put examples/bot_test.py

sleep 2
ampy -p /dev/cu.SLAB_USBtoUART reset


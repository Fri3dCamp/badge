#!/bin/bash

ampy -p /dev/cu.SLAB_USBtoUART reset
sleep 2 
ampy -p /dev/cu.SLAB_USBtoUART rmdir fri3d
ampy -p /dev/cu.SLAB_USBtoUART put fri3d
ampy -p /dev/cu.SLAB_USBtoUART reset


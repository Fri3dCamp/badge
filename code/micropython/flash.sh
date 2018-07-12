#!/usr/bin/env bash

PORT=$1

# -- first flash the firmware
FLASH_COMPORT="/dev/cu.SLAB_USBtoUART"
FLASH_BDRATE="921600"

get_arguments() {
    POSITIONAL_ARGS=()
    local key="$1"
    J_OPTION=""

    while [[ $# -gt 0 ]]
    do
    local key="$1"
    case $key in
        -p|--port)
        FLASH_COMPORT="$2"
        shift # past argument
        shift # past value
        ;;
        -b|--bdrate)
        FLASH_BDRATE="$2"
        shift # past argument
        shift # past value
        ;;
        *)    # unknown option
        local opt="$1"
        if [ "${opt:0:2}" == "-j" ]; then
            J_OPTION=${opt}
        else
            POSITIONAL_ARGS+=("$1") # save it in an array for later
        fi
        shift # past argument
        ;;
    esac
    done
    #set -- "${POSITIONAL_ARGS[@]}" # restore positional parameters
}

get_arguments "$@"

esptool.py --chip esp32 --port ${FLASH_COMPORT} --baud ${FLASH_BDRATE} --before default_reset --after hard_reset write_flash -z --flash_mode dio --flash_freq 40m --flash_size detect 0x1000 esp32/bootloader/bootloader.bin 0xf000 esp32/phy_init_data.bin 0x10000 esp32/MicroPython.bin 0x8000 esp32/partitions_mpy.bin
sleep 3
rshell -p /dev/cu.SLAB_USBtoUART -b 115200 --ascii -f flash_commands
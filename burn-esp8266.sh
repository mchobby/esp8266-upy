#!/bin/bash
esptool.py --port /dev/ttyUSB0 --baud 460800 write_flash --flash_size=8m 0 esp8266-20161017-v1.8.5.bin 


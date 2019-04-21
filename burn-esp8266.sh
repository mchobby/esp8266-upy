#!/bin/bash
esptool.py --port /dev/ttyUSB0 --baud 115200 write_flash --flash_size=detect -fm dio 0 esp8266-20180511-v1.9.4.bin 


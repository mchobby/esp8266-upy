"""
 GPS MicroPython examples GPS Ultime breakout.

 CONFIGURE GPS & READ NMEA data

Where to buy:
* GPS-ULTIME: https://shop.mchobby.be/fr/breakout/62-gps-adafruit-ultimate-chipset-mtk3339--3232100000629-adafruit.html
* GPS-ULTIME: https://www.adafruit.com/product/746
* Pyboard: https://shop.mchobby.be/esp8266-esp32-wifi-iot/668-module-wifi-esp8266-carte-d-evaluation-3232100006683-olimex.html

The MIT License (MIT)
Copyright (c) 2018 Dominique Meurisse, support@mchobby.be, shop.mchobby.be
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

from machine import UART

# RMC (recommended minimum) et GGA (fix data)
PMTK_SET_NMEA_OUTPUT_RMCGGA = "$PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0*28" # turn on GPRMC and GPGGA
# 5 Hz update
PMTK_SET_NMEA_UPDATE_5HZ = "$PMTK220,200*2C"


ser1 = UART( 1, 9600 )
# send the commands
ser1.write( PMTK_SET_NMEA_OUTPUT_RMCGGA )
ser1.write( bytes([13,10]) )
ser1.write( PMTK_SET_NMEA_UPDATE_5HZ )
ser1.write( bytes([13,10]) )

MAX_BUF_SIZE = 120
buf = bytearray( MAX_BUF_SIZE )
lineidx=0 # Index when filling the line

def process_buffer( buffer, length ):
	# Buffer have a fixed length of 120 chars. Content is smaller
	print( buffer[:length] )

# Read the data and forward it to the input buffer
while True:
	if not ser1.any():
		continue
	data = ser1.read()
	for i in range( len(data)):
		buf[lineidx] = data[i]
		if data[i] != 10: # CR/LF
			lineidx += 1
		else:
			process_buffer( buf, lineidx+1 )
			lineidx = 0
		if lineidx >= MAX_BUF_SIZE:
			raise Exception( 'Exceed buffer size')

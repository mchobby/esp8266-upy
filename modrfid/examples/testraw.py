"""
    MOD-RFID1356MIFARE reader test.

    Read the data coming from RFID reader
	see protocol details on https://www.olimex.com/wiki/MOD-RFID1356MIFARE


Where to buy:
* MOD-RFID1356MIFARE : https://shop.mchobby.be/product.php?id_product=1619
* MOD-RFID1356MIFARE : https://www.olimex.com/Products/Modules/RFID/MOD-RFID1356MIFARE/
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


ser1 = UART( 1, baudrate=38400 )
# send the commands

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
		if data[i] == 10: # CR/LF
			process_buffer( buf, lineidx+1 )
			lineidx = 0
		elif data[i]==62 and (lineidx==0): # >
			# received a prompt > characters (just after emitting some data)
			# Do not wait for \r\n that will not come immediately
			process_buffer( buf, lineidx+1 )
		else:
			lineidx += 1

		if lineidx >= MAX_BUF_SIZE:
			raise Exception( 'Exceed buffer size')

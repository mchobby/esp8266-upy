[Ce fichier existe également en FRANCAIS](readme.md)

# Use an Olimex's MOD-Wii-UEXT-NUNCHUCK with MicroPython

The WII NUNCHUCK is the game controler for the Wii gaming station.

This I2C controler is fitted with the UEXT connector to helps wiring.

![The MOD-Wii-UEXT-NUNCHUCK Nunchuck game contoler](docs/_static/mod-wii.png)

This controler does have the following features:
* 3 axis accelerometer
* Analog joystick for X-Y
* Two buttons C & Z
* __I2C interface__
* UEXT connector


# A word about ESP8266-EVB under MicroPython
Before to use this module, it will be necessary to flash the MicroPython firmware ontor the ESP8266.

You can read the steps on our [ESP8266-EVB](https://wiki.mchobby.be/index.php?title=ESP8266-DEV) tutorial (on MCHobby's WIKI, French).


## UEXT connector

On the ESP8266-EVB, the UEXT connector does ship UART, SPI, I2C buses as well as 3.3V power. The UEXT pins to ESP8266 GPIO are descrived in the following picture.

![UEXT connector](docs/_static/ESP8266-EVB-UEXT.jpg)

# Brancher

## ESP8266-EVB (Olimex)
As first operation, I did plug a [UEXT Splitter](http://shop.mchobby.be/product.php?id_product=1412) to duplicates the UEXT port. We do need to use the serial lines for the REPL session with the computer __and__ we do need to plug the Game Controler.

![Wiring with UEXT](docs/_static/mod-wii-wiring.jpg)

## MicroPython Pyboard

You can also wire it on you MicroPython Pyboard. To do so, just wire an UEXT male connector to you Pyboard as displayed here below THEN plug your wii nunchuck on it.

![WII Nunchuck to Pyboard](docs/_static/wii-nunchuck-to-pyboard.jpg)

# Library

Before using the examples, you will need to transfert le library __bibliothèque `wiichuck.py`__ to your MicroPython board.

Then you can copy the following examples file to your board.
* `testtest.py`
* `testcount.py`
* `testacc.py`

The `wiichuck.py` library does offer the following features

__property:__
* `c`  : True/False when the C button is pressed or released.
* `z`  : True/False, when the Z button is pressed or released.
* `c_count` : the number of pressure on C button since the last `c_count` read. Reset the counter when read. Effectiveness of the detection depends on the `update()` method call.
* `z_count` : the number of pressure on Z button since the last  `z_count` read. Réinitialize la valeur à 0. Effectiveness of the detection depends on the `update()` method call.
*  `joy_x`  : return current position of joystick X axis. Returns an integer from -128 (left) et +128 (right)
*  `joy_y`  : return current position of joystick Y axis. Returns an integer from -128 (backward) et +128 (forward)
* `joy_right`  : is the joystick moved to right (over minimum threshold).
* `joy_left`  : is the joystick moved to left (over minimum threshold).
* `joy_up`  : is the joystick moved to up (over minimum threshold).
* `joy_down` : is the joystick moved to down (over minimum threshold).
* `accel_x`  : read the accelerometer on X axis.
* `accel_y`  : read the accelerometer on Y axis.
* `accel_z`  : read the accelerometer on Z axis.
* `roll`  : Rool angle of the controller (in degrees). Just rolling your wrist to left or right!
* `pitch`  : The "pitch" angle (in degrees), arm move toward the top or toward the bottom.

__Methods:__
* `update()`   : must be call to fetch the informations from the Wii Nunchuck. Informations that can be readed from various properties.

# Test
## Example for read the joystick and buttons
```
# Test the Olimex MOD-Wii-UEXT-NUNCHUCK game controler.
#
# MOD-Wii-UEXT-NUNCHUCK : http://shop.mchobby.be/product.php?id_product=1416
# MOD-Wii-UEXT-NUNCHUCK : https://www.olimex.com/Products/Modules/Sensors/MOD-WII/MOD-Wii-UEXT-NUNCHUCK/  

from machine import I2C, Pin
from time import sleep_ms
from wiichuck import WiiChuck

# Pyboard
# i2c=I2C(2)
i2c = I2C( sda=Pin(2), scl=Pin(4) )
wii = WiiChuck( i2c ) # default address=0x58

while True:
	# Detect direction from boolean property
	direction = ''
	if wii.joy_up:
		direction = 'Up'
	elif wii.joy_down:
		direction = 'Down'
	elif wii.joy_right:
		direction = '>>>'
	elif wii.joy_left:
		direction = '<<<'

	print( "-"*20 )
	# Test button states
	print( "Button C: %s" % wii.c )
	print( "Button Z: %s" % wii.z )
	# print X, Y analog value + detected direction
	print( "Joy X, Y: %4d,%4d  (%s)" % (wii.joy_x, wii.joy_y, direction) )

	wii.update()
	sleep_ms( 150 )
```

Which produces the following results:

```
Button C: False
Button Z: False
Joy X, Y:    0, 123  (Up)
--------------------
Button C: False
Button Z: False
Joy X, Y:    0, 123  (Up)
--------------------
Button C: False
Button Z: False
Joy X, Y:    0,  28  ()
--------------------
Button C: False
Button Z: False
Joy X, Y:    0,   0  ()
--------------------
Button C: False
Button Z: False
Joy X, Y:    0,  -3  ()
--------------------
Button C: False
Button Z: False
Joy X, Y:    3,-132  (Down)
--------------------
Button C: False
Button Z: False
Joy X, Y:    5,-132  (Down)
```

## Example counting button pressure
See the file [testcount.py](examples/testcount.py) .

Count the number of pressures on C & Z buttons between 2 consecutive call to `c_count()` & `z_count()`.

```
# Test the Olimex MOD-Wii-UEXT-NUNCHUCK game controler.
#
# MOD-Wii-UEXT-NUNCHUCK : http://shop.mchobby.be/product.php?id_product=1416
# MOD-Wii-UEXT-NUNCHUCK : https://www.olimex.com/Products/Modules/Sensors/MOD-WII/MOD-Wii-UEXT-NUNCHUCK/  

from machine import I2C, Pin
import time
from wiichuck import WiiChuck

# Pyboard
# i2c=I2C(2)
i2c = I2C( sda=Pin(2), scl=Pin(4) )
wii = WiiChuck( i2c ) # default address=0x58

dir_time   = time.time()
count_time = time.time()
while True:
	if time.time()-dir_time > 0.5:
		# Detect direction from boolean property
		direction = ''
		if wii.joy_up:
			direction = 'Up'
		elif wii.joy_down:
			direction = 'Down'
		elif wii.joy_right:
			direction = '>>>'
		elif wii.joy_left:
			direction = '<<<'
		print( "Joy direction : %s" % (direction) )
		dir_time = time.time()

	if time.time()-count_time > 2:
		# Test button states
		print( "C Button pressure count: %s" % wii.c_count )
		print( "Z Button pressure count: %s" % wii.z_count )
		count_time = time.time()

	wii.update()
	time.sleep_ms( 5 )
```

Which produce the following result:

```
Joy direction : Up
C Button pressure count: 2
Z Button pressure count: 1
Joy direction :
Joy direction :
Joy direction : Down
C Button pressure count: 0
Z Button pressure count: 7
Joy direction : Down
Joy direction :
Joy direction :
C Button pressure count: 1
Z Button pressure count: 1
Joy direction :
Joy direction :
Joy direction :
C Button pressure count: 2
Z Button pressure count: 5
Joy direction :

```

## Example of accelerometer reading

Content of this file is available in [testacc.py](examples/testacc.py) .

Displays the accelerometer data as well as the 'pitch' & 'roll' en degrees.

```
# Test the Olimex MOD-Wii-UEXT-NUNCHUCK game controler.
#
# MOD-Wii-UEXT-NUNCHUCK : http://shop.mchobby.be/product.php?id_product=1416
# MOD-Wii-UEXT-NUNCHUCK : https://www.olimex.com/Products/Modules/Sensors/MOD-WII/MOD-Wii-UEXT-NUNCHUCK/  

from machine import I2C, Pin
import time
from wiichuck import WiiChuck

i2c = I2C( sda=Pin(2), scl=Pin(4) )
wii = WiiChuck( i2c ) # default address=0x58

acc_time   = time.time()
while True:
	if time.time()-acc_time > 0.5:
		print( '-'*20 )
		print( "Joy Accelerometer x,y,z  : %4d, %4d, %4d" % (wii.accel_x, wii.accel_y, wii.accel_z) )
		# https://www.novatel.com/solutions/attitude/
		# pitch = airplane nose up/down
		# roll  = airplane rooling to right / left
		print( "Joy roll, pitch (degrees): %4d, %4d" % (wii.roll, wii.pitch) )
		acc_time = time.time()

	wii.update()
	time.sleep_ms( 5 )
```

Which produces the following result

```
--------------------
Joy Accelerometer x,y,z  :   81,    1,  299
Joy roll, pitch (degrees):   15,   89
--------------------
Joy Accelerometer x,y,z  :  145,   -3,  275
Joy roll, pitch (degrees):   27,   90
--------------------
Joy Accelerometer x,y,z  :  -15,  -11,  311
Joy roll, pitch (degrees):   -2,   93
--------------------
Joy Accelerometer x,y,z  : -139,   -3,  271
Joy roll, pitch (degrees):  -27,   90
--------------------
Joy Accelerometer x,y,z  :  -19,    1,  311
Joy roll, pitch (degrees):   -3,   89
--------------------
Joy Accelerometer x,y,z  :   -3, -135,  259
Joy roll, pitch (degrees):    0,  130
--------------------
Joy Accelerometer x,y,z  :  -11, -143,  259
Joy roll, pitch (degrees):   -2,  132
--------------------
Joy Accelerometer x,y,z  :  -11,  -47,  303
Joy roll, pitch (degrees):   -2,  102
--------------------
Joy Accelerometer x,y,z  :    9,   61,  299
Joy roll, pitch (degrees):    1,   73
--------------------
Joy Accelerometer x,y,z  :   21,  145,  283
Joy roll, pitch (degrees):    4,   46
--------------------
Joy Accelerometer x,y,z  :   -7,   41,  307
Joy roll, pitch (degrees):   -1,   78
--------------------
Joy Accelerometer x,y,z  :  -11,   13,  307
Joy roll, pitch (degrees):   -2,   86
```

# Shopping list
* Shop: [Wii Nunchuck UEXT controler](http://shop.mchobby.be/product.php?id_product=1416)
* Shop: [Module WiFi ESP8266 - evaluation board (ESP8266-EVB)](http://shop.mchobby.be/product.php?id_product=668)
* Shop: [UEXT Splitter](http://shop.mchobby.be/product.php?id_product=1412)
* Shop: [Câble console](http://shop.mchobby.be/product.php?id_product=144)
* Wiki: https://wiki.mchobby.be/index.php?title=MICROPYTHON-MOD-WII-NUNCHUCK

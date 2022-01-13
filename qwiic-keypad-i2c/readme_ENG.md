[Ce fichier existe également en Français](readme.md)

# Use the Qwiic 12 Keys I2C Keypad with MicroPython

SparkFun manufacture the [12 keys I2C keypad](https://www.sparkfun.com/products/15290) using the Qwiic connector (SparkFun, COM-15290).

![SparkFun 12 key Qwiic I2C Keypad](docs/_static/Keypad-Qwiic.jpg)

This __autonomous keypad__ is able to record keys (and respective timing) even when data is not readed for a while!

It is really a great feature!

# Library

Before to test the I2C keypad, it will be necessary to copy the [kpadi2c.py](lib/kpadi2c.py) library on the MicroPython board.

Bibliothèques:
* [kpadi2c.py](lib/kpadi2c.py) : bibliothèque de base permettant d'interagir avec le module KeyPad I2C.
* [kpadcode.py](lib/kpadcode.py) : bibliothèque complémentaire à [kpadi2c.py](lib/kpadi2c.py) destiné à la saisie type "DigiCode".

# Wiring

## wire to a MicroMod-RP2040

In this example, the [MicroMod Learning Machine](https://www.sparkfun.com/products/16400) carrier board (SparkFun,  DEV-16400) is used to offers the Qwiic connectivity to the MicroMod-RP2040

![Qwiic Keypad to MicroMod RP2040](docs/_static/keypad-to-micromod-rp2040.jpg)

## Wire to a Raspberry-Pi Pico

You can also wire the Keypad to other microcontroler thanks to the [Qwiic Cable Breakout](https://www.sparkfun.com/products/14425) (SparFun, PRT-14425)

![Qwiic Keypad to Raspberry-Pi Pico](docs/_static/keypad-to-pico.jpg)

# Testing

All the examples would need the [kpadi2c.py](lib/kpadi2c.py) library onto the MicroPython board.

Somes examples would also needs for the [kpadcode.py](lib/kpadcode.py) to run properly.

## test.py : reading the keys

The [test.py](examples/test.py) script just read the keys pressed on the Keypad and print them on the REPL console.

The script will ends when then "*" is pressed.

``` python
from machine import I2C, Pin
from kpadi2c import Keypad_I2C
import time

# MicroMod-RP2040 - SparkFun
i2c = I2C( 0, sda=Pin(4), scl=Pin(5) )
# Raspberry-Pi Pico
# i2c = I2C( 1 ) # sda=GP6, scl=GP7

kpad = Keypad_I2C( i2c )
print( 'KeyPad connected:', 'Yes' if kpad.is_connected else 'NO' )
print( 'Version:', kpad.version )
print( 'Press buttons: * to exit reading loop')
while True:
	kpad.update_fifo()
	_btn = kpad.button # Return ASCII code
	while _btn != 0:
		print( "ASCII: %s,  Char: %s" % (_btn, chr(_btn) ) )
		if _btn == 42:
			raise Exception( 'User Exit!' )
		kpad.update_fifo()
		_btn = kpad.button # read next
	time.sleep_ms( 200 )
```

This produce the following into the REPL session.

```  
>>> import test
KeyPad connected: Yes
Version: v1.0
Press buttons: * to exit reading loop
ASCII: 49,  Char: 1
ASCII: 50,  Char: 2
ASCII: 51,  Char: 3
ASCII: 52,  Char: 4
ASCII: 53,  Char: 5
ASCII: 54,  Char: 6
ASCII: 55,  Char: 7
ASCII: 56,  Char: 8
ASCII: 57,  Char: 9
ASCII: 48,  Char: 0
ASCII: 35,  Char: #
ASCII: 35,  Char: #
ASCII: 35,  Char: #
ASCII: 42,  Char: *
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "test.py", line 34, in <module>
Exception: User Exit!
>>>
```

## Test2.py : Reading keys and timing

The Keypad Qwiic modules also record the timing when a key is pressed.

The keys and timing are recorded into the keypad memory so it records keypress even when the module is not queried by the MicroControler.

``` python
from machine import I2C, Pin
from kpadi2c import Keypad_I2C
import time

# MicroMod-RP2040 - SparkFun
i2c = I2C( 0, sda=Pin(4), scl=Pin(5) )
# Raspberry-Pi Pico
# i2c = I2C( 1 ) # sda=GP6, scl=GP7

kpad = Keypad_I2C( i2c )
print( 'KeyPad connected:', 'Yes' if kpad.is_connected else 'NO' )
print( 'Version:', kpad.version )
while True:
	kpad.update_fifo()
	_btn   = kpad.button # Return ASCII code
	_deltaT= kpad.time_since_pressed
	if _btn == 0: # no reading
		time.sleep_ms( 200 )
		continue # restart loop

	print( "Button %s was pressed %d milliseconds ago." % (chr(_btn),_deltaT) )
```

Which produce the following onto the REPL session:

```
>>> import test2
KeyPad connected: Yes
Version: v1.0
Button 3 was pressed 18463 milliseconds ago.
Button 3 was pressed 18182 milliseconds ago.
Button 3 was pressed 17866 milliseconds ago.
Button 6 was pressed 17481 milliseconds ago.
Button 1 was pressed 16160 milliseconds ago.
Button 7 was pressed 15076 milliseconds ago.
Button # was pressed 13685 milliseconds ago.
Button 9 was pressed 28 milliseconds ago.
Button 8 was pressed 168 milliseconds ago.
Button 7 was pressed 74 milliseconds ago.
Button 6 was pressed 144 milliseconds ago.
Button 5 was pressed 172 milliseconds ago.
Button 4 was pressed 97 milliseconds ago.
Button 3 was pressed 99 milliseconds ago.
Button 2 was pressed 101 milliseconds ago.
Button 1 was pressed 41 milliseconds ago.
Button # was pressed 60 milliseconds ago.
Button # was pressed 100 milliseconds ago.
Button * was pressed 186 milliseconds ago.
Button * was pressed 160 milliseconds ago.
```

The 7 first results matches some keys pressed before the execution of the script. This means that they were recorded into the module memory by waiting the script to read them.

Those keys are reads (and pop out of the module) when then script starts.

The others keys are read along the time at key presses by the script running on the microcontroler, this explains why it doesn't exeeds 200ms of delay (the pause/sleep used inside the script).

## checkcode.py : digital code door entrance

The [checkcode.py](examples/checkcode.py) example script do implement a digital code door entrance with the I2C Keypad.

This example requires the [kpadcode.py](lib/kpadcode.py) library to be copied on the MicroPython board.

``` python
from machine import I2C, Pin
from kpadcode import CodeChecker
import time

# MicroMod-RP2040 - SparkFun
i2c = I2C( 0, sda=Pin(4), scl=Pin(5) )
# Raspberry-Pi Pico
# i2c = I2C( 1 ) # sda=GP6, scl=GP7

# Callback function used by the CodeChecker to give information about user encoding
def update_display( user_entry, timeout ):
	# user_entry : string
	# timeout : True when nothing more is keyed in by user (and user_entry clearance)
	if timeout:
		print( 'Callback: timeout!' )
	print( 'Callback: "%s"' % user_entry )

locker = CodeChecker( i2c, address=0x4B, code='1234*' ) # secret code is '1234*'
locker.on_update = update_display # set the callback function
print( 'KeyPad connected:', 'Yes' if locker.is_connected else 'NO' )
print( 'Version:', locker.version )

locked = True
while locked:
	print( '==== Enter KeyCode to Unlock ====' )
	# execute() queries the KeyPad for code. Returns True when code is correct.
	# Returns false when user is inactive until the timeout
	locked = not( locker.execute() )
	if locked:
		print( 'Execute() timeout! Try again' )

# Loop exits only when code is right
print( 'Yes! Unlocked!' )
```
Which produces the following results:

```
MicroPython v1.17 on 2021-09-02; Raspberry Pi Pico with RP2040
Type "help()" for more information.
>>> import checkcode
KeyPad connected: Yes
Version: v1.0
==== Enter KeyCode to Unlock ====
Callback: "     "
Callback: "5    "
Callback: "55   "
Callback: "555  "
Callback: "5555 "
Callback: "55555"
Callback: "     "

Callback: "     "
Callback: "4    "
Callback: "44   "
Callback: timeout!
Callback: "     "
Callback: "4    "
Callback: "44   "
Callback: "444  "
Callback: timeout!
Callback: "     "
Execute() timeout! Try again
==== Enter KeyCode to Unlock ====
Callback: "     "
Execute() timeout! Try again
==== Enter KeyCode to Unlock ====
Callback: "     "
Execute() timeout! Try again
==== Enter KeyCode to Unlock ====
Callback: "     "
Callback: "6    "
Callback: "66   "
Callback: "666  "
Callback: "6666 "
Callback: "66666"
Callback: "     "
Callback: timeout!
Callback: "     "
Execute() timeout! Try again
==== Enter KeyCode to Unlock ====
Callback: "     "
Callback: "1    "
Callback: "12   "
Callback: "123  "
Callback: "1234 "
Callback: "12345"
Callback: "     "
Callback: "1    "
Callback: "12   "
Callback: "123  "
Callback: "1234 "
Callback: "1234*"
Yes! Unlocked!
```

## multicode.py : mutiple digital code door entrance

The [multicode.py](examples/multicode.py) does support several code entrance.

This example requires the [kpadcode.py](lib/kpadcode.py) library to be copied on the MicroPython board.

``` python
from machine import I2C, Pin
from kpadcode import CodeChecker

# MicroMod-RP2040 - SparkFun
i2c = I2C( 0, sda=Pin(4), scl=Pin(5) )
# Raspberry-Pi Pico
# i2c = I2C( 1 ) # sda=GP6, scl=GP7

code_list = ['1*123','2*777','3*456','4*###','12345']

locker = CodeChecker( i2c, address=0x4B, code=code_list )
print( 'KeyPad connected:', 'Yes' if locker.is_connected else 'NO' )
print( 'Valid codes: ',code_list)

while True:
	print( '==== Enter KeyCode  ====' )
	if locker.execute():
		print( 'Code "%s" catched!' % locker.user_entry )
```

Which will produce the following result:
```
Connected to MicroPython at /dev/ttyACM0
Use Ctrl-] to exit this shell

>>> import multicode
KeyPad connected: Yes
Version: v1.0
Valid codes:  ['1*123', '2*777', '3*456', '4*###', '12345']
==== Enter KeyCode  ====
Code "1*123" catched!
==== Enter KeyCode  ====
==== Enter KeyCode  ====
Code "2*777" catched!
==== Enter KeyCode  ====
Code "4*###" catched!
==== Enter KeyCode  ====
==== Enter KeyCode  ====
==== Enter KeyCode  ====
==== Enter KeyCode  ====
==== Enter KeyCode  ====
Code "3*456" catched!
```

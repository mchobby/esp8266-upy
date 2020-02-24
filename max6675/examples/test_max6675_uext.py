"""
TC-MOD test script - MAX6675 Type-K thermocouple amplifier
==========================================================
This library supports the use of the TC-MOD (exposing UEXT connector) for
thermocouple reading under MicroPython.

For wiring, see the:
* Pyboard-Uno-R3 adapter : https://github.com/mchobby/pyboard-driver/tree/master/UNO-R3
* Pyboard UEXT connector : https://github.com/mchobby/pyboard-driver/tree/master/UEXT

Author(s):
* Meurisse D for MC Hobby sprl
"""

from max6675 import MAX6675
from time import sleep

print( "MAX6675 - thermocouple reading")
# PYBOARD-UEXT adapter -> cs_pin = "Y5"
# sensor = MAX6675( data_pin = "Y7", clk_pin = "Y6" , cs_pin="Y5" )

# PYBOARD-UNO-R3 adapter -> cs_pin = "X8"
sensor = MAX6675( data_pin = "Y7", clk_pin = "Y6" , cs_pin="X8" ) 


# Wait the MAX6675 to stabilize
sleep( 0.500 )

while True:
	print( "C = %s" % sensor.temperature )
	sleep(1)

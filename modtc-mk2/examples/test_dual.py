# Read the temperature from two distinct MOD-TC-MK2-31855
# The modules must have different I2C addres.
#
from machine import I2C
from modtc_mk2 import MODTC_MK2
from time import sleep

# The address of the two modules
MK2_ADDR_1 = 0x23
MK2_ADDR_2 = 0x25

# PYBOARD-UNO-R3 & UEXT for Pyboard. SCL=Y9, SDA=Y10
i2c = I2C(2)
mk_dic = { 'temp 1' : MODTC_MK2( i2c, address=MK2_ADDR_1 ),
		   'temp 2' : MODTC_MK2( i2c, address=MK2_ADDR_2 )   }

while True:
	print( "-"*40 )
	for name, mk2 in mk_dic.items():
		temp = mk2.temperatures[1]
		print( "%s : %5.2f C" % (name, temp) )
	sleep(1)

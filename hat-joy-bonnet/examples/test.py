from machine import I2C
from joybonnet import JoyBonnet
from time import sleep

# NADHAT PYB405 with HAT connector
i2c = I2C( 1 )
joy = JoyBonnet( i2c )

# Read a button
print( "Push the START button" )
for i in range( 10 ):
	print( '%i/10 -> Read START button = %s' %(i, joy.button('START')) )
	sleep( 1 )

# Read all button
print( "Push the buttons" )
for i in range( 10 ):
	print( '%i/10 -> all button = %s' %(i, joy.all_buttons) )
	sleep( 1 )

# Read X,Y axis between -100 <-> +100
print( "Move the Joystick" )
for i in range( 20 ):
	print( 'x, y = %i, %i' % joy.axis )
	sleep(0.5)

# List the button name
print( joy.pin_setup.keys() )
# will display
#  dict_keys(['A', 'Y', 'X', 'B', 'PLAYER2', 'SELECT', 'START', 'PLAYER1'])

print( "That's all Folks" )

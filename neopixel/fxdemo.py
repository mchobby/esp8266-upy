# Utilisation de la bibliothèque neopixel avec Feather ESP8266 sous MicroPython
# 
# Differente fonctions permettant de réaliser des animations lumineuses
#
# Shop: https://shop.mchobby.be/55-leds-neopixels-et-dotstar
# Wiki: https://wiki.mchobby.be/index.php?title=MicroPython-Accueil#ESP8266_en_MicroPython

from machine import Pin
from neopixel import NeoPixel
from time import sleep
from os import urandom

NEOPIXEL_PIN = 2
NEOPIXEL_COUNT = 8
NEOPIXEL_WAIT = 0.010 # 10 ms

# NeoPixel( broche_signal, nbre_de_led )
np = NeoPixel( Pin(NEOPIXEL_PIN), NEOPIXEL_COUNT )
np.fill( (0,0,0) )
np.write()

def wheel( wheel_pos ):
	""" caculate color based on a color wheel. 
	    Color are transistion r - g - b back r based on wheel_pos (0-255) """
	assert 0<= wheel_pos <= 255, "Invalid wheel_pos!"
	
	wheel_pos = 255 - wheel_pos
	if( wheel_pos < 85 ):
		return ( 255-(wheel_pos*3), 0, wheel_pos*3 )
	elif( wheel_pos < 170 ):
		wheel_pos -= 85
		return ( 0, wheel_pos*3, 255-(wheel_pos*3) )
	else:
		wheel_pos -= 170
		return ( wheel_pos*3, 255-(wheel_pos*3), 0 )

def set_color( np, pos, color ):
	""" Set the color in a safe way. """
	# Normal NeoPixel code would update the last pixel for np[-1]=color
	if 0 <= pos < np.n:
		np[pos] = color

def cycle_wheel( np ):
	""" All neopixels change color following a color wheel """   
	for color in range( 256 ):
		np.fill( wheel(color) )
		np.write()
		sleep( NEOPIXEL_WAIT )

def moving_wheel( np, wheel_pos=0, iteration=500, wheel_step = 4 ):
	""" Cycle rainbow color over a series of NeoPixel """ 
	while iteration > 0:
		iteration -= 1
		# Starting Rainbow color for the ribbon
		ruban_pos = wheel_pos

		# iterate Raibow color over the Ribbon 
		for i in range( np.n ):
			np[i] = wheel( ruban_pos )
			ruban_pos += wheel_step
			if ruban_pos > 255:
				ruban_pos = 0
		
		np.write()
		sleep( NEOPIXEL_WAIT )

		# next starting color
		wheel_pos += 1
		if wheel_pos > 255:
			wheel_pos = 0
	
	return wheel_pos

def fade_inout( np, color, step=5 ):
	assert len(color)==3, "Invalid color tuple!"
	for b in range( 0, 256, step ):
		col = ( (color[0]*b)//255 , (color[1]*b)//255, (color[2]*b)//255 ) 
		np.fill( col )
		np.write()
		sleep( NEOPIXEL_WAIT )
	for b in range( 255, -1, -1*step ):
		col = ( (color[0]*b)//255 , (color[1]*b)//255, (color[2]*b)//255 ) 
		np.fill( col )
		np.write()
		sleep( NEOPIXEL_WAIT )

def candle( np, iteration=1000 ):
	assert np.n < 256, "Too much pixels!"
	while iteration>0 :
		iteration -= 1
		rnd = urandom(3) # generate 3 random bytes (0-255)
		green = 50 + int(rnd[0]) 
		red   = green + int(rnd[1]) 
		# Which NeoPixel to update
		pos = int(rnd[2])%np.n
		np[pos] = ( red, green, 0 )
		np.write()
		sleep( 0.005 ) # 5ms

def larson_scanner( np, posdir=None, iteration=100, pause=0.100 ):
	""" Larson Scanner (K2000) effect
	posdir : a tuple (pos,dir) with pos = position of the eye
									dir = direction of the eye """

	assert np.n > 4, "Too few pixels"
	assert (posdir==None) or (len(posdir)==2), "Invalid posdir"
	
	if posdir:
		pos = posdir[0]
		dir = posdir[1]
	else:
		pos,dir = 0, 1

	while iteration > 0:
		iteration -= 1
		set_color( np, pos-2, (0x10,0x00,0x00) ) # Dark red
		set_color( np, pos-1, (0x80,0x00,0x00) ) # Medium Red
		set_color( np, pos  , (0xFF,0x30,0x00) ) # Center Pixel (brightest)
		set_color( np, pos+1, (0x80,0x00,0x00) ) # Medium Red
		set_color( np, pos+2, (0x10,0x00,0x00) ) # Dark red
		np.write()
		sleep( pause )

		# Erase the pixels
		for i in range( -2, +2+1 ):
			set_color( np, pos + i, (0,0,0) )

		# Move the eye
		pos += dir
		if pos<0:
			pos = 1
			dir = 1
		elif pos >= np.n:
			pos = np.n-2
			dir = -1

	# return current state		
	return (pos,dir)

def rainbow7( np, pos ):
	set_color( np, pos % np.n , (0,0,0) )
	set_color( np, (pos +1) % np.n, (25, 0, 25))   # violet
	set_color( np, (pos +2) % np.n, (255, 0, 255)) # indigo
	set_color( np, (pos +3) % np.n, (0, 0, 150))   # blue
	set_color( np, (pos +4) % np.n, (0, 150, 0))   # green
	set_color( np, (pos +5) % np.n, (255, 255, 0)) # yellow
	set_color( np, (pos +6) % np.n, (110, 70, 0))  # orange
	set_color( np, (pos +7) % np.n, (150, 0, 0))   # red
	np.write();

def moving_rainbow( np, pause=0.100 ):
	for i in range( np.n ):
		rainbow7( np, i )
		sleep( pause )

# --- Test the functions ---

# Moving_rainbow
for i in range( 4 ):
	moving_rainbow( np )
np.fill( (0,0,0) )
np.write()
sleep( 1 )

# Fade In And Out
fade_inout( np, (255,   0,   0) ) # Red
fade_inout( np, (0  , 255,   0) ) # Green
fade_inout( np, (0  ,   0, 255) ) # Blue
np.fill( (0,0,0) )
np.write()
sleep( 1 )

# moving_wheel
moving_wheel( np )
np.fill( (0,0,0) )
np.write()
sleep( 1 )

# cycle_wheel
for i in range(2):
	cycle_wheel( np )
np.fill( (0,0,0) )
np.write()
sleep( 1 )

# Candle Effect
candle( np )
np.fill( (0,0,0) )
np.write()
sleep( 1 )

# Larson Scanner (K2000)
#   execute 3 iterations
posdir = None
for i in range( 3 ):
	posdir = larson_scanner( np, posdir )
np.fill( (0,0,0) )
np.write()
sleep( 1 )

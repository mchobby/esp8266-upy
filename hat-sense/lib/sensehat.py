# Driver for Sense-Hat (originally designed for Raspberry-Pi) using the I2C machine API
#
# See GitHub: https://github.com/mchobby/esp8266-upy/tree/master/hat-sense
#
# Author:
#   Meurisse D. for shop.mchobby.be - 29 Aug. 2020 - MicroPython portage
#   Larry Bank - 11/10/2017 - Initial C code
#
# Note: driver based on the "Sense Hat Unchained" ( https://github.com/bitbank2/sense_hat_unchained )
#       work from bitbank2
#

__version__ = '0.0.1'

from framebuf import FrameBuffer, RGB565, MONO_VLSB
import time

LED_MATRIX_ADDR = 0x46 # Atmel handling the LED Matrix and Joystick
ACC_ADDR = 0x6A # Accelerometer + Gyroscope
MAG_ADDR = 0x1C # Magnetometer
HUM_ADDR = 0x5f # Humidity Sensor
PRESS_ADDR=0x5C # Pressure sensor

# Joystick definition
JOY_DOWN = 1
JOY_UP   = 4
JOY_LEFT = 16
JOY_RIGHT= 2
JOY_ENTER= 8

class SenseHat( FrameBuffer ):
	def __init__(self, i2c ):
		""" initialize the sense HAT to work on the specified I2C bus """
		self.i2c = i2c
		self.buf1 = bytearray( 1 ) # Various read buffer
		self.buf3 = bytearray( 3 )
		self.buf4 = bytearray( 4 )
		self.buf5 = bytearray( 5 )
		self.buf6 = bytearray( 6 )

		# FrameBuffer
		self.buf = bytearray( 8*8*2 ) # 8x8 pixels, 2 byte per pixel for RGB565
		self.buf_leds = bytearray( 8*8*3 ) # 8x8 pixels, 3 byte per pixel for sending data to the LCD
		super().__init__( self.buf, 8, 8, RGB565 ) # Initialize the FrameBuffer

		self.clear()

		# humidity/temp calibration values
		self.H0_rH_x2, self.H1_rH_x2, self.T0_degC_x8 = None, None, None
 		self.T1_degC_x8, self.H0_T0_OUT          = None, None
		self.H1_T0_OUT, self.T0_OUT, self.T1_OUT      = None, None, None

		# Prepare humidity sensor
		self.i2c.readfrom_mem_into( HUM_ADDR, 0x10, self.buf1 ) # AV_CONF
		self.buf1[0] &= 0xc0
		self.buf1[0] |= 0x1b # avgt=16, avgh=32
		self.i2c.writeto_mem( HUM_ADDR, 0x10, self.buf1 )

		self.i2c.readfrom_mem_into( HUM_ADDR,0x20+0x80, self.buf3 ) # get CTRL_REG 1-3
		self.buf3[0] &= 0x78  # keep reserved bits
		self.buf3[0] |= 0x81  # turn on + 1Hz sample rate
		self.buf3[1] &= 0x7c  # turn off heater + boot + one shot
		self.i2c.writeto_mem( HUM_ADDR,0x20+0x80, self.buf3 ) # turn on + set sample rate

		# Get the Humidity sensor  calibration values
		data = i2c.readfrom_mem( HUM_ADDR, 0x30+0x80, 16) # read 16 bytes
		self.H0_rH_x2 = data[0]
		self.H1_rH_x2 = data[1]
		self.T0_degC_x8 = data[2]
		self.T1_degC_x8 = data[3]
		self.T0_degC_x8 |= ((data[5] & 0x3) << 8) # 2 msb bits
		self.T1_degC_x8 |= ((data[5] & 0xc) << 6)
		self.H0_T0_OUT = (data[6] | (data[7]) << 8)
		self.H1_T0_OUT = (data[10] | (data[11]) << 8)
		self.T0_OUT = data[12] | (data[13] << 8)
		self.T1_OUT = data[14] | (data[15] << 8)
		if self.H0_T0_OUT > 32767 :
			self.H0_T0_OUT -= 65536 # signed
		if self.H1_T0_OUT > 32767 :
			self.H1_T0_OUT -= 65536
		if self.T0_OUT > 32767:
			self.T0_OUT -= 65536
		if self.T1_OUT > 32767:
			self.T1_OUT -= 65536

		# prepare pressure sensor
		self.buf1[0] = 0x90 # turn on and set 1Hz update
		self.i2c.writeto_mem( PRESS_ADDR, 0x20, self.buf1 )

		# Init magnetometer
		self.buf4[0] = 0x48 # output data rate/power mode
		self.buf4[1] = 0x00 # default scale
		self.buf4[2] = 0x00 # continuous conversion
		self.buf4[3] = 0x08 # high performance mode
		self.i2c.writeto_mem( MAG_ADDR, 0x20+0x80, self.buf4 )

		# Init accelerometer/gyroscope
		self.buf1[0] = 0x60 # 119hz accel
		self.i2c.writeto_mem( ACC_ADDR, 0x20, self.buf1 )
		self.buf1[0] = 0x38 # enable gyro on all axes
		self.i2c.writeto_mem( ACC_ADDR, 0x1e, self.buf1 )
		self.buf1[0] = 0x28 # data rate + full scale + bw selection
		# bits:        ODR_G2 | ODR_G1 | ODR_G0 | FS_G1 | FS_G0 | 0 | BW_G1 | BW_G0
		# 0x28 = 14.9hz, 500dps
		self.i2c.writeto_mem( ACC_ADDR, 0x10, self.buf1 ) # gyro ctrl_reg1

	def update( self ):
		""" Send the data to the screen """
		# self.i2c.writeto_mem( LED_MATRIX_ADDR, 0, self.buf )
		for y in range(8):
			# send the 8 pixels RED color
			for x in range(8):
				i = (y*24)+x # offset into array
				color = self.pixel(x,y)
				self.buf_leds[i] = (color >> 10) & 0x3e # Red
				self.buf_leds[i+8] = (color >> 5) & 0x3f # Green
				self.buf_leds[i+16] = (color << 1) & 0x3e # Blue
		self.i2c.writeto_mem( LED_MATRIX_ADDR, 0, self.buf_leds )

	def clear( self, update=True ):
		# Just clear the LCD
		self.fill( 0 ) # clear LCD
		if update:
			self.update() # Update the LCD

	def color( self, r,g,b ):
		""" Convert a RGB888 value to RGB565 """
		# Sourced from rgb24_to_rgb16 in https://github.com/mchobby/esp8266-upy/blob/master/COLORS/lib/colortls.py
		return (  ((r >> 3) << 11) | ((g >> 2) << 5) | (b >> 3) )

	def pixels( self, image ):
		""" send a list of pixels (image) to the led matrix """
		for i in range( len(image) ):
			x = i % 8
			y = i // 8
			self.pixel( x,y, image[i] )

	def icon( self, icon, x=1, y=1, color=0x7BEF, clear=True ):
		""" Display one of the icon @ x,y with the C color.
		    Icons are stored into the icons.py file. """
		if clear:
			self.clear( update=False )
		size = icon[0]
		for row in range( size ):
			for col in range( size ):
				if (icon[row+1] & (1<<col)) > 0:
					self.pixel(col+y,row+y,color)


	def scroll( self, s, c=0xFFFF, delay_ms=100 ):
		""" Make a text scrolling on the screen with the c color. delay_ms is the time between 2 successive frames """
		_w = (len(s)+2)*8
		_buf = bytearray( (len(s)+2)*8 ) # 8 columns * 1 byte (8 rows) needed to display a char (each char = 8x8 pixels)
		_fb = FrameBuffer( _buf, _w, 8, MONO_VLSB )
		_fb.text( " %s " % s, 0,0,1 )
		for cols in range( _w-8 ):
			for x in range(8):
				for y in range(8):
					self.pixel( x,y, c if _buf[cols+x] & (0x1 << y) else 0x0 )
			self.update()
			time.sleep_ms( delay_ms )
		del( _fb )
		del( _buf )

	def flip_h( self ):
		for col in range(4):
			for row in range(8):
				c = self.pixel(col,row)
				self.pixel(col,row, self.pixel(7-col,row) )
				self.pixel(7-col,row, c )

	def flip_v( self ):
		for row in range(4):
			for col in range(8):
				c = self.pixel(col,row)
				self.pixel(col,row, self.pixel(col,7-row) )
				self.pixel(col,7-row, c )

	@property
	def joystick( self ):
		""" Read the joystick position. May return None or a JOY_xxxx value """
		self.i2c.readfrom_mem_into( LED_MATRIX_ADDR, 0xF2, self.buf1 )
		if self.buf1[0]==0:
			return None
		else:
			return self.buf1[0]

	@property
	def pressure( self ):
		""" Read the pressure and temperature sensor.

			Returns Pressure in hPa, temp in Celcius """
		self.i2c.readfrom_mem_into( PRESS_ADDR, 0x28+0x80, self.buf5 )
		p = self.buf5[0] + (self.buf5[1]<<8) + (self.buf5[2]<<16)
		t = self.buf5[3] + (self.buf5[4] << 8)
		if t > 32767:
			t -= 65536 # two's compliment
		t = 425 + (t / 48)  # 42.5 + T value/480

		return (p/4096 , t/10) # Press in hPA, Temp in Degree

	@property
	def humidity( self ):
		""" Read the Humidity and temperature sensor.

			Returns Relative_hymidity in percent, temp in Celcius """
		self.i2c.readfrom_mem_into( HUM_ADDR, 0x28+0x80, self.buf4 ) # Only the first 4 bytes are needed.

		self.H_T_out = self.buf4[0] + (self.buf4[1] << 8)
		self.T_out = self.buf4[2] + (self.buf4[3] << 8)
		if self.H_T_out > 32767 :
			self.H_T_out -=65536
		if self.T_out > 32767:
			self.T_out -= 65536
		self.T0_degC = self.T0_degC_x8 / 8
		self.T1_degC = self.T1_degC_x8 / 8
		self.H0_rh = self.H0_rH_x2 / 2
		self.H1_rh = self.H1_rH_x2 / 2
		tmp = (self.H_T_out - self.H0_T0_OUT) * (self.H1_rh - self.H0_rh)*10
		humid = tmp / (self.H1_T0_OUT - self.H0_T0_OUT) + self.H0_rh*10
		tmp = (self.T_out - self.T0_OUT) * (self.T1_degC - self.T0_degC)*10
		temp = tmp / (self.T1_OUT - self.T0_OUT) + self.T0_degC*10

		return (humid/10, temp/10)

	@property
	def mag( self ):
		""" Returns the Magnetic values on the 3 axis """
		self.i2c.readfrom_mem_into( MAG_ADDR, 0x28+0x80, self.buf6 )

		x = self.buf6[0] + (self.buf6[1] << 8)
		y = self.buf6[2] + (self.buf6[3] << 8)
		z = self.buf6[4] + (self.buf6[5] << 8)
		# fix signed values
		if x > 32767 :
			x -= 65536
		if y > 32767 :
			y -= 65536
		if z > 32767 :
			z -= 65536
		return (x,y,z)

	@property
	def gyro( self ):
		""" return the rotation changes in the 3 axis """
		self.i2c.readfrom_mem_into( ACC_ADDR, 0x18+0x80, self.buf6 )
		Gx = self.buf6[0] + (self.buf6[1] << 8);
		Gy = self.buf6[2] + (self.buf6[3] << 8);
		Gz = self.buf6[4] + (self.buf6[5] << 8);
		return (Gx,Gy,Gz)

	@property
	def acc( self ):
		""" return the Accelerometer measurement on x,y,z axis """
		self.i2c.readfrom_mem_into( ACC_ADDR, 0x28+0x80, self.buf6 )

		x = self.buf6[0] + (self.buf6[1] << 8)
		y = self.buf6[2] + (self.buf6[3] << 8)
		z = self.buf6[4] + (self.buf6[5] << 8)
		# fix the signed values
		if x > 32767 :
			x -= 65536
		if y > 32767 :
			y -= 65536
		if z > 32767 :
			z -= 65536

		return (x,y,z)

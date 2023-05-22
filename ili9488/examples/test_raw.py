# Project home: https://github.com/mchobby/esp8266-upy/tree/master/ili9488
#
# Raw portage for Arduino library to decipher communication scheme
#
# Portage of the Arduino code coming from
# http://www.lcdwiki.com/3.5inch_SPI_Module_ILI9488_SKU:MSP3520#How_to_use_on_Arduino
#
from machine import Pin, SPI
from ili9488 import *
from time import sleep_ms


# Raspberry-Pi Pico
#   setBitOrder(MSBFIRST), setDataMode(SPI_MODE0);
# spi = SPI( 1, sck=Pin(10), mosi=Pin(11), miso=Pin(8), polarity=0, phase=0, baudrate=400_000 ) # 40 Mhz
spi = SPI( 1, baudrate=1_000_000 ) # 40 Mhz
cs_pin = Pin(9, Pin.OUT, value=1 )
dc_pin = Pin(12, Pin.OUT )
rst_pin = Pin(13, Pin.OUT, value=1 )

def Lcd_Writ_Bus( d ):
	global spi
	#print( d )
	spi.write( d )

def Lcd_Write_Com( VH ):
	global dc_pin
	dc_pin.value( 0 ) # LCD_RS=0;
	Lcd_Writ_Bus( bytes([VH]) )


def Lcd_Write_Data( VH ):
	global dc_pin
	dc_pin.value( 1 ) # LCD_RS=1;
	Lcd_Writ_Bus( bytes([VH]) )

def Lcd_Write_Com_Data( com, dat):
	Lcd_Write_Com(com)
	Lcd_Write_Data(dat)

def Address_set( x1, y1, x2, y2 ):
	Lcd_Write_Com( 0x2a )
	Lcd_Write_Data(x1>>8)
	Lcd_Write_Data(x1&0xFF)
	Lcd_Write_Data(x2>>8)
	Lcd_Write_Data(x2&0xFF)
	Lcd_Write_Com(0x2b)
	Lcd_Write_Data(y1>>8)
	Lcd_Write_Data(y1&0xFF)
	Lcd_Write_Data(y2>>8)
	Lcd_Write_Data(y2&0xFF)
	Lcd_Write_Com(0x2c)

def Lcd_Init():
	global rst_pin, cs_pin
	rst_pin.value( 1 )
	sleep_ms(5)
	rst_pin.value( 0 )
	sleep_ms(15)
	rst_pin.value( 1 )
	sleep_ms(15)

	cs_pin.value( 0 ) # CS


	Lcd_Write_Com(0xF7) # _PRCTRL = const(0xf7) # Pump Ratio Control
	Lcd_Write_Data(0xA9)
	Lcd_Write_Data(0x51)
	Lcd_Write_Data(0x2C)
	Lcd_Write_Data(0x82)


	Lcd_Write_Com(0xC0) # _PWCTRL1 = const(0xc0) # Power Control 1
	Lcd_Write_Data(0x11)
	Lcd_Write_Data(0x09)


	Lcd_Write_Com(0xC1) # _PWCTRL2 = const(0xc1) # Power Control 2
	Lcd_Write_Data(0x41)


	Lcd_Write_Com(0xC5) # _VMCTRL1 = const(0xc5) # VCOM Control 1
	Lcd_Write_Data(0x00)
	Lcd_Write_Data(0x0A)
	Lcd_Write_Data(0x80)


	Lcd_Write_Com(0xB1) # _FRMCTR1 = const(0xb1) # Frame Rate Control 1
	Lcd_Write_Data(0xB0)
	Lcd_Write_Data(0x11)


	Lcd_Write_Com(0xB4) # _DISINV = const(0xb4) # Display RGB column Inversion control
	Lcd_Write_Data(0x02)

	Lcd_Write_Com(0xB6) # _DISCTRL = const(0xb6) # Display Function Control
	Lcd_Write_Data(0x02)
	Lcd_Write_Data(0x22)

	Lcd_Write_Com(0xB7) # _ENTRYMODE = const(0xb7) # Entry Mode Set
	Lcd_Write_Data(0xC6) # 18 bits RGB encoding


	Lcd_Write_Com(0xBE) # _HSLANE = const(0xBE) # HS Lanes Control
	Lcd_Write_Data(0x00)
	Lcd_Write_Data(0x04)

	Lcd_Write_Com(0xE9) # _IMGSER = const(0xE) # Set Image Function
	Lcd_Write_Data(0x00) # NOT 24bits data bus

	Lcd_Write_Com(0x36) # _MADCTL = const(0x36) # Memory Access Control
	Lcd_Write_Data(0x08) # Value depends on rotation
	# Lcd_Write_Data(0x48) # same rotation as ili9374x
	# Lcd_Write_Data(0xa8)

	Lcd_Write_Com(0x3A) # _PIXSET = const(0x3a) # Pixel Format Set
	Lcd_Write_Data(0x66) # 18 bits/pixel

	Lcd_Write_Com(0x26)  # _GAMSET = const(0x26) # Gamma Set
	Lcd_Write_Data(0x01)

	Lcd_Write_Com(0xE0) # _PGAMCTRL = const(0xe0) # Positive Gamma Control
	Lcd_Write_Data(0x00)
	Lcd_Write_Data(0x07)
	Lcd_Write_Data(0x10)
	Lcd_Write_Data(0x09)
	Lcd_Write_Data(0x17)
	Lcd_Write_Data(0x0B)
	Lcd_Write_Data(0x41)
	Lcd_Write_Data(0x89)
	Lcd_Write_Data(0x4B)
	Lcd_Write_Data(0x0A)
	Lcd_Write_Data(0x0C)
	Lcd_Write_Data(0x0E)
	Lcd_Write_Data(0x18)
	Lcd_Write_Data(0x1B)
	Lcd_Write_Data(0x0F)
	# override with Gamma from ili934x
	Lcd_Write_Com(0xE0) # _PGAMCTRL = const(0xe0) # Positive Gamma Control
	global dc_pin
	dc_pin.value( 1 ) # LCD_RS=1;
	Lcd_Writ_Bus( b"\x0f\x31\x2b\x0c\x0e\x08\x4e\xf1\x37\x07\x10\x03\x0e\x09\x00" )


	Lcd_Write_Com(0xE1) # _NGAMCTRL = const(0xe1) # Negative Gamma Control
	Lcd_Write_Data(0x00)
	Lcd_Write_Data(0x17)
	Lcd_Write_Data(0x1A)
	Lcd_Write_Data(0x04)
	Lcd_Write_Data(0x0E)
	Lcd_Write_Data(0x06)
	Lcd_Write_Data(0x2F)
	Lcd_Write_Data(0x45)
	Lcd_Write_Data(0x43)
	Lcd_Write_Data(0x02)
	Lcd_Write_Data(0x0A)
	Lcd_Write_Data(0x09)
	Lcd_Write_Data(0x32)
	Lcd_Write_Data(0x36)
	Lcd_Write_Data(0x0F)
	# override with Gamma from ili934x
	Lcd_Write_Com(0xE1) # _NGAMCTRL = const(0xe1) # Negative Gamma Control
	global dc_pin
	dc_pin.value( 1 ) # LCD_RS=1;
	Lcd_Writ_Bus( b"\x00\x0e\x14\x03\x11\x07\x31\xc1\x48\x08\x0f\x0c\x31\x36\x0f" )


	Lcd_Write_Com(0x11) # _SLPOUT = const(0x11) # Sleep Out

	sleep_ms(120)


	Lcd_Write_Com(0x29)	# _DISPON = const(0x29) # Display On

	cs_pin.value( 1 )

def H_line( x, y, l, c ):
	global cs_pin
	# unsigned int i,j;
	cs_pin.value( 0 )

	Lcd_Write_Com(0x2c) # write_memory_start
	# //digitalWrite(RS,HIGH);
	l=l+x
	Address_set(x,y,l,y)
	j=l*2
	for i in range( j ): # for(i=1;i<=j;i++)
		Lcd_Write_Data((c>>8) & 0xF8)
		Lcd_Write_Data((c>>3) & 0xFC)
		Lcd_Write_Data((c<<3) & 0xFF)
	cs_pin.value( 1 )

Lcd_Init()
#print( 'init done')
H_line( 10, 10, 30, 165 ) # x, y, len, color

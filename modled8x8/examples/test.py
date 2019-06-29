from machine import Pin, SPI
from modled import ModLedRGB

# Initialize the SPI Bus (on ESP8266-EVB)
# Software SPI
#    spi = SPI(-1, baudrate=4000000, polarity=1, phase=0, sck=Pin(14), mosi=Pin(13), miso=Pin(12))
# Hardware SPI on Pyboard
spi = SPI(2) # MOSI=Y8, MISO=Y7, SCK=Y6, SS=Y5
spi.init( baudrate=2000000, phase=0, polarity=0 ) # low @ 2 MHz
# We must manage the SS signal ourself
ss = Pin( Pin.board.Y5, Pin.OUT )

modled = ModLedRGB( spi, ss ) # Just one LED brick LED-8x8RGB
modled.drawPixel( 1,1, color=1 ) # Red
modled.drawPixel( 2,2, color=2 ) # Green
modled.drawPixel( 3,3, color=4 ) # Blue
modled.drawPixel( 4,8, color=3 ) # Red + Green = Yellow
modled.drawPixel( 5,8, color=5 ) # Red + Blue  = Magenta
modled.drawPixel( 6,7, color=6 ) # Green + Blue  = Cyan
modled.drawPixel( 7,6, color=7 ) # Red + Green + Blue  = White
modled.show()

# Simple demo of the TCS34725 color sensor.
# Will detect the color from the sensor and print it out every second.
import time
from machine import I2C
from tcs34725 import TCS34725

# Pyboard - SDA=Y10, SCL=Y9
i2c = I2C(2)
# ESP8266 sous MicroPython
# i2c = I2C(scl=Pin(5), sda=Pin(4))

sensor = TCS34725(i2c)
#sensor.gain = 16
sensor.integration_time = 200 # Bigger integration time means collect more data about color

def gamma_255( x ):
    """ Apply a gamma correction factor for a value in the range 0 - 255 """
    x /= 255
    x = pow(x, 2.5)
    x *= 255
    return int(x) if x < 255 else 255

def gamma_color( color ):
    """ Apply the Gamma correction to a tuple of rgb color.
        Eyes does not sense the color range in a linear way """
    return gamma_255(color[0]), gamma_255(color[1]), gamma_255(color[2])


# Main loop reading color and printing it every second.
while True:
    # Read the color at the sensor
    rgb = sensor.color_rgb_bytes    # color_rgb_bytes
    gamma_rgb = gamma_color( rgb )  # Apply Gamma
    print( "rgb : %s   gamma_rgb : %s" % (rgb, gamma_rgb) )
	# Delay for a second and repeat.
    time.sleep(1)

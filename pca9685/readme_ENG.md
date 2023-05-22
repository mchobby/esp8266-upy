[Ce fichier existe également en FRANCAIS ici](readme.md)

# Control LEDs and Servo-motors with an autonomous PWM driver / controler

This driver allows you to take control of the Adafruit PWM Driver 16 channels (Adafruit ID 815).

![PCA9685 en breakout](docs/_static/pca9685-pwm-driver.jpg)

The Adafruit Breakout does use the PCA9685 chipset which has a 12 bits resolution.

![PCA9685 en breakout](docs/_static/pwm-driver-usage.jpg)

You can find wiring and sample of using this library on this MC Hobby tutorial

https://wiki.mchobby.be/index.php?title=MicroPython-PWM-DRIVER

# Library

The library must be copied on the MicroPython board before using the examples.

On a WiFi capable plateform:

```
>>> import mip
>>> mip.install("github:mchobby/esp8266-upy/pca9685")
```

Or via the mpremote utility :

```
mpremote mip install github:mchobby/esp8266-upy/pca9685
```

# Wire

# Wire the breakout (Pyboard)

![PCA9685 to Pyboard](docs/_static/pwmdriver-to-pyboard.jpg)

| Pyboard  | PWM-Driver  |  Description |
|----------|-------------|--------------|
|  Y10     |  SDA        | I2C(2).SDA   |
|  Y9      |  SCL        | I2C(2).SCL   |
|  3.3V    |  VCC        | Logic power  |
|  GND     | GND         | Common ground  |

# Test
Copy the needed `pca8685.py` and `servoctrl.py` libraries to your MicroPython board.

The `test.py` file (listed here under) can easily be loaded in the REPL session with `import test`

```
from time import sleep
from machine import I2C
# Import ServoCtrl, the PMW controler for Servo motor
from servoctrl import ServoCtrl

# Initialize the I2C(2) bus on Pyboard Y9,Y10
i2c = I2C( 2 )

# Create the servo motor PWM controler.
# Use the default address 0x40
driver = ServoCtrl( i2c )

# Position of servo #15 to angle of 45 degres
driver.position( 15, 45 )
sleep(2)

# Position of servo  #15 to angle of 180 degres
driver.position( 15, 180 )
sleep(2)

# Position of servo  #15 to angle of 0 degres
driver.position( 15, 0 )
sleep(2)

# Position of servo  #15 to angle of 90 degres
driver.position( 15, 90 )

print( "That s all folks!")

```

# Ressources

## micropython-pca9685
Former work of Radomir Dopieralski around micropython-pca9685

Support for Adafruit Motor Shield and PWM driver using the the PCA9685 chipset

https://bitbucket.org/thesheep/micropython-pca9685/src/c8dec836f7a4?at=default

## Adafruit 16 Channel Servo Driver with Raspberry Pi

https://learn.adafruit.com/adafruit-16-channel-servo-driver-with-raspberry-pi/overview

# Where to buy

The PWM controler is also available at MC Hobby
* PWM-Driver PCA9685 : http://shop.mchobby.be/product.php?id_product=89
* PWM-Driver PCA9685 @ Adafruit :  https://www.adafruit.com/product/815"
* MicroPython Pyboard's :  http://shop.mchobby.be/category.php?id_category=56

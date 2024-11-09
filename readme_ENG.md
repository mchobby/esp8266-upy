[Ce fichier existe également en FRANCAIS](readme.md)

# Plateform Agnostic MicroPython Driver

Initially, this collection of driver + wiring were created for ESP8266 running under MicroPython. The reason for this repository "esp8266-upy" name.

Since, the collection widely evolved and drivers are written to work independently from the target [MicroPython plateform](https://shop.mchobby.be/fr/56-micropython).

![PLateform Agnostic MicroPython Driver](docs/_static/PAM-driver.jpg)

__MIP ready!__ The libraries can be installed with the [MIP Tool](https://docs.micropython.org/en/latest/reference/packages.html) (__MicroPython Install Package__).

# Available libraries
Here is a description of the libraries available in this repository. <strong>Each sub-folders contain README file with additionnal informations about the driver, examples and wiring.</strong>

Explore it by:
* Interface:
[FEATHERWING](docs/indexes/drv_by_intf_FEATHERWING_ENG.md), [GPIO](docs/indexes/drv_by_intf_GPIO_ENG.md), [GROVE](docs/indexes/drv_by_intf_GROVE_ENG.md), [HAT](docs/indexes/drv_by_intf_HAT_ENG.md), [I2C](docs/indexes/drv_by_intf_I2C_ENG.md), [NCD](docs/indexes/drv_by_intf_NCD_ENG.md), [ONEWIRE](docs/indexes/drv_by_intf_ONEWIRE_ENG.md), [QWIIC](docs/indexes/drv_by_intf_QWIIC_ENG.md), [SPI](docs/indexes/drv_by_intf_SPI_ENG.md), [UART](docs/indexes/drv_by_intf_UART_ENG.md), [UEXT](docs/indexes/drv_by_intf_UEXT_ENG.md), [UNO-R3](docs/indexes/drv_by_intf_UNO-R3_ENG.md)
* Manufacturer:
[ADAFRUIT](docs/indexes/drv_by_man_ADAFRUIT_ENG.md), [DFROBOT](docs/indexes/drv_by_man_DFROBOT_ENG.md), [GARATRONIC](docs/indexes/drv_by_man_GARATRONIC_ENG.md), [M5STACK](docs/indexes/drv_by_man_M5STACK_ENG.md), [NCD](docs/indexes/drv_by_man_NCD_ENG.md), [NONE](docs/indexes/drv_by_man_NONE_ENG.md), [OLIMEX](docs/indexes/drv_by_man_OLIMEX_ENG.md), [PIMORONI](docs/indexes/drv_by_man_PIMORONI_ENG.md), [POLOLU](docs/indexes/drv_by_man_POLOLU_ENG.md), [SEEEDSTUDIO](docs/indexes/drv_by_man_SEEEDSTUDIO_ENG.md), [SPARKFUN](docs/indexes/drv_by_man_SPARKFUN_ENG.md)
<table>
<thead>
  <th>Folder</th><th>Description</th>
</thead>
<tbody>
  <tr><td><a href="../../tree/master/74HC595">74HC595</a></td>
      <td><strong>Components</strong> : 74HC595<br />
      <strong>Interfaces</strong> : GPIO<br />
<small>Create a 16 bits address bus with 74HC595.</small><br/><br />
      <strong>Tested with</strong> : PICO<br />
      <strong>Manufacturer</strong> : <br />
<ul>
<li>See <a href="https://shop.mchobby.be/fr/ci/466-74hc595-registre-a-decalage-8-bits-3232100004665.html">74HC595 - Shift Register - Serial to parallel @ MCHobby</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../tree/master/COLORS">COLORS</a></td>
      <td><strong>Components</strong> : <br />
      <strong>Interfaces</strong> : <br />
<small>Color management/tool library</small><br/><br />
      <strong>Tested with</strong> : <br />
      <strong>Manufacturer</strong> : <br />
      </td>
  </tr>
  <tr><td><a href="../../tree/master/FBGFX">FBGFX</a></td>
      <td><strong>Components</strong> : <br />
      <strong>Interfaces</strong> : <br />
<small>Graphical library for FrameBuffer</small><br/><br />
      <strong>Tested with</strong> : <br />
      <strong>Manufacturer</strong> : <br />
      </td>
  </tr>
  <tr><td><a href="../../tree/master/NCD">NCD</a></td>
      <td><strong>Components</strong> : NCD<br />
      <strong>Interfaces</strong> : I2C, NCD<br />
<small>Connect NCD (National Control Device) __I2C mini board__  easily to a MicroPython microcontroler with the <strong>NCD connector</strong>. I2C connexion made easy, 5V logic.</small><br/><br />
      <strong>Tested with</strong> : ESP8266-EVB, FEATHER-ESP8266, WEMOS-D1<br />
      <strong>Manufacturer</strong> : NCD<br />
<ul>
<li>See <a href="https://ncd.io/">NCD.io</a></li>
<li>See <a href="https://ncd.io/">National Control Device</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../tree/master/UEXT">UEXT</a></td>
      <td><strong>Components</strong> : UEXT<br />
      <strong>Interfaces</strong> : I2C, SPI, UART<br />
<small><strong>UEXT</strong> connector work in 3.3V logic and is used on many board and extension of Olimex. It ship I2C, SPI, UART buses as well as 3.3V</small><br/><br />
      <strong>Tested with</strong> : ESP8266-EVB<br />
      <strong>Manufacturer</strong> : OLIMEX<br />
<ul>
<li>See <a href="https://shop.mchobby.be/fr/138-uext">UEXT @ MCHobby</a></li>
<li>See <a href="https://www.olimex.com/Products/Modules/">UEXT @ Olimex</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../tree/master/ad9833">ad9833</a></td>
      <td><strong>Components</strong> : AD9833<br />
      <strong>Interfaces</strong> : SPI<br />
<small>Create a signal generator with the MPR121 chip.</small><br/><br />
      <strong>Tested with</strong> : PYBOARD<br />
      <strong>Manufacturer</strong> : <br />
<ul>
<li>See <a href="https://shop.mchobby.be/fr/breakout/1689-generateur-de-signal-sinus-triangle-clock-0-125-mhz.html">AD9833 - signal generator Sinus, triangle and clock @ MCHobby</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../tree/master/adfmotors">adfmotors</a></td>
      <td><strong>Components</strong> : PCA9685<br />
      <strong>Interfaces</strong> : I2C, UNO-R3<br />
<small>Drive DC motors, steppers or servos with the Adafruit Industries MotorShield.</small><br/><br />
      <strong>Tested with</strong> : PYBOARD, PICO<br />
      <strong>Manufacturer</strong> : ADAFRUIT<br />
<ul>
<li>See <a href="https://shop.mchobby.be/fr/shields/379-shield-de-controle-moteur-motor-shield-v2-3232100003798-adafruit.html">Adafruit Motor Shield @ MCHobby</a></li>
<li>See <a href="https://www.adafruit.com/product/1438">Adafruit Motor Shield @ Adafruit</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../tree/master/ads1015-ads1115">ads1015-ads1115</a></td>
      <td><strong>Components</strong> : ADS1015, ADS1115, ADA1085<br />
      <strong>Interfaces</strong> : I2C<br />
<small>ADC converter (Analog to Digital) 4 channel allowing analog reading and differential reading.<br />L'ADS1115 have a internal amplifier (programmable) that can be used to read very small voltage.</small><br/><br />
      <strong>Tested with</strong> : FEATHER-ESP8266<br />
      <strong>Manufacturer</strong> : ADAFRUIT<br />
<ul>
<li>See <a href="https://shop.mchobby.be/breakout/362-ads1115-convertisseur-adc-16bits-i2c-3232100003620-adafruit.html">ADS1115 breakout</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../tree/master/am2315">am2315</a></td>
      <td><strong>Components</strong> : AM2315<br />
      <strong>Interfaces</strong> : I2C<br />
<small><strong>Temperature & relative humidity</strong> (0 to 100%) sensor for capture outside data.</small><br/><br />
      <strong>Tested with</strong> : FEATHER-ESP8266<br />
      <strong>Manufacturer</strong> : ADAFRUIT<br />
<ul>
<li>See <a href="https://shop.mchobby.be/fr/environnemental-press-temp-hrel-gaz/932-am2315-senseur-de-temperature-et-humidite-sous-boitier-3232100009325.html">AM2315 Sensor</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../tree/master/bme280-bmp280">bme280-bmp280</a></td>
      <td><strong>Components</strong> : BME280, BMP280, ADA2651, ADA2652<br />
      <strong>Interfaces</strong> : I2C<br />
<small>The BMP280 is a very popular <strong>pressure and temperatur</strong> sensor.<br />The BME280 is a sensor for <strong>pressure, temperature and relative HUMIDITY</strong></small><br/><br />
      <strong>Tested with</strong> : FEATHER-ESP8266, PYBOARD, PICO<br />
      <strong>Manufacturer</strong> : ADAFRUIT<br />
<ul>
<li>See <a href="http://shop.mchobby.be/product.php?id_product=1118">Capteur BMP280</a></li>
<li>See <a href="http://shop.mchobby.be/product.php?id_product=684">Capteur BME280</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../tree/master/bmp180">bmp180</a></td>
      <td><strong>Components</strong> : BMP180<br />
      <strong>Interfaces</strong> : I2C<br />
<small>The BMP180 is a <strong>pressure & temperature</strong> sensor now replaced with the BMP280.</small><br/><br />
      <strong>Tested with</strong> : FEATHER-ESP8266<br />
      <strong>Manufacturer</strong> : ADAFRUIT<br />
<ul>
<li>See <a href="http://shop.mchobby.be/product.php?id_product=397">BMP180 Sensor</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../tree/master/cardkb">cardkb</a></td>
      <td><strong>Components</strong> : CARDKB, U035<br />
      <strong>Interfaces</strong> : I2C, GROVE<br />
<small>CardKB - QWERTY mini-keyboard over I2C</small><br/><br />
      <strong>Tested with</strong> : PYBOARD, PYBOARD, M5STACK<br />
      <strong>Manufacturer</strong> : M5STACK<br />
<ul>
<li>See <a href="http://shop.mchobby.be/product.php?id_product=1912">CardKB : Mini Qwerty Keyboard from M5Stack</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../tree/master/ccs811">ccs811</a></td>
      <td><strong>Components</strong> : CCS811<br />
      <strong>Interfaces</strong> : I2C<br />
<small>CCS811 - air quality sensor - COV and eCO2 with MicroPython.</small><br/><br />
      <strong>Tested with</strong> : PYBOARD<br />
      <strong>Manufacturer</strong> : ADAFRUIT, OLIMEX<br />
<ul>
<li>See <a href="https://shop.mchobby.be/product.php?id_product=1274">CCS811 breakout - VOC and eCO2 gaz sensor (ADA3566) @ MCHobby</a></li>
<li>See <a href="https://www.adafruit.com/product/3566">CCS811 breakout - VOC and eCO2 gaz sensor (ADA3566) @ Adafruit</a></li>
<li>See <a href="https://www.adafruit.com/product/1780">MOD-ENV capteur environnemental @ MC Hobby</a></li>
<li>See <a href="https://www.olimex.com/Products/Modules/Sensors/MOD-ENV">MOD-ENV capteur environnemental @ MC Olimex</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../tree/master/dht11">dht11</a></td>
      <td><strong>Components</strong> : DHT11<br />
      <strong>Interfaces</strong> : GPIO<br />
<small>The DHT11 is a very cheap <strong>humidity</strong> (20 to 80%) and temperature sensor.</small><br/><br />
      <strong>Tested with</strong> : FEATHER-ESP8266<br />
      <strong>Manufacturer</strong> : NONE<br />
<ul>
<li>See <a href="http://shop.mchobby.be/product.php?id_product=708">DHT11 Sensor</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../tree/master/dotstar">dotstar</a></td>
      <td><strong>Components</strong> : DOTSTAR, 74AHCT125, APA102<br />
      <strong>Interfaces</strong> : SPI<br />
<small>The <strong>DotStar / APA102</strong> are Smart digitals LED that can be controled individually.</small><br/><br />
      <strong>Tested with</strong> : PYBOARD, PYBSTICK<br />
      <strong>Manufacturer</strong> : ADAFRUIT<br />
<ul>
<li>See <a href="https://shop.mchobby.be/fr/55-neopixels-et-dotstar">APA102 / DotStar</a></li>
<li>See <a href="https://shop.mchobby.be/fr/ci/1041-74ahct125-4x-level-shifter-3v-a-5v-3232100010413.html">74AHCT125</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../tree/master/drv8830">drv8830</a></td>
      <td><strong>Components</strong> : DRV8830, Mini-I2C-Motor-Driver<br />
      <strong>Interfaces</strong> : I2C<br />
<small>The Mini I2C motor driver can be used to control two 5V motors via I2C interface.</small><br/><br />
      <strong>Tested with</strong> : PICO<br />
      <strong>Manufacturer</strong> : SEEEDSTUDIO<br />
<ul>
<li>See <a href="https://www.seeedstudio.com/Grove-I2C-Mini-Motor-Driver.html">Mini I2C Motor Driver (DRV8830)</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../tree/master/ds18b20">ds18b20</a></td>
      <td><strong>Components</strong> : DS18B20<br />
      <strong>Interfaces</strong> : ONEWIRE<br />
<small>The DS18B20 is a very popular <strong>temperature</strong> sensor. It use the 1-Wire bus to connect several sensors.</small><br/><br />
      <strong>Tested with</strong> : FEATHER-ESP8266, PICO, PYBOARD<br />
      <strong>Manufacturer</strong> : NONE<br />
<ul>
<li>See <a href="http://shop.mchobby.be/product.php?id_product=259">DS18B20 Sensor</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../tree/master/eeprom">eeprom</a></td>
      <td><strong>Components</strong> : AT24C512C, AT24C02C, 24LC256<br />
      <strong>Interfaces</strong> : I2C<br />
<small>Using I2C EEPROM to store data.</small><br/><br />
      <strong>Tested with</strong> : PYBOARD, PYBSTICK<br />
      <strong>Manufacturer</strong> : NONE<br />
<ul>
<li>See <a href="http://shop.mchobby.be/product.php?id_product=1582">EEPROM 256 Kbit (32Ko), I2C, 24LC256</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../tree/master/fsr-fma-25N">fsr-fma-25N</a></td>
      <td><strong>Components</strong> : FMAMSDXX005WC2C3, FMAMSDXX015WC2C3, FMAMSDXX025WC2C3<br />
      <strong>Interfaces</strong> : I2C<br />
<small>Using the I2C Force/Dynamometer (FMAMSDXX025WC2C3 from Honeywell).</small><br/><br />
      <strong>Tested with</strong> : PICO<br />
      <strong>Manufacturer</strong> : NONE<br />
<ul>
<li>See <a href="https://automation.honeywell.com/us/en/products/sensing-solutions/sensors/force-sensors/microforce-fma-series">Honeywell Force Sensor - MicroForce FMA Series</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../tree/master/gps-ultimate">gps-ultimate</a></td>
      <td><strong>Components</strong> : GPS-ULTIMATE, MTK3339<br />
      <strong>Interfaces</strong> : UART<br />
<small>Being able to capture (or follow) your position with a GPS module</small><br/><br />
      <strong>Tested with</strong> : PYBOARD<br />
      <strong>Manufacturer</strong> : ADAFRUIT<br />
<ul>
<li>See <a href="https://shop.mchobby.be/fr/breakout/62-gps-adafruit-ultimate-chipset-mtk3339--3232100000629-adafruit.html">GPS Ultime @ MCHobby</a></li>
<li>See <a href="https://www.adafruit.com/product/746">GPS Ultimate</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../tree/master/grav-digital-led">grav-digital-led</a></td>
      <td><strong>Components</strong> : TM1650, DFR0645, VK16K33, DFR646<br />
      <strong>Interfaces</strong> : I2C, GPIO<br />
<small>4x7 or 8x7 Digital LED Segments Display Module via I2C (DFR0645,DFR0646) - under MicroPython.</small><br/><br />
      <strong>Tested with</strong> : PICO<br />
      <strong>Manufacturer</strong> : DFROBOT<br />
<ul>
<li>See <a href="https://shop.mchobby.be/en/leds-leds-displays/2092-4-display-of-7-seg-green-i2c-22-mm-3232100020924-dfrobot.html">Gravity - 4-Digital LED Segment Display Module @ MCHobby</a></li>
<li>See <a href="https://shop.mchobby.be/fr/leds/2584-afficheur-i2c-vert-8-chiffres-de-7-seg-22-mm-3232100025844-dfrobot.html">Gravity - 8-Digital LED Segment Display Module @ MCHobby</a></li>
<li>See <a href="https://www.dfrobot.com/product-1966.html">Gravity - 4-Digital LED Segment Display Module @ DFRobot</a></li>
<li>See <a href="https://www.dfrobot.com/product-1979.html">Gravity - 8-Digital LED Segment Display Module @ DFRobot</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../tree/master/grove-5-way-switch">grove-5-way-switch</a></td>
      <td><strong>Components</strong> : 5-Way-Switch, 6-Position-DIP-Switch<br />
      <strong>Interfaces</strong> : I2C, GROVE<br />
<small>5 dir. joystick (and 6 DIPs board) via I2C - under MicroPython.</small><br/><br />
      <strong>Tested with</strong> : PICO<br />
      <strong>Manufacturer</strong> : SEEEDSTUDIO<br />
<ul>
<li>See <a href="https://www.seeedstudio.com/Grove-5-Way-Switch.html">Grove - 5 Way Switch via I2C @ SeeedStudio</a></li>
<li>See <a href="https://www.seeedstudio.com/Grove-6-Position-DIP-Switch.html">Grove - 6 position DIP switch via I2C @ SeeedStudio</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../tree/master/hat-joy-bonnet">hat-joy-bonnet</a></td>
      <td><strong>Components</strong> : JOY-BONNET<br />
      <strong>Interfaces</strong> : HAT<br />
<small>Use the Joy Bonnet HAT with the MicroPython NADHAT PYB405.</small><br/><br />
      <strong>Tested with</strong> : <br />
      <strong>Manufacturer</strong> : ADAFRUIT<br />
<ul>
<li>See <a href="https://shop.mchobby.be/fr/micropython/1653-hat-micropython-pyb405-nadhat-3232100016538-garatronic.html">NADHAT PYB405 @ MCHobby</a></li>
<li>See <a href="https://shop.mchobby.be/fr/pi-zero-w/1116-gamepad-pizero-joy-bonnet-3232100011168-adafruit.html">Joy Bonnet Gamepad PiZero (ADA3464) @ MCHobby</a></li>
<li>See <a href="https://www.adafruit.com/product/3464">Joy Bonnet Gamepad PiZero (ADA3464) @ Adafruit</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../tree/master/hat-piface">hat-piface</a></td>
      <td><strong>Components</strong> : HAT-PIFACE<br />
      <strong>Interfaces</strong> : HAT<br />
<small>Use the PiFace Digital with the MicroPython Pyboard, PYBStick.</small><br/><br />
      <strong>Tested with</strong> : PYBSTICK, PYBOARD, PICO<br />
      <strong>Manufacturer</strong> : <br />
<ul>
<li>See <a href="https://shop.mchobby.be/fr/pi-hats/221-piface-digital-2-pour-raspberry-pi-3232100002210.html">Hat PiFace Digital 2 @ MCHobby</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../tree/master/hat-sense">hat-sense</a></td>
      <td><strong>Components</strong> : HAT-SENSE<br />
      <strong>Interfaces</strong> : HAT<br />
<small>Use the Sense Hat with the MicroPython Pyboard, PYBStick, PYB405.</small><br/><br />
      <strong>Tested with</strong> : PYBSTICK, PYB405, PYBOARD, PICO<br />
      <strong>Manufacturer</strong> : <br />
<ul>
<li>See <a href="https://shop.mchobby.be/fr/pi-hats/687-sense-hat-pour-raspberry-pi-3232100006874.html">Sense Hat Astro-Pi - le micro laboratoire prêt à l'emploi @ MCHobby</a></li>
<li>See <a href="https://www.raspberrypi.org/products/sense-hat">Hat-sense @ Raspberry-Pi.org</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../tree/master/ht0740-switch">ht0740-switch</a></td>
      <td><strong>Components</strong> : HT0740, TCA9554A<br />
      <strong>Interfaces</strong> : I2C<br />
<small>HT0740 - 40V / 10A MosFet controlable via I2C - under MicroPython.</small><br/><br />
      <strong>Tested with</strong> : PYBOARD, PICO<br />
      <strong>Manufacturer</strong> : PIMORONI<br />
<ul>
<li>See <a href="https://shop.mchobby.be/fr/bouton/1990-40v-10a-mosfet-controlable-via-i2c-3232100019904-pimoroni.html">HT0740 - 40V / 10A MosFet controlable via I2C @ MCHobby</a></li>
<li>See <a href="https://shop.pimoroni.com/products/ht0740-breakout">HT0740 - 40V / 10A MosFet controlable via I2C @ Pimoroni</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../tree/master/huskylens">huskylens</a></td>
      <td><strong>Components</strong> : HuskyLens<br />
      <strong>Interfaces</strong> : I2C, UART<br />
<small>Use a HuskyLens AI Camera with MicroPython</small><br/><br />
      <strong>Tested with</strong> : PICO<br />
      <strong>Manufacturer</strong> : DFROBOT<br />
<ul>
<li>See <a href="https://shop.mchobby.be/fr/imprimantes-et-camera/2421-huskylens-capteur-de-vision-ai-uart-i2c-interface-gravity-3232100024212-dfrobot.html">Huskylens - capteur de vision AI / UART, I2C - interface Gravity @ MCHobby</a></li>
<li>See <a href="https://www.dfrobot.com/product-1922.html">Gravity: Huskylens - An Easy-to-use AI Camera @ DFRobot</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../tree/master/hx711">hx711</a></td>
      <td><strong>Components</strong> : HX711<br />
      <strong>Interfaces</strong> : HAT<br />
<small>Use a HX711 converter with a load cell under MicroPython.</small><br/><br />
      <strong>Tested with</strong> : PICO<br />
      <strong>Manufacturer</strong> : ADAFRUIT<br />
<ul>
<li>See <a href="https://shop.mchobby.be/product.php?id_product=2710">HX711 - convertisseur ADC 24 bits pour cellule de charge / gauge de contrainte @ MCHobby</a></li>
<li>See <a href="https://shop.mchobby.be/product.php?id_product=2712">Cellule de charge 5 Kg, 4 fils @ MCHobby</a></li>
<li>See <a href="https://shop.mchobby.be/product.php?id_product=2711">Cellule de charge 10 Kg, 4 fils @ MCHobby</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../tree/master/ili934x">ili934x</a></td>
      <td><strong>Components</strong> : ILI9341<br />
      <strong>Interfaces</strong> : FEATHERWING, I2C<br />
<small>ILI934x - TFT display controler with 16 bits color - under MicroPython.</small><br/><br />
      <strong>Tested with</strong> : PYBOARD, PYBSTICK, PICO<br />
      <strong>Manufacturer</strong> : ADAFRUIT<br />
<ul>
<li>See <a href="https://shop.mchobby.be/fr/feather-adafruit/1050-tft-featherwing-24-touch-320x240-3232100010505-adafruit.html">TFT FeatherWing 2.4 inch Touch - 320x240 - ILI9341 @ MCHobby</a></li>
<li>See <a href="https://www.adafruit.com/product/3315">TFT FeatherWing 2.4 inch Touch - 320x240 - ILI9341 @ Adafruit</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../tree/master/imu-a">imu-a</a></td>
      <td><strong>Components</strong> : LSM6DS33, LSM6DSOX, LIS3MDL, ADF-4517<br />
      <strong>Interfaces</strong> : I2C<br />
<small>Inertial Measurement Unit 9DOF (acc,magn,gyro) - LSM6DSOX + LIS3MDL - I2C I2C - under MicroPython.</small><br/><br />
      <strong>Tested with</strong> : PICO<br />
      <strong>Manufacturer</strong> : ADAFRUIT<br />
<ul>
<li>See <a href="https://shop.mchobby.be/fr/mouvement/2393-centrale-interielle-9dof-lsm6ds33-lis3mdl-3232100023932-adafruit.html">Centrale Interielle 9DOF - LSM6DSOX + LIS3MDL - Qwiic/StemmaQt - ADF-4517 @ MCHobby</a></li>
<li>See <a href="https://www.adafruit.com/product/4517">9DOF Inertial Measurement Unit - LSM6DSOX + LIS3MDL - Qwiic/StemmaQt - ADF-4517 @ Adafruit</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../tree/master/is31fl">is31fl</a></td>
      <td><strong>Components</strong> : IS31FL3731<br />
      <strong>Interfaces</strong> : FEATHERWING, I2C<br />
<small>IS31FL3731 - CharliePlexing controler via I2C - under MicroPython.</small><br/><br />
      <strong>Tested with</strong> : PYBOARD, PYBSTICK<br />
      <strong>Manufacturer</strong> : ADAFRUIT<br />
<ul>
<li>See <a href="https://shop.mchobby.be/fr/feather-adafruit/1563-featherwing-matrice-led-15x7-en-charlieplexing-pour-feather-3232100015630-adafruit.html">FeatherWing Matrice LED 15x7, ROUGE, CharliePlexing pour Feather @ MCHobby</a></li>
<li>See <a href="https://www.adafruit.com/product/3134">FeatherWing Matrice LED 15x7, ROUGE, CharliePlexing pour Feather @ Adafruit</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../tree/master/lcdi2c">lcdi2c</a></td>
      <td><strong>Components</strong> : I2C BackPack, LCD 16x2, LCD 16x4<br />
      <strong>Interfaces</strong> : I2C<br />
<small>Liquid Crystal display (LCD) controled via I2C bus.</small><br/><br />
      <strong>Tested with</strong> : PYBOARD<br />
      <strong>Manufacturer</strong> : NONE<br />
<ul>
<li>See <a href="https://shop.mchobby.be/fr/afficheur-lcd-tft-oled/882-lcd-20x4-backpack-i2c-blanc-sur-bleu-3232100008823.html">I2C Backpack for LCD display</a></li>
<li>See <a href="https://shop.mchobby.be/fr/afficheur-lcd-tft-oled/881-lcd-20x4-backpack-i2c-blanc-sur-bleu-3232100008816.html">LCD 20x4 + I2C Backpack</a></li>
<li>See <a href="https://shop.mchobby.be/fr/nouveaute/1807-afficheur-lcd-16x2-i2c-3232100018075-dfrobot.html">LCD I2C from DFRobot</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../tree/master/lcdmtrx">lcdmtrx</a></td>
      <td><strong>Components</strong> : USB + Serial Backpack<br />
      <strong>Interfaces</strong> : UART<br />
<small>USB + Serial Backpack Kit with 16x2 RGB backlight positive LCD - Black on RGB.</small><br/><br />
      <strong>Tested with</strong> : PYBOARD<br />
      <strong>Manufacturer</strong> : ADAFRUIT<br />
<ul>
<li>See <a href="https://shop.mchobby.be/fr/afficheur-lcd-tft-oled/475-lcd-16x2-rgb-positif-usb-serie-3232100004757.html">USB + Serial Backpack @ MCHobby</a></li>
<li>See <a href="https://www.adafruit.com/product/782">USB + Serial Backpack @ Adafruit</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../tree/master/lcdspi-lcd12864">lcdspi-lcd12864</a></td>
      <td><strong>Components</strong> : LCD12864<br />
      <strong>Interfaces</strong> : SPI<br />
<small>128 x 64 pixels LCD graphical display. Interface SPI (3 fils)</small><br/><br />
      <strong>Tested with</strong> : PYBOARD, PYBSTICK, PICO<br />
      <strong>Manufacturer</strong> : DFROBOT<br />
<ul>
<li>See <a href="https://shop.mchobby.be/fr/gravity-boson/1878-afficheur-lcd-128x64-spi-3-fils-3232100018785-dfrobot.html">LCD12864 (DFR0091) 128x64 graphical LCD display @ MCHobby</a></li>
<li>See <a href="https://www.dfrobot.com/product-372.html">LCD12864 (DFR0091) 128x64 graphical LCD display @ DFRobot</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../tree/master/lsm303">lsm303</a></td>
      <td><strong>Components</strong> : LSM303D<br />
      <strong>Interfaces</strong> : UNO-R3, I2C<br />
<small>Use a LSM303D compas and accelerometer with MicroPython.</small><br/><br />
      <strong>Tested with</strong> : PYBOARD<br />
      <strong>Manufacturer</strong> : POLOLU<br />
<ul>
<li>See <a href="https://www.pololu.com/product/2127">LSM303D breakout - 3D Compass and Accelerometer @ Pololu</a></li>
<li>See <a href="https://www.pololu.com/product/2510">Robot Zumo pour Arduino (2510) @ Pololu</a></li>
<li>See <a href="https://shop.mchobby.be/fr/prototypage-robotique-roue/448-robot-zumo-pour-arduino-assemble-moteurs-3232100004481-pololu.html">Robot Zumo pour Arduino @ MC Hobby</a></li>
<li>See <a href="https://shop.mchobby.be/fr/nouveaute/1745-adaptateur-pyboard-vers-uno-r3-extra-3232100017450.html">PYBOARD-UNO-R3 - Adaptateur Pyboard vers UNO-R3 + Extra @ MC Hobby</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../tree/master/m5stack-u024">m5stack-u024</a></td>
      <td><strong>Components</strong> : U004, JOYSTICK<br />
      <strong>Interfaces</strong> : GROVE, I2C<br />
<small>I2C Analog Joystick module</small><br/><br />
      <strong>Tested with</strong> : PICO, M5STACK<br />
      <strong>Manufacturer</strong> : M5STACK<br />
<ul>
<li>See <a href="https://shop.mchobby.be/fr/tactile-flex-pot-softpad/2459-m5stack-joystick-grove-i2c-3232100024595-m5stack.html">M5Stack : module joystick analogique en I2C, Grove</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../tree/master/m5stack-u087">m5stack-u087</a></td>
      <td><strong>Components</strong> : U087, ADS1115, VMeter<br />
      <strong>Interfaces</strong> : GROVE, I2C<br />
<small>I2C Voltmeter module</small><br/><br />
      <strong>Tested with</strong> : PICO, M5STACK<br />
      <strong>Manufacturer</strong> : M5STACK<br />
<ul>
<li>See <a href="https://shop.mchobby.be/fr/grove/2153-m5stack-voltmetre-mesure-de-tension-36v-ds1115-grove-3232100021532-m5stack.html">M5Stack : module Voltmètre en I2C, Grove</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../tree/master/m5stack-u088">m5stack-u088</a></td>
      <td><strong>Components</strong> : U088, SGP30<br />
      <strong>Interfaces</strong> : GROVE, I2C<br />
<small>SGP30 I2C Module for TVOC & eCO2 measurement</small><br/><br />
      <strong>Tested with</strong> : PICO, M5STACK<br />
      <strong>Manufacturer</strong> : M5STACK, ADAFRUIT<br />
<ul>
<li>See <a href="https://shop.mchobby.be/fr/grove/2322-m5stack-tvoceco2-gas-sensor-unit-sgp30-gro-3232100023222-m5stack.html">M5Stack : module TVOC, eCO2 en I2C, Grove</a></li>
<li>See <a href="https://shop.mchobby.be/fr/environnemental-press-temp-hrel-gaz/2546-sgp30-capteur-qualite-d-air-voc-eco2-qwiic-stemmaqt-3232100025462-adafruit.html">Adafruit SGP30 module TVOC, eCO2 en I2C</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../tree/master/m5stack-u097">m5stack-u097</a></td>
      <td><strong>Components</strong> : U097, RELAYS<br />
      <strong>Interfaces</strong> : GROVE, I2C<br />
<small>I2C 4 relays module</small><br/><br />
      <strong>Tested with</strong> : PICO, M5STACK<br />
      <strong>Manufacturer</strong> : M5STACK<br />
<ul>
<li>See <a href="https://shop.mchobby.be/fr/nouveaute/2149-m5stack-module-4-relais-i2c-grove-3232100021495.html">M5Stack : module 4 relais en I2C, Grove</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../tree/master/m5stack-u105">m5stack-u105</a></td>
      <td><strong>Components</strong> : U105, AD9833<br />
      <strong>Interfaces</strong> : GROVE, I2C<br />
<small>I2C DDS unit (Direct Digital Synthesis, AD9833, ), Grove</small><br/><br />
      <strong>Tested with</strong> : PICO, M5STACK<br />
      <strong>Manufacturer</strong> : M5STACK<br />
<ul>
<li>See <a href="https://shop.mchobby.be/fr/nouveaute/2151-m5stack-generateur-de-signal-dds-stm32f0-ad9833-grove-3232100021518.html">M5Stack : DDS unit (AD9833) with STM32F0 I2C custom firmware, Grove</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../tree/master/m5stack-u135">m5stack-u135</a></td>
      <td><strong>Components</strong> : U135, ENCODER<br />
      <strong>Interfaces</strong> : GROVE, I2C<br />
<small>I2C Encoder unit, Grove</small><br/><br />
      <strong>Tested with</strong> : PICO, M5STACK<br />
      <strong>Manufacturer</strong> : M5STACK<br />
<ul>
<li>See <a href="https://shop.mchobby.be/fr/grove/2456-m5stack-encodeur-led-rgb-grove-3232100024564-m5stack.html">M5Stack : I2C Encoder unit with custom firmware, Grove @ MCHobby</a></li>
<li>See <a href="https://shop.m5stack.com/products/encoder-unit">M5Stack : I2C Encoder unit with custom firmware, Grove @ M5Stack</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../tree/master/m5stack-u136">m5stack-u136</a></td>
      <td><strong>Components</strong> : U136, BH1750FVI-TR<br />
      <strong>Interfaces</strong> : GROVE, I2C<br />
<small>I2C DLight unit - Ambiant Light (Lux) sensor, Grove</small><br/><br />
      <strong>Tested with</strong> : PICO<br />
      <strong>Manufacturer</strong> : M5STACK<br />
<ul>
<li>See <a href="https://shop.mchobby.be/fr/grove/2444-m5stack-capteur-luminosite-ambiante-bh1750fvi-tr-grove-i2c-3232100024441-m5stack.html">M5Stack : I2C Capteur luminosité ambiante DLight, Grove @ MCHobby</a></li>
<li>See <a href="https://shop.m5stack.com/products/dlight-unit-ambient-light-sensor-bh1750fvi-tr">M5Stack : Dlight Unit - Ambient Light Sensor , Grove @ M5Stack</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../tree/master/max31855">max31855</a></td>
      <td><strong>Components</strong> : MAX31855<br />
      <strong>Interfaces</strong> : SPI<br />
<small>Type-K thermocouple + MAX31855 amplifier - under MicroPython.</small><br/><br />
      <strong>Tested with</strong> : PICO<br />
      <strong>Manufacturer</strong> : ADAFRUIT<br />
<ul>
<li>See <a href="https://shop.mchobby.be/fr/temperature/301-thermocouple-type-k-3232100003019.html">MAX31855 - Amplificateur Thermocouple Type-K via SPI d'Adafruit @ MCHobby</a></li>
<li>See <a href="https://www.adafruit.com/product/269">AX31855 - Amplificateur Thermocouple Type-K via SPI d'Adafruit @ Adafruit</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../tree/master/max6675">max6675</a></td>
      <td><strong>Components</strong> : MOD-TC, MAX6675<br />
      <strong>Interfaces</strong> : UEXT, SPI<br />
<small>MAX6675 Type-K Thermocouple amplifier - MOD-TC - under MicroPython.</small><br/><br />
      <strong>Tested with</strong> : PYBOARD<br />
      <strong>Manufacturer</strong> : OLIMEX<br />
<ul>
<li>See <a href="https://shop.mchobby.be/product.php?id_product=1623">MOD-TC - Amplificateur Thermocouple Type-K d'Olimex @ MCHobby</a></li>
<li>See <a href="https://www.olimex.com/Products/Modules/Sensors/MOD-TC">MOD-TC - Amplificateur Thermocouple Type-K @ Olimex</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../tree/master/mcp230xx">mcp230xx</a></td>
      <td><strong>Components</strong> : MCP23017, MCP23008<br />
      <strong>Interfaces</strong> : I2C<br />
<small>The MCP23017 (and MCP2308) are <strong>GPIO Expander</strong> on I2C bis adding input/output to a microcontroler.</small><br/><br />
      <strong>Tested with</strong> : FEATHER-ESP8266<br />
      <strong>Manufacturer</strong> : NONE<br />
<ul>
<li>See <a href="http://shop.mchobby.be/product.php?id_product=218">MCP23017 GPIO Expander</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../tree/master/mcp23Sxx">mcp23Sxx</a></td>
      <td><strong>Components</strong> : MCP23S17<br />
      <strong>Interfaces</strong> : SPI<br />
<small>The MCP23S17 is a <strong>GPIO Expander</strong> on SPI bus adding input/output to a microcontroler.</small><br/><br />
      <strong>Tested with</strong> : PYBOARD, PYBSTICK<br />
      <strong>Manufacturer</strong> : NONE<br />
      </td>
  </tr>
  <tr><td><a href="../../tree/master/mcp4725">mcp4725</a></td>
      <td><strong>Components</strong> : MCP4725<br />
      <strong>Interfaces</strong> : I2C<br />
<small>The MCP4725 (I2C bus) is a DAC -or- a TRUE 12 bits analog output (0 à 65535).</small><br/><br />
      <strong>Tested with</strong> : FEATHER-ESP8266, PYBOARD<br />
      <strong>Manufacturer</strong> : ADAFRUIT<br />
<ul>
<li>See <a href="http://shop.mchobby.be/product.php?id_product=132">MCP4725 12 bits DAC @ MCHobby : Convertisseur Digital/Analogique pour MicroControlleur, interface I2C</a></li>
<li>See <a href="https://www.adafruit.com/product/935">MCP4725 12 bits DAC @ Adafruit : 12 bits DAC over I2C bus</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../tree/master/mcp9808">mcp9808</a></td>
      <td><strong>Components</strong> : MCP9808<br />
      <strong>Interfaces</strong> : I2C<br />
<small>The MCP9808 (I2C bus) can measure temperature with high accuracy (0.25°C).</small><br/><br />
      <strong>Tested with</strong> : FEATHER-ESP8266, PYBOARD<br />
      <strong>Manufacturer</strong> : ADAFRUIT<br />
<ul>
<li>See <a href="http://shop.mchobby.be/product.php?id_product=572">MCP9808 @ MCHobby : mesure de température de précision via I2C</a></li>
<li>See <a href="https://www.adafruit.com/product/1782">MCP9808 @ Adafruit : High precision temperature sensor</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../tree/master/modenv">modenv</a></td>
      <td><strong>Components</strong> : CCS811, BME280<br />
      <strong>Interfaces</strong> : UEXT, I2C<br />
<small>Environmental sensor all-in-one - BME280 + CCS811 - under MicroPython.</small><br/><br />
      <strong>Tested with</strong> : PYBOARD<br />
      <strong>Manufacturer</strong> : OLIMEX<br />
<ul>
<li>See <a href="https://shop.mchobby.be/product.php?id_product=1280">MOD-ENV - Capteur environnemental d'Olimex CCS811 + BME280 @ MCHobby</a></li>
<li>See <a href="https://www.olimex.com/Products/Modules/Sensors/MOD-ENV">MOD-ENV capteur environnemental @ Olimex</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../tree/master/modio">modio</a></td>
      <td><strong>Components</strong> : MOD-IO<br />
      <strong>Interfaces</strong> : I2C, UEXT<br />
<small>MOD-IO is an I2C extension board with <strong>UEXT</strong> connector. This Olimex's Board have relays, OptoCoupler input (24V) and analog input (0-3.3V).<br />This board is compatible with the industrial grade voltages (24V).</small><br/><br />
      <strong>Tested with</strong> : ESP8266-EVB<br />
      <strong>Manufacturer</strong> : OLIMEX<br />
<ul>
<li>See <a href="https://shop.mchobby.be/fr/138-uext">UEXT @ MCHobby</a></li>
<li>See <a href="https://www.olimex.com/Products/Modules/">UEXT @ Olimex</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../tree/master/modio2">modio2</a></td>
      <td><strong>Components</strong> : MOD-IO2<br />
      <strong>Interfaces</strong> : I2C, UEXT<br />
<small>MOD-IO is an I2C extension board with <strong>UEXT</strong> connector. This Olimex's Board have relays, and GPIOs with various functions (Input, Output, Analog, PWM; 0-3.3V).</small><br/><br />
      <strong>Tested with</strong> : ESP8266-EVB<br />
      <strong>Manufacturer</strong> : OLIMEX<br />
<ul>
<li>See <a href="https://shop.mchobby.be/fr/138-uext">UEXT @ MCHobby</a></li>
<li>See <a href="https://www.olimex.com/Products/Modules/">UEXT @ Olimex</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../tree/master/modirdaplus">modirdaplus</a></td>
      <td><strong>Components</strong> : MOD-IRDA+<br />
      <strong>Interfaces</strong> : I2C, UEXT<br />
<small>MOD-IRDA+ is an I2C Infrared emitter/receiver module supporting the RC5 (Philips) and SIRCS (Sony) protocols.</small><br/><br />
      <strong>Tested with</strong> : PICO, PYBOARD<br />
      <strong>Manufacturer</strong> : OLIMEX<br />
<ul>
<li>See <a href="https://shop.mchobby.be/fr/138-uext">UEXT @ MCHobby</a></li>
<li>See <a href="https://www.olimex.com/Products/Modules/">UEXT @ Olimex</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../tree/master/modirtemp">modirtemp</a></td>
      <td><strong>Components</strong> : MOD-IR-TEMP, MLX90614<br />
      <strong>Interfaces</strong> : I2C, UEXT<br />
<small>NON-Contact IR temperature sensor, from -70°C to 380°C with MXL90164.</small><br/><br />
      <strong>Tested with</strong> : FEATHER-ESP8266, PYBOARD<br />
      <strong>Manufacturer</strong> : OLIMEX<br />
<ul>
<li>See <a href="https://www.olimex.com/Products/Modules/Sensors/MOD-IR-TEMP/open-source-hardware">MOD-IR-TEMP @ Olimex</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../tree/master/modlcd1x9">modlcd1x9</a></td>
      <td><strong>Components</strong> : MOD-LCD-1x9<br />
      <strong>Interfaces</strong> : I2C, UEXT<br />
<small>MOD-LCD1x9 is an I2C'based 9 characters alphanumeric display using the <strong>UEXT</strong> connector.</small><br/><br />
      <strong>Tested with</strong> : ESP8266-EVB, PYBOARD<br />
      <strong>Manufacturer</strong> : OLIMEX<br />
<ul>
<li>See <a href="https://shop.mchobby.be/esp8266-esp32-wifi-iot/1414-uext-lcd-display-1-line-of-9-alphanumeric-chars-3232100014145-olimex.html">MOD-LCD1x9 @ MCHobby</a></li>
<li>See <a href="https://www.olimex.com/Products/Modules/">UEXT @ Olimex</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../tree/master/modlcd3310">modlcd3310</a></td>
      <td><strong>Components</strong> : MOD-LCD3310, PCD8544<br />
      <strong>Interfaces</strong> : SPI, UEXT<br />
<small>MOD-LCD3310 is the Nokia 3310 LCD display offering 84 x 48 pixels and an <strong>UEXT</strong> connector.</small><br/><br />
      <strong>Tested with</strong> : PYBOARD<br />
      <strong>Manufacturer</strong> : OLIMEX<br />
<ul>
<li>See <a href="https://shop.mchobby.be/fr/uext/1867-afficheur-noirblanc-84x48-px-nokia-3310-3232100018679-olimex.html">MOD-LCD3310 @ MCHobby</a></li>
<li>See <a href="https://www.olimex.com/Products/Modules/LCD/MOD-LCD3310/open-source-hardware">MOD-LCD3310 @ Olimex</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../tree/master/modled8x8">modled8x8</a></td>
      <td><strong>Components</strong> : MOD-LED8x8RGB<br />
      <strong>Interfaces</strong> : GPIO, SPI<br />
<small>A 8x8 RGB led display that can be daisy chained.</small><br/><br />
      <strong>Tested with</strong> : PYBOARD<br />
      <strong>Manufacturer</strong> : OLIMEX<br />
<ul>
<li>See <a href="https://shop.mchobby.be/fr/nouveaute/1625-mod-led8x8rgb-matrice-led-rgb-8x8-3232100016255-olimex.html">MOD-LED8x8RGB @ MCHobby</a></li>
<li>See <a href="https://www.olimex.com/Products/Modules/LED/MOD-LED8x8RGB/open-source-hardware">MOD-LED8x8RGB @ Olimex</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../tree/master/modltr501">modltr501</a></td>
      <td><strong>Components</strong> : MOD-LTR-501ALS, LTR-501ALS<br />
      <strong>Interfaces</strong> : I2C, UEXT<br />
<small>LTR-501ALS can be used to acquires luminosity data from 0.01 to 64.000 Lux (64K lux) and make proximity detection (up to 10cm). The MOD-MAG have an <strong>UEXT</strong> connector to ease wiring.</small><br/><br />
      <strong>Tested with</strong> : ESP8266-EVB<br />
      <strong>Manufacturer</strong> : OLIMEX<br />
<ul>
<li>See <a href="https://shop.mchobby.be/uext/1415-senseur-proximite-et-lumiere-ltr501-connecteur-uext-3232100014152-olimex.html">MOD-LTR-501ALS @ MCHobby</a></li>
<li>See <a href="https://www.olimex.com/Products/Modules/">UEXT @ Olimex</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../tree/master/modmag">modmag</a></td>
      <td><strong>Components</strong> : MOD-MAG, MAG3110<br />
      <strong>Interfaces</strong> : I2C, UEXT<br />
<small>The MAG3110 is a digital 3 axis magnetometer from NXP running over an I2C bus. The MOD-MAG have an <strong>UEXT</strong> connector to ease wiring.</small><br/><br />
      <strong>Tested with</strong> : ESP8266-EVB<br />
      <strong>Manufacturer</strong> : OLIMEX<br />
<ul>
<li>See <a href="https://shop.mchobby.be/esp8266-esp32-wifi-iot/1413-uext-mag3110-magnetometer-module-3232100014138-olimex.html">MOD-MAG @ MCHobby</a></li>
<li>See <a href="https://www.olimex.com/Products/Modules/">UEXT @ Olimex</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../tree/master/modoled128x64">modoled128x64</a></td>
      <td><strong>Components</strong> : SSD1306, MOD-OLED-128x64, OLED, OLED-FEATHERWING, MINI-OLED<br />
      <strong>Interfaces</strong> : I2C, UEXT<br />
<small>A 128x64 / 128x32 / 64x48 OLED display with the SSD1306 I2C controler exposing a UEXT, Feather, Qwiic connector.</small><br/><br />
      <strong>Tested with</strong> : ESP8266-EVB, PICO, MICROMOD-RP2040<br />
      <strong>Manufacturer</strong> : OLIMEX, ADAFRUIT, SPARKFUN<br />
<ul>
<li>See <a href="https://shop.mchobby.be/product.php?id_product=1411">Afficheur OLED 128 x 64 avec interface I2C et UEXT</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../tree/master/modrfid">modrfid</a></td>
      <td><strong>Components</strong> : MOD-RFID1536MIFARE<br />
      <strong>Interfaces</strong> : UART, UEXT<br />
<small>NFC RFID reader writer for 13.56Mhz NFC MIFARE RFID tags.</small><br/><br />
      <strong>Tested with</strong> : PYBOARD<br />
      <strong>Manufacturer</strong> : OLIMEX<br />
<ul>
<li>See <a href="https://shop.mchobby.be/product.php?id_product=1619">MOD-RFID1536MIFARE @ MCHobby</a></li>
<li>See <a href="https://www.olimex.com/Products/Modules/RFID/MOD-RFID1356MIFARE/">MOD-RFID1536MIFARE @ Olimex</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../tree/master/modrgb">modrgb</a></td>
      <td><strong>Components</strong> : MOD-RGB<br />
      <strong>Interfaces</strong> : I2C, UEXT<br />
<small>MOD-RGB is an I2C extension board with <strong>UEXT</strong> connector. This Olimex's Board have power MosFet to control RGB analogic LED strips via I2C (or DMX).</small><br/><br />
      <strong>Tested with</strong> : ESP8266-EVB<br />
      <strong>Manufacturer</strong> : OLIMEX<br />
<ul>
<li>See <a href="https://shop.mchobby.be/fr/138-uext">UEXT @ MCHobby</a></li>
<li>See <a href="https://www.olimex.com/Products/Modules/">UEXT @ Olimex</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../tree/master/modrs485iso">modrs485iso</a></td>
      <td><strong>Components</strong> : MOD-RS485-ISO<br />
      <strong>Interfaces</strong> : I2C, UART, UEXT<br />
<small>MOD-RS485-ISO is an Full-Duplex/Half-Duplex RS485 adapter with isolation circuitery. Data transmission is made via UART (MODE_PASS) or I2C (MODE_BRIDE). It expose an <strong>UEXT</strong> connector for quick wiring.</small><br/><br />
      <strong>Tested with</strong> : PYBOARD<br />
      <strong>Manufacturer</strong> : OLIMEX<br />
<ul>
<li>See <a href="https://shop.mchobby.be/fr/138-uext">UEXT @ MCHobby</a></li>
<li>See <a href="https://www.olimex.com/Products/Modules/">UEXT @ Olimex</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../tree/master/modtc-mk2">modtc-mk2</a></td>
      <td><strong>Components</strong> : MOD-TC-MK2-31855<br />
      <strong>Interfaces</strong> : UEXT, I2C<br />
<small>MAX6MOD-TC-MK2 : Type-K Thermocouple amplifier (MAX31855) over I2C - under MicroPython.</small><br/><br />
      <strong>Tested with</strong> : PYBOARD<br />
      <strong>Manufacturer</strong> : OLIMEX<br />
<ul>
<li>See <a href="https://shop.mchobby.be/fr/uext/1624-mod-tc-mk2-31855-interface-thermocouple-type-k-avec-max31855-bus-i2c-gpio-3232100016248-olimex.html">MOD-TC-MK2 - Amplificateur Thermocouple Type-K (MAX31855) via I2C d'Olimex @ MCHobby</a></li>
<li>See <a href="https://www.olimex.com/Products/Modules/Sensors/MOD-TC-MK2-31855/open-source-hardware">MOD-TC-MK2 - Type-K Thermocouple Amplifier (MAX31855) over I2C from Olimex @ Olimex</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../tree/master/modwii">modwii</a></td>
      <td><strong>Components</strong> : MOD-Wii-UEXT-NUNCHUCK, NUNCHUCK<br />
      <strong>Interfaces</strong> : I2C, UEXT<br />
<small>The Wii NUNCHUCK is a game controler very comfortable to used and runs over the I2C bus. This controler have an <strong>UEXT</strong> connector to ease wiring.</small><br/><br />
      <strong>Tested with</strong> : ESP8266-EVB<br />
      <strong>Manufacturer</strong> : OLIMEX<br />
<ul>
<li>See <a href="https://shop.mchobby.be/esp8266-esp32-wifi-iot/1416-uext-wii-nunchuck-controller-3232100014169-olimex.html">Wii Nunchuck game controller (UEXT) @ MCHobby</a></li>
<li>See <a href="https://www.olimex.com/Products/Modules/">UEXT @ Olimex</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../tree/master/mpr121">mpr121</a></td>
      <td><strong>Components</strong> : MPR121<br />
      <strong>Interfaces</strong> : I2C<br />
<small>Create tactile pad/inputs with capacitive effect with the MPR121 chip.</small><br/><br />
      <strong>Tested with</strong> : PYBOARD, FEATHER-ESP8266<br />
      <strong>Manufacturer</strong> : ADAFRUIT<br />
<ul>
<li>See <a href="https://shop.mchobby.be/fr/tactile-flex-pot-softpad/1685-capteur-capacitif-12-touches-mpr121-3232100016859-adafruit.html">MPR121 - capteur capacitif 12 entrées/touches @ MCHobby</a></li>
<li>See <a href="https://www.adafruit.com/product/1982">12-Key Capacitive Touch Sensor Breakout - MPR121 @ Adafruit</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../tree/master/mpx5700a">mpx5700a</a></td>
      <td><strong>Components</strong> : MPX5700AP<br />
      <strong>Interfaces</strong> : GROVE<br />
<small>Using a MPX5700AP ANALOG pressure sensor.</small><br/><br />
      <strong>Tested with</strong> : PICO, PYBSTICK<br />
      <strong>Manufacturer</strong> : SEEEDSTUDIO<br />
<ul>
<li>See <a href="https://www.seeedstudio.com/Grove-Integrated-Pressure-Sensor-Kit-MPX5700AP-p-4295.html">Capteur ANALOGIQUE de pression 15 kPa à 480 kPa sous 3.3V (700 kPa) @ SeeedStudio</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../tree/master/ncd-fet-solenoid">ncd-fet-solenoid</a></td>
      <td><strong>Components</strong> : I2CDRV8W4I12V, MCP23008<br />
      <strong>Interfaces</strong> : I2C, NCD<br />
<small>FET Output controler + GPIO (based on a MCP23008) for 12V resistive / inductive load (like valve). The <i>I2C NCD board</i> have the <strong>NCD</strong> connector which facilitate the device wiring.<br />The MPL115A2 is also available as breakout.</small><br/><br />
      <strong>Tested with</strong> : FEATHER-ESP8266, PYBOARD<br />
      <strong>Manufacturer</strong> : NCD<br />
<ul>
<li>See <a href="https://ncd.io/">NCD.io</a></li>
<li>See <a href="https://ncd.io/">National Control Device</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../tree/master/ncd-mpl115a2">ncd-mpl115a2</a></td>
      <td><strong>Components</strong> : MPL115A2, ADA992<br />
      <strong>Interfaces</strong> : I2C, NCD<br />
<small>The MPL115A2 sensor capture the pressure and temperature over I2C bus. The <i>I2C NCD mini board</i> have the <strong>NCD</strong> connector which facilitate the device wiring.<br />The MPL115A2 is also available as breakout.</small><br/><br />
      <strong>Tested with</strong> : FEATHER-ESP8266, PYBOARD<br />
      <strong>Manufacturer</strong> : NCD, ADAFRUIT<br />
<ul>
<li>See <a href="https://ncd.io/">NCD.io</a></li>
<li>See <a href="https://ncd.io/">National Control Device</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../tree/master/ncd-oled">ncd-oled</a></td>
      <td><strong>Components</strong> : SSD1306, I2COLED, OLED<br />
      <strong>Interfaces</strong> : I2C, NCD<br />
<small>A 128x64 display with the SSD1306 I2C controler exposing a NCD connector.</small><br/><br />
      <strong>Tested with</strong> : FEATHER-ESP8266, PYBOARD<br />
      <strong>Manufacturer</strong> : NCD<br />
<ul>
<li>See <a href="https://ncd.io/">NCD.io - National Control Device</a></li>
<li>See <a href="https://store.ncd.io/product/oled-128x64-graphic-display-i2c-mini-module/">NCD oled 128x64 i2c mini module</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../tree/master/ncd-pecmac">ncd-pecmac</a></td>
      <td><strong>Components</strong> : DLCT27C10, OPCT16AL, I2CCMAC230A, PECMAC2xxxA<br />
      <strong>Interfaces</strong> : I2C, NCD<br />
<small>AC Current sensor on I2C bus (or IoT interface). The <i>I2C NCD board</i> have the <strong>NCD</strong> connector which facilitate the device wiring.<br />The MPL115A2 is also available as breakout.</small><br/><br />
      <strong>Tested with</strong> : FEATHER-ESP8266, PYBOARD<br />
      <strong>Manufacturer</strong> : NCD<br />
<ul>
<li>See <a href="https://ncd.io/">NCD.io</a></li>
<li>See <a href="https://ncd.io/">National Control Device</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../tree/master/ncd-si7005">ncd-si7005</a></td>
      <td><strong>Components</strong> : SI7005<br />
      <strong>Interfaces</strong> : I2C, NCD<br />
<small>The SI7005 is a pressure and temperature sensor working over the I2C bus. The <i>I2C NCD mini board</i> have the <strong>NCD</strong> connector which facilitate the device wiring.<br />The MPL115A2 is also available as breakout.</small><br/><br />
      <strong>Tested with</strong> : FEATHER-ESP8266, PYBOARD<br />
      <strong>Manufacturer</strong> : NCD<br />
<ul>
<li>See <a href="https://ncd.io/">NCD.io</a></li>
<li>See <a href="https://ncd.io/">National Control Device</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../tree/master/ncd-water-detect">ncd-water-detect</a></td>
      <td><strong>Components</strong> : WATER-DETECT, WDBZ, PCA9536<br />
      <strong>Interfaces</strong> : I2C, NCD<br />
<small>Water detection + Buzzer + 2 extra GPIOs (based on a PCA9536). The <i>I2C NCD mini board</i> have the <strong>NCD</strong> connector which facilitate the device wiring.<br />The MPL115A2 is also available as breakout.</small><br/><br />
      <strong>Tested with</strong> : FEATHER-ESP8266, PYBOARD<br />
      <strong>Manufacturer</strong> : NCD<br />
<ul>
<li>See <a href="https://ncd.io/">NCD.io</a></li>
<li>See <a href="https://ncd.io/">National Control Device</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../tree/master/neopixel">neopixel</a></td>
      <td><strong>Components</strong> : NEOPIXEL, 74AHCT125, WS2812<br />
      <strong>Interfaces</strong> : GPIO<br />
<small>The <strong>NéoPixels</strong> are Smart digitals LED that can be controled individually.</small><br/><br />
      <strong>Tested with</strong> : FEATHER-ESP8266, PYBOARD<br />
      <strong>Manufacturer</strong> : ADAFRUIT<br />
<ul>
<li>See <a href="https://shop.mchobby.be/fr/55-neopixels-et-dotstar">NeoPixels</a></li>
<li>See <a href="https://shop.mchobby.be/fr/ci/1041-74ahct125-4x-level-shifter-3v-a-5v-3232100010413.html">74AHCT125</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../tree/master/oled-ssd1306">oled-ssd1306</a></td>
      <td><strong>Components</strong> : SSD1306, FEATHER-OLED-WING, ADA2900, OLED<br />
      <strong>Interfaces</strong> : I2C, FEATHERWING, QWIIC<br />
<small>The SSD1306 is an OLED display controler.</small><br/><br />
      <strong>Tested with</strong> : FEATHER-ESP8266<br />
      <strong>Manufacturer</strong> : ADAFRUIT<br />
<ul>
<li>See <a href="https://shop.mchobby.be/product.php?id_product=879">FeatherWing OLED ssd1306 128x32</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../tree/master/opt3101-fov">opt3101-fov</a></td>
      <td><strong>Components</strong> : OPT3101, POL3412<br />
      <strong>Interfaces</strong> : I2C<br />
<small>3-Channel Wide FOV Time-of-Flight Distance Sensor OPT310 (POL3412)</small><br/><br />
      <strong>Tested with</strong> : PICO, PYBSTICK<br />
      <strong>Manufacturer</strong> : POLOLU<br />
<ul>
<li>See <a href="https://shop.mchobby.be/product.php?id_product=2289">Capteur Time-Of-Flight FoV 3 canaux OPT3101 (POL3412)</a></li>
<li>See <a href="https://www.pololu.com/product/3412">3-Channel Wide FOV Time-of-Flight Distance Sensor Using OPT310 (POL3412)</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../tree/master/pca9536">pca9536</a></td>
      <td><strong>Components</strong> : PCA9536<br />
      <strong>Interfaces</strong> : I2C<br />
<small>4 bit I2C controled GPIO expander.</small><br/><br />
      <strong>Tested with</strong> : <br />
      <strong>Manufacturer</strong> : NONE<br />
      </td>
  </tr>
  <tr><td><a href="../../tree/master/pca9685">pca9685</a></td>
      <td><strong>Components</strong> : PCA9685, PWM-Driver<br />
      <strong>Interfaces</strong> : I2C<br />
<small>PWM-Driver driver contrôler based on PCA9685 from NXP, 16 channel, 12 bits resolution, to drive LEDs and Servos.</small><br/><br />
      <strong>Tested with</strong> : PYBOARD<br />
      <strong>Manufacturer</strong> : ADAFRUIT<br />
<ul>
<li>See <a href="https://shop.mchobby.be/fr/breakout/89-adafruit-controleur-pwm-servo-16-canaux-12-bits-i2c-interface-pca9685-3232100000896-adafruit.html">PCA9685 - PWM Driver @ MCHobby</a></li>
<li>See <a href="https://www.adafruit.com/product/815">PCA9685 - PWM Driver @ Adafruit</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../tree/master/pcf8523">pcf8523</a></td>
      <td><strong>Components</strong> : PCF8523<br />
      <strong>Interfaces</strong> : I2C<br />
<small>A real time clock RTC + alarm for MicroPython</small><br/><br />
      <strong>Tested with</strong> : PYBSTICK, PICO<br />
      <strong>Manufacturer</strong> : ADAFRUIT<br />
<ul>
<li>See <a href="https://shop.mchobby.be/fr/pi-extensions/1148-pirtc-pcf8523-real-time-clock-for-raspberry-pi-3232100011489-adafruit.html">PiRTC (PCF8523) @ MCHobby</a></li>
<li>See <a href="https://shop.mchobby.be/fr/feather-adafruit/1056-adalogger-featherwing-rtc-pcf8523-microsd-3232100010567-adafruit.html">Adafruit AdaLogger FeatherWing (PCF8523) @ MCHobby</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../tree/master/pm25">pm25</a></td>
      <td><strong>Components</strong> : MP2.5, PMS5003<br />
      <strong>Interfaces</strong> : UART<br />
<small>Using a PM2.5 particle sensor (PMS5003) with MicroPython</small><br/><br />
      <strong>Tested with</strong> : PICO<br />
      <strong>Manufacturer</strong> : ADAFRUIT, PIMORONI<br />
<ul>
<li>See <a href="https://shop.mchobby.be/product.php?id_product=1332">PM2.5 Particle Sensor (PMS5003) @ MCHobby</a></li>
<li>See <a href="https://www.adafruit.com/product/3686">PM2.5 Air Quality Sensor (PMS5003) @ Adafruit</a></li>
<li>See <a href="(https://shop.pimoroni.com/products/pms5003-particulate-matter-sensor-with-cable">PMS5003 Particulate Matter Sensor @ Pimoroni</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../tree/master/pn532-rfid">pn532-rfid</a></td>
      <td><strong>Components</strong> : pn532<br />
      <strong>Interfaces</strong> : UART<br />
<small>Use a PN532 RFID/NFC controler with MicroPython</small><br/><br />
      <strong>Tested with</strong> : PICO<br />
      <strong>Manufacturer</strong> : ADAFRUIT<br />
<ul>
<li>See <a href="https://shop.mchobby.be/fr/cartes-breakout/528-rfid-nfc-controleur-pn532-3232100005280-adafruit.html">RFID/NFC Controleur PN532 - v1.6 + Extra @ MCHobby</a></li>
<li>See <a href="https://www.adafruit.com/product/364">RFID/NFC Controller PN532 - v1.6 + Extra @ Adafruit</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../tree/master/qwiic-joystick-i2c">qwiic-joystick-i2c</a></td>
      <td><strong>Components</strong> : JOYSTICK-I2C<br />
      <strong>Interfaces</strong> : I2C, QWIIC<br />
<small>Use an I2C analog joystick (Qwiic) with MicroPython</small><br/><br />
      <strong>Tested with</strong> : MICROMOD-RP2040, PICO<br />
      <strong>Manufacturer</strong> : SPARKFUN<br />
<ul>
<li>See <a href="https://www.sparkfun.com/products/15168">Qwiic Analog Joystick @ SparkFun</a></li>
<li>See <a href="https://www.sparkfun.com/products/17720">MicroMod RP2040 Processor @ SparkFun</a></li>
<li>See <a href="https://www.sparkfun.com/products/16400">MicroMod Machine Learning Carrier Board @ SparkFun</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../tree/master/qwiic-keypad-i2c">qwiic-keypad-i2c</a></td>
      <td><strong>Components</strong> : KEYPAD-I2C<br />
      <strong>Interfaces</strong> : I2C, QWIIC<br />
<small>Use an 12 keys I2C Keypad (Qwiic) with MicroPython</small><br/><br />
      <strong>Tested with</strong> : MICROMOD-RP2040, PICO<br />
      <strong>Manufacturer</strong> : SPARKFUN<br />
<ul>
<li>See <a href="https://www.sparkfun.com/products/15290">Qwiic 12 Keys Keypad @ SparkFun</a></li>
<li>See <a href="https://www.sparkfun.com/products/17720">MicroMod RP2040 Processor @ SparkFun</a></li>
<li>See <a href="https://www.sparkfun.com/products/16400">MicroMod Machine Learning Carrier Board @ SparkFun</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../tree/master/qwiic-relay-i2c">qwiic-relay-i2c</a></td>
      <td><strong>Components</strong> : SingleRelay, QuadRelay, DualSsrRelay, QuadSsrRelay<br />
      <strong>Interfaces</strong> : I2C, QWIIC<br />
<small>Using an I2C Single-Relay/Quad-Relay/Quad-SSR-Relay (qwiic) with MicroPython</small><br/><br />
      <strong>Tested with</strong> : MICROMOD-RP2040, PICO<br />
      <strong>Manufacturer</strong> : SPARKFUN<br />
<ul>
<li>See <a href="https://www.sparkfun.com/products/15093">Qwiic Single Relay @ SparkFun</a></li>
<li>See <a href="https://www.sparkfun.com/products/16566">Qwiic Quad Relay @ SparkFun</a></li>
<li>See <a href="https://www.sparkfun.com/products/16833">Qwiic Quad Solid State Relay  @ SparkFun</a></li>
<li>See <a href="https://www.sparkfun.com/products/16810">Qwiic Dual Solid State Relay  @ SparkFun</a></li>
<li>See <a href="https://www.sparkfun.com/products/17720">MicroMod RP2040 Processor @ SparkFun</a></li>
<li>See <a href="https://www.sparkfun.com/products/16400">MicroMod Machine Learning Carrier Board @ SparkFun</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../tree/master/qwiic-serlcd-i2c">qwiic-serlcd-i2c</a></td>
      <td><strong>Components</strong> : SerLCD, LCD-16397, LCD-16396, LCD-16398<br />
      <strong>Interfaces</strong> : I2C, QWIIC<br />
<small>Use a SerLCD I2C LCD display (Qwiic) with MicroPython</small><br/><br />
      <strong>Tested with</strong> : PICO<br />
      <strong>Manufacturer</strong> : SPARKFUN<br />
<ul>
<li>See <a href="https://www.sparkfun.com/products/16397">Qwiic SerLCD LCD-16397 @ SparkFun</a></li>
<li>See <a href="https://www.sparkfun.com/products/16396">Qwiic SerLCD LCD-16396 @ SparkFun</a></li>
<li>See <a href="https://www.sparkfun.com/products/16398">Qwiic SerLCD LCD-16398 @ SparkFun</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../tree/master/qwiic-vcnl4040-i2c">qwiic-vcnl4040-i2c</a></td>
      <td><strong>Components</strong> : VCNL4040-I2C<br />
      <strong>Interfaces</strong> : I2C, QWIIC<br />
<small>Use the proximity VCNL4040 sensor (Qwiic, I2C) with MicroPython</small><br/><br />
      <strong>Tested with</strong> : MICROMOD-RP2040, PICO<br />
      <strong>Manufacturer</strong> : SPARKFUN<br />
<ul>
<li>See <a href="https://www.sparkfun.com/products/15177">Qwiic VCNL4040 distance & proximity sensor @ SparkFun</a></li>
<li>See <a href="https://www.sparkfun.com/products/17720">MicroMod RP2040 Processor @ SparkFun</a></li>
<li>See <a href="https://www.sparkfun.com/products/16400">MicroMod Machine Learning Carrier Board @ SparkFun</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../tree/master/rfm69">rfm69</a></td>
      <td><strong>Components</strong> : RFM69, RFM69HCW<br />
      <strong>Interfaces</strong> : SPI<br />
<small>Use a RFM69HCW packet radio module (SPI) avec MicroPython</small><br/><br />
      <strong>Tested with</strong> : PICO<br />
      <strong>Manufacturer</strong> : ADAFRUIT<br />
<ul>
<li>See <a href="https://shop.mchobby.be/product.php?id_product=1390">Breakout RFM69HCW Transpondeur Radio - 433 MHz - RadioFruit @ MCHobby</a></li>
<li>See <a href="https://www.adafruit.com/product/3071">RFM69HCW radio transceiver breakout - 433 MHz - RadioFruit @ Adafruit</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../tree/master/sht3x">sht3x</a></td>
      <td><strong>Components</strong> : SHT31-F, SHT3x<br />
      <strong>Interfaces</strong> : I2C<br />
<small>Using a SHT3x humidity sensor under MicroPython</small><br/><br />
      <strong>Tested with</strong> : PYBOARD, PYBSTICK<br />
      <strong>Manufacturer</strong> : DFROBOT<br />
<ul>
<li>See <a href="https://shop.mchobby.be/fr/environnemental-press-temp-hrel-gaz/1882-sht31-f-capteur-d-humidite-et-temperature-3232100018822-dfrobot.html">Capteur d'humidité SHT31-F SENS0332 @ MCHobby</a></li>
<li>See <a href="https://www.dfrobot.com/product-2015.html">Capteur d'humidité SHT31-F SENS0332 @ DFRobot</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../tree/master/st7687s">st7687s</a></td>
      <td><strong>Components</strong> : ST7687S<br />
      <strong>Interfaces</strong> : SPI<br />
<small>Using a round TFT under MicroPython</small><br/><br />
      <strong>Tested with</strong> : PYBOARD, PYBSTICK<br />
      <strong>Manufacturer</strong> : DFROBOT<br />
<ul>
<li>See <a href="https://shop.mchobby.be/fr/afficheur-lcd-tft-oled/1856-tft-couleur-22-rond-spi-breakout-3232100018563-dfrobot.html">Ecran TFT DFRobot DFR0529 @ MCHobby</a></li>
<li>See <a href="https://www.dfrobot.com/product-1794.html">Ecran TFT DFRobot DFR0529 @ DFRobot</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../tree/master/stmpe610">stmpe610</a></td>
      <td><strong>Components</strong> : STMPE610<br />
      <strong>Interfaces</strong> : SPI<br />
<small>Using a resistive touch screen sensor with MicroPython</small><br/><br />
      <strong>Tested with</strong> : PICO<br />
      <strong>Manufacturer</strong> : <br />
<ul>
<li>See <a href="https://shop.mchobby.be/fr/feather-adafruit/1050-tft-featherwing-24-touch-320x240-3232100010505-adafruit.html">Ecran FeatherWing TFT 2.4 Adafruit @ MCHobby</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../tree/master/tca9554a">tca9554a</a></td>
      <td><strong>Components</strong> : TCA9554A<br />
      <strong>Interfaces</strong> : I2C<br />
<small>Add 8 input/output GPIO with the TCA9554A</small><br/><br />
      <strong>Tested with</strong> : PYBOARD, PICO<br />
      <strong>Manufacturer</strong> : <br />
<ul>
<li>See <a href="https://shop.mchobby.be/">TCA9544A - 8 bits GPIO extender</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../tree/master/tcs34725">tcs34725</a></td>
      <td><strong>Components</strong> : TCS34725<br />
      <strong>Interfaces</strong> : I2C<br />
<small>Read the color (rgb or Kelvin) with a TCS34725 sensor + MED + IR filter.</small><br/><br />
      <strong>Tested with</strong> : PYBOARD, FEATHER-ESP8266<br />
      <strong>Manufacturer</strong> : ADAFRUIT<br />
<ul>
<li>See <a href="https://shop.mchobby.be/fr/afficheur-lcd-tft-oled/475-lcd-16x2-rgb-positif-usb-serie-3232100004757.html">TCS34725 - capteur de couleur RGB + Filtre IR + LED blanche @ MCHobby</a></li>
<li>See <a href="https://www.adafruit.com/product/1334">RGB Color Sensor with IR filter and White LED - TCS34725 @ Adafruit</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../tree/master/trackball">trackball</a></td>
      <td><strong>Components</strong> : TRACKBALL-BREAKOUT<br />
      <strong>Interfaces</strong> : I2C<br />
<small>Add a Trackball + RGBW LED to your MicroPython project</small><br/><br />
      <strong>Tested with</strong> : PYBOARD, PYBSTICK<br />
      <strong>Manufacturer</strong> : PIMORONI<br />
<ul>
<li>See <a href="https://shop.mchobby.be/fr/tactile-flex-pot-softpad/1833-trackball-i2c-avec-retro-eclairage-3232100018334-pimoroni.html">Trackball I2C avec retro-éclairage @ MCHobby</a></li>
<li>See <a href="https://shop.pimoroni.com/products/trackball-breakout">Trackball Breakout @ Pimoroni</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../tree/master/tsl2561">tsl2561</a></td>
      <td><strong>Components</strong> : TSL2561, ADA439<br />
      <strong>Interfaces</strong> : I2C<br />
<small>The TSL2561 is a visible light <strong>luminosity</strong> sensor having a response close from human Eyes. It produces values in LUX.</small><br/><br />
      <strong>Tested with</strong> : FEATHER-ESP8266<br />
      <strong>Manufacturer</strong> : ADAFRUIT<br />
<ul>
<li>See <a href="https://shop.mchobby.be/product.php?id_product=238">Capteur Lux/Luminosité/Lumière digital</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../tree/master/tsl2591">tsl2591</a></td>
      <td><strong>Components</strong> : TSL2591, ADA1980<br />
      <strong>Interfaces</strong> : I2C<br />
<small>The TSL2591 is a visible light <strong>luminosity</strong> sensor having a response close from human Eyes. It produces values in LUX.</small><br/><br />
      <strong>Tested with</strong> : FEATHER-ESP8266, PYBOARD<br />
      <strong>Manufacturer</strong> : ADAFRUIT<br />
<ul>
<li>See <a href="https://shop.mchobby.be/product.php?id_product=1599">TSL2591 @ MCHobby - Capteur Lux/Luminosité/Lumière digital</a></li>
<li>See <a href="https://www.adafruit.com/product/1980">TSL2591 @ Adafruit - Capteur Lux/Luminosité/Lumière digital</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../tree/master/umqtt">umqtt</a></td>
      <td><strong>Components</strong> : <br />
      <strong>Interfaces</strong> : <br />
<small>MQTT Communication exemples with ESP8266 module.</small><br/><br />
      <strong>Tested with</strong> : FEATHER-ESP8266, PYBOARD<br />
      <strong>Manufacturer</strong> : NONE<br />
<ul>
<li>See <a href="https://shop.mchobby.be/product.php?id_product=846">Feather ESP8266</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../tree/master/veml6075">veml6075</a></td>
      <td><strong>Components</strong> : VEML6075, SEN0303<br />
      <strong>Interfaces</strong> : I2C<br />
<small>The VEML6075 sensor is sensitive to <strong>ultraviolet light</strong> (315~375nm) and can calculate the UV Index of visible light en lumière visible.</small><br/><br />
      <strong>Tested with</strong> : PICO<br />
      <strong>Manufacturer</strong> : DFROBOT<br />
<ul>
<li>See <a href="https://shop.mchobby.be/fr/environnemental-press-temp-hrel-gaz/1881-mesure-ultraviolet-veml6075-gravity-i2c-3232100018815-dfrobot.html">VEML6075 @ MCHobby - Capteur UltraViolet / Index UV numérique</a></li>
<li>See <a href="https://www.dfrobot.com/product-1906.html">VEML6075 @ DFRobot - UltraViolet / UV Index digital sensor</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../tree/master/weather-station">weather-station</a></td>
      <td><strong>Components</strong> : GPIO<br />
      <strong>Interfaces</strong> : UART<br />
<small>Weather Station Kit with Anemometer/Wind Vane/Rain Bucket</small><br/><br />
      <strong>Tested with</strong> : PICO<br />
      <strong>Manufacturer</strong> : DFROBOT<br />
<ul>
<li>See <a href="https://shop.mchobby.be/product.php?id_product=2385">Station Meteo @ MCHobby</a></li>
<li>See <a href="https://www.dfrobot.com/product-1308.html">Weather Station @ DFRobot</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../tree/master/winbond">winbond</a></td>
      <td><strong>Components</strong> : W25Qxx, FLASH<br />
      <strong>Interfaces</strong> : SPI<br />
<small>Using a QSPI Flash memory with MicroPython (in SPI)</small><br/><br />
      <strong>Tested with</strong> : PICO<br />
      <strong>Manufacturer</strong> : <br />
<ul>
<li>See <a href="https://www.digikey.be/fr/products/detail/winbond-electronics/W25Q128JVSIQ/5803943">W25Q128JVSIQ @ Digikey</a></li>
</ul>
      </td>
  </tr>
</tbody>
</table>

# Ressources
* [__Wiki about MicroPython on ESP8266__]( https://wiki.mchobby.be/index.php?title=MicroPython-Accueil#ESP8266_en_MicroPython), a french support to learn how to flash an ESP with MicroPython.
* [__GitHub dedicated to the Pyboard__](https://github.com/mchobby/pyboard-driver) with other drivers requiring more ressources. https://github.com/mchobby/pyboard-driver.
* Where to buy - https://shop.mchobby.be


There are many Adafruit  drivers (various plateforms) on this Github (Tony Dicola)
* https://github.com/adafruit/micropython-adafruit-bundle/tree/master/libraries/drivers

And some IMU (inertial sensor) driver on Github
* https://github.com/micropython-IMU/

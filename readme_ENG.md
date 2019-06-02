[Ce fichier existe également en FRANCAIS](readme.md)

# ESP8266 MicroPython Driver

This is a collection of drivers (and wiring) for various board, breakout and connectors used with an __ESP8266 under MicroPython__.

IF it works with the ESP8266 THEN it will also run with the [MicroPython Pyboard](https://shop.mchobby.be/fr/56-micropython) or any other MicroPython boards!

![ESP8266 and Pyboard](docs/_static/ESP8266-to-PYBOARD.jpg)

The most easiest plateform to flash with MicroPython are the [Feather ESP8266 HUZZA ADA2821](http://shop.mchobby.be/product.php?id_product=846) or an [ESP8266-EVB evaluation board from Olimex](https://shop.mchobby.be/esp8266-esp32-wifi-iot/668-module-wifi-esp8266-carte-d-evaluation-3232100006683-olimex.html) or a [WEMOS / LOLIN (ESP modules) boards](https://shop.mchobby.be/fr/123-wemos-lolin-esp)

![Feather ESP8266](docs/_static/FEAT-HUZZA-ESP8266-01.jpg)
![Olimex ESP8266 Evaluation Board](docs/_static/ESP8266-EVB.jpg)
![Wemos D1 (ESP8266)](docs/_static/WEMOS-D1.jpg)

# Other information source
* [__Wiki about MicroPython on ESP8266__]( https://wiki.mchobby.be/index.php?title=MicroPython-Accueil#ESP8266_en_MicroPython), a french support to learn how to flash an ESP with MicroPython.
* [__GitHub dedicated to the Pyboard__](https://github.com/mchobby/pyboard-driver) with other drivers requiring more ressources. https://github.com/mchobby/pyboard-driver.
* Where to buy - https://shop.mchobby.be

# Available libraries
Here is a description of the libraries available in this repository. <strong>Each sub-folders contain README file with additionnal informations about the driver, examples and wiring.</strong>

Explorer par:
* Interface:
[FEATHERWING](docs/drv_by_intf_FEATHERWING_ENG.md), [GPIO](docs/drv_by_intf_GPIO_ENG.md), [I2C](docs/drv_by_intf_I2C_ENG.md), [NCD](docs/drv_by_intf_NCD_ENG.md), [ONEWIRE](docs/drv_by_intf_ONEWIRE_ENG.md), [QWIIC](docs/drv_by_intf_QWIIC_ENG.md), [SPI](docs/drv_by_intf_SPI_ENG.md), [UART](docs/drv_by_intf_UART_ENG.md), [UEXT](docs/drv_by_intf_UEXT_ENG.md)
* Fabriquant:
[ADAFRUIT](docs/drv_by_man_ADAFRUIT_ENG.md), [NCD](docs/drv_by_man_NCD_ENG.md), [NONE](docs/drv_by_man_NONE_ENG.md), [OLIMEX](docs/drv_by_man_OLIMEX_ENG.md), [SPARKFUN](docs/drv_by_man_SPARKFUN_ENG.md)
<table>
<thead>
  <th>Folder</th><th>Description</th>
</thead>
<tbody>
  <tr><td>NCD</td>
      <td><strong>Components</strong> : NCD<br />
      <strong>Interfaces</strong> : I2C, NCD<br />
      <strong>Tested with</strong> : ESP8266-EVB, FEATHER-ESP8266, WEMOS-D1<br />
<small>Connect NCD (National Control Device) __I2C mini board__  easily to a MicroPython microcontroler with the <strong>NCD connector</strong>. I2C connexion made easy, 5V logic.</small>
<br /><ul>
<li>See <a href="https://ncd.io/">NCD.io</a></li>
<li>See <a href="https://ncd.io/">National Control Device</a></li>
</ul>
      </td>
  </tr>
  <tr><td>UEXT</td>
      <td><strong>Components</strong> : UEXT<br />
      <strong>Interfaces</strong> : I2C, SPI, UART<br />
      <strong>Tested with</strong> : ESP8266-EVB<br />
<small><strong>UEXT</strong> connector work in 3.3V logic and is used on many board and extension of Olimex. It ship I2C, SPI, UART buses as well as 3.3V</small>
<br /><ul>
<li>See <a href="https://shop.mchobby.be/fr/138-uext">UEXT @ MCHobby</a></li>
<li>See <a href="https://www.olimex.com/Products/Modules/">UEXT @ Olimex</a></li>
</ul>
      </td>
  </tr>
  <tr><td>ads1015-ads1115</td>
      <td><strong>Components</strong> : ADS1015, ADS1115, ADA1085<br />
      <strong>Interfaces</strong> : I2C<br />
      <strong>Tested with</strong> : FEATHER-ESP8266<br />
<small>ADC converter (Analog to Digital) 4 channel allowing analog reading and differential reading.<br />L'ADS1115 have a internal amplifier (programmable) that can be used to read very small voltage.</small>
<br /><ul>
<li>See <a href="https://shop.mchobby.be/breakout/362-ads1115-convertisseur-adc-16bits-i2c-3232100003620-adafruit.html">ADS1115 breakout</a></li>
</ul>
      </td>
  </tr>
  <tr><td>am2315</td>
      <td><strong>Components</strong> : AM2315<br />
      <strong>Interfaces</strong> : I2C<br />
      <strong>Tested with</strong> : FEATHER-ESP8266<br />
<small><strong>Temperature & relative humidity</strong> (0 to 100%) sensor for capture outside data.</small>
<br /><ul>
<li>See <a href="https://shop.mchobby.be/fr/environnemental-press-temp-hrel-gaz/932-am2315-senseur-de-temperature-et-humidite-sous-boitier-3232100009325.html">AM2315 Sensor</a></li>
</ul>
      </td>
  </tr>
  <tr><td>bme280-bmp280</td>
      <td><strong>Components</strong> : BME280, BMP280, ADA2651, ADA2652<br />
      <strong>Interfaces</strong> : I2C<br />
      <strong>Tested with</strong> : FEATHER-ESP8266<br />
<small>The BMP280 is a very popular <strong>pressure and temperatur</strong> sensor.<br />The BME280 is a sensor for <strong>pressure, temperature and relative HUMIDITY</strong></small>
<br /><ul>
<li>See <a href="http://shop.mchobby.be/product.php?id_product=1118">BMP280 Sensor</a></li>
<li>See <a href="http://shop.mchobby.be/product.php?id_product=684">BME280 Sensor</a></li>
</ul>
      </td>
  </tr>
  <tr><td>bmp180</td>
      <td><strong>Components</strong> : BMP180<br />
      <strong>Interfaces</strong> : I2C<br />
      <strong>Tested with</strong> : FEATHER-ESP8266<br />
<small>The BMP180 is a <strong>pressure & temperature</strong> sensor now replaced with the BMP280.</small>
<br /><ul>
<li>See <a href="http://shop.mchobby.be/product.php?id_product=397">BMP180 Sensor</a></li>
</ul>
      </td>
  </tr>
  <tr><td>dht11</td>
      <td><strong>Components</strong> : DHT11<br />
      <strong>Interfaces</strong> : GPIO<br />
      <strong>Tested with</strong> : FEATHER-ESP8266<br />
<small>The DHT11 is a very cheap <strong>humidity</strong> (20 to 80%) and temperature sensor.</small>
<br /><ul>
<li>See <a href="http://shop.mchobby.be/product.php?id_product=708">DHT11 Sensor</a></li>
</ul>
      </td>
  </tr>
  <tr><td>ds18b20</td>
      <td><strong>Components</strong> : DS18B20<br />
      <strong>Interfaces</strong> : ONEWIRE<br />
      <strong>Tested with</strong> : FEATHER-ESP8266<br />
<small>The DS18B20 is a very popular <strong>temperature</strong> sensor. It use the 1-Wire bus to connect several sensors.</small>
<br /><ul>
<li>See <a href="http://shop.mchobby.be/product.php?id_product=259">DS18B20 Sensor</a></li>
</ul>
      </td>
  </tr>
  <tr><td>mcp230xx</td>
      <td><strong>Components</strong> : MCP23017, MCP23008<br />
      <strong>Interfaces</strong> : I2C<br />
      <strong>Tested with</strong> : FEATHER-ESP8266<br />
<small>The MCP23017 (and MCP2308) are <strong>GPIO Expander</strong> adding additionnal input/output to a microcontroler.</small>
<br /><ul>
<li>See <a href="http://shop.mchobby.be/product.php?id_product=218">MCP23017 GPIO Expander</a></li>
</ul>
      </td>
  </tr>
  <tr><td>modio</td>
      <td><strong>Components</strong> : MOD-IO<br />
      <strong>Interfaces</strong> : I2C, UEXT<br />
      <strong>Tested with</strong> : ESP8266-EVB<br />
<small>MOD-IO is an I2C extension board with <strong>UEXT</strong> connector. This Olimex's Board have relays, OptoCoupler input (24V) and analog input (0-3.3V).<br />This board is compatible with the industrial grade voltages (24V).</small>
<br /><ul>
<li>See <a href="https://shop.mchobby.be/fr/138-uext">UEXT @ MCHobby</a></li>
<li>See <a href="https://www.olimex.com/Products/Modules/">UEXT @ Olimex</a></li>
</ul>
      </td>
  </tr>
  <tr><td>modio2</td>
      <td><strong>Components</strong> : MOD-IO2<br />
      <strong>Interfaces</strong> : I2C, UEXT<br />
      <strong>Tested with</strong> : ESP8266-EVB<br />
<small>MOD-IO is an I2C extension board with <strong>UEXT</strong> connector. This Olimex's Board have relays, and GPIOs with various functions (Input, Output, Analog, PWM; 0-3.3V).</small>
<br /><ul>
<li>See <a href="https://shop.mchobby.be/fr/138-uext">UEXT @ MCHobby</a></li>
<li>See <a href="https://www.olimex.com/Products/Modules/">UEXT @ Olimex</a></li>
</ul>
      </td>
  </tr>
  <tr><td>modlcd1x9</td>
      <td><strong>Components</strong> : MOD-LCD-1x9<br />
      <strong>Interfaces</strong> : I2C, UEXT<br />
      <strong>Tested with</strong> : ESP8266-EVB<br />
<small>MOD-LCD1x9 is an I2C'based 9 characters alphanumeric display using the <strong>UEXT</strong> connector.</small>
<br /><ul>
<li>See <a href="https://shop.mchobby.be/esp8266-esp32-wifi-iot/1414-uext-lcd-display-1-line-of-9-alphanumeric-chars-3232100014145-olimex.html">MOD-LCD1x9 @ MCHobby</a></li>
<li>See <a href="https://www.olimex.com/Products/Modules/">UEXT @ Olimex</a></li>
</ul>
      </td>
  </tr>
  <tr><td>modltr501</td>
      <td><strong>Components</strong> : MOD-LTR-501ALS, LTR-501ALS<br />
      <strong>Interfaces</strong> : I2C, UEXT<br />
      <strong>Tested with</strong> : ESP8266-EVB<br />
<small>LTR-501ALS can be used to acquires luminosity data from 0.01 to 64.000 Lux (64K lux) and make proximity detection (up to 10cm). The MOD-MAG have an <strong>UEXT</strong> connector to ease wiring.</small>
<br /><ul>
<li>See <a href="https://shop.mchobby.be/uext/1415-senseur-proximite-et-lumiere-ltr501-connecteur-uext-3232100014152-olimex.html">MOD-LTR-501ALS @ MCHobby</a></li>
<li>See <a href="https://www.olimex.com/Products/Modules/">UEXT @ Olimex</a></li>
</ul>
      </td>
  </tr>
  <tr><td>modmag</td>
      <td><strong>Components</strong> : MOD-MAG, MAG3110<br />
      <strong>Interfaces</strong> : I2C, UEXT<br />
      <strong>Tested with</strong> : ESP8266-EVB<br />
<small>The MAG3110 is a digital 3 axis magnetometer from NXP running over an I2C bus. The MOD-MAG have an <strong>UEXT</strong> connector to ease wiring.</small>
<br /><ul>
<li>See <a href="https://shop.mchobby.be/esp8266-esp32-wifi-iot/1413-uext-mag3110-magnetometer-module-3232100014138-olimex.html">MOD-MAG @ MCHobby</a></li>
<li>See <a href="https://www.olimex.com/Products/Modules/">UEXT @ Olimex</a></li>
</ul>
      </td>
  </tr>
  <tr><td>modoled128x64</td>
      <td><strong>Components</strong> : SSD1306, MOD-OLED-128x64, OLED<br />
      <strong>Interfaces</strong> : I2C, UEXT<br />
      <strong>Tested with</strong> : ESP8266-EVB<br />
<small>A 128x64 display with the SSD1306 I2C controler exposing a UEXT connector.</small>
<br /><ul>
<li>See <a href="https://shop.mchobby.be/product.php?id_product=1411">Afficheur OLED 128 x 64 avec interface I2C et UEXT</a></li>
</ul>
      </td>
  </tr>
  <tr><td>modrgb</td>
      <td><strong>Components</strong> : MOD-RGB<br />
      <strong>Interfaces</strong> : I2C, UEXT<br />
      <strong>Tested with</strong> : ESP8266-EVB<br />
<small>MOD-RGB is an I2C extension board with <strong>UEXT</strong> connector. This Olimex's Board have power MosFet to control RGB analogic LED strips via I2C (or DMX).</small>
<br /><ul>
<li>See <a href="https://shop.mchobby.be/fr/138-uext">UEXT @ MCHobby</a></li>
<li>See <a href="https://www.olimex.com/Products/Modules/">UEXT @ Olimex</a></li>
</ul>
      </td>
  </tr>
  <tr><td>modwii</td>
      <td><strong>Components</strong> : MOD-Wii-UEXT-NUNCHUCK, NUNCHUCK<br />
      <strong>Interfaces</strong> : I2C, UEXT<br />
      <strong>Tested with</strong> : ESP8266-EVB<br />
<small>The Wii NUNCHUCK is a game controler very comfortable to used and runs over the I2C bus. This controler have an <strong>UEXT</strong> connector to ease wiring.</small>
<br /><ul>
<li>See <a href="https://shop.mchobby.be/esp8266-esp32-wifi-iot/1416-uext-wii-nunchuck-controller-3232100014169-olimex.html">Wii Nunchuck game controller (UEXT) @ MCHobby</a></li>
<li>See <a href="https://www.olimex.com/Products/Modules/">UEXT @ Olimex</a></li>
</ul>
      </td>
  </tr>
  <tr><td>ncd-fet-solenoid</td>
      <td><strong>Components</strong> : I2CDRV8W4I12V, MCP23008<br />
      <strong>Interfaces</strong> : I2C, NCD<br />
      <strong>Tested with</strong> : FEATHER-ESP8266, PYBOARD<br />
<small>FET Output controler + GPIO (based on a MCP23008) for 12V resistive / inductive load (like valve). The <i>I2C NCD board</i> have the <strong>NCD</strong> connector which facilitate the device wiring.<br />The MPL115A2 is also available as breakout.</small>
<br /><ul>
<li>See <a href="https://ncd.io/">NCD.io</a></li>
<li>See <a href="https://ncd.io/">National Control Device</a></li>
</ul>
      </td>
  </tr>
  <tr><td>ncd-mpl115A2</td>
      <td><strong>Components</strong> : MPL115A2, ADA992<br />
      <strong>Interfaces</strong> : I2C, NCD<br />
      <strong>Tested with</strong> : FEATHER-ESP8266, PYBOARD<br />
<small>The MPL115A2 sensor capture the pressure and temperature over I2C bus. The <i>I2C NCD mini board</i> have the <strong>NCD</strong> connector which facilitate the device wiring.<br />The MPL115A2 is also available as breakout.</small>
<br /><ul>
<li>See <a href="https://ncd.io/">NCD.io</a></li>
<li>See <a href="https://ncd.io/">National Control Device</a></li>
</ul>
      </td>
  </tr>
  <tr><td>ncd-oled</td>
      <td><strong>Components</strong> : SSD1306, I2COLED, OLED<br />
      <strong>Interfaces</strong> : I2C, NCD<br />
      <strong>Tested with</strong> : FEATHER-ESP8266, PYBOARD<br />
<small>A 128x64 display with the SSD1306 I2C controler exposing a NCD connector.</small>
<br /><ul>
<li>See <a href="https://ncd.io/">NCD.io - National Control Device</a></li>
<li>See <a href="https://store.ncd.io/product/oled-128x64-graphic-display-i2c-mini-module/">NCD oled 128x64 i2c mini module</a></li>
</ul>
      </td>
  </tr>
  <tr><td>ncd-pecmac</td>
      <td><strong>Components</strong> : DLCT27C10, OPCT16AL, I2CCMAC230A, PECMAC2xxxA<br />
      <strong>Interfaces</strong> : I2C, NCD<br />
      <strong>Tested with</strong> : FEATHER-ESP8266, PYBOARD<br />
<small>AC Current sensor on I2C bus (or IoT interface). The <i>I2C NCD board</i> have the <strong>NCD</strong> connector which facilitate the device wiring.<br />The MPL115A2 is also available as breakout.</small>
<br /><ul>
<li>See <a href="https://ncd.io/">NCD.io</a></li>
<li>See <a href="https://ncd.io/">National Control Device</a></li>
</ul>
      </td>
  </tr>
  <tr><td>ncd-si7005</td>
      <td><strong>Components</strong> : SI7005<br />
      <strong>Interfaces</strong> : I2C, NCD<br />
      <strong>Tested with</strong> : FEATHER-ESP8266, PYBOARD<br />
<small>The SI7005 is a pressure and temperature sensor working over the I2C bus. The <i>I2C NCD mini board</i> have the <strong>NCD</strong> connector which facilitate the device wiring.<br />The MPL115A2 is also available as breakout.</small>
<br /><ul>
<li>See <a href="https://ncd.io/">NCD.io</a></li>
<li>See <a href="https://ncd.io/">National Control Device</a></li>
</ul>
      </td>
  </tr>
  <tr><td>ncd-water-detect</td>
      <td><strong>Components</strong> : WATER-DETECT, WDBZ, PCA9536<br />
      <strong>Interfaces</strong> : I2C, NCD<br />
      <strong>Tested with</strong> : FEATHER-ESP8266, PYBOARD<br />
<small>Water detection + Buzzer + 2 extra GPIOs (based on a PCA9536). The <i>I2C NCD mini board</i> have the <strong>NCD</strong> connector which facilitate the device wiring.<br />The MPL115A2 is also available as breakout.</small>
<br /><ul>
<li>See <a href="https://ncd.io/">NCD.io</a></li>
<li>See <a href="https://ncd.io/">National Control Device</a></li>
</ul>
      </td>
  </tr>
  <tr><td>neopixel</td>
      <td><strong>Components</strong> : NEOPIXEL, 74AHCT125<br />
      <strong>Interfaces</strong> : GPIO<br />
      <strong>Tested with</strong> : FEATHER-ESP8266<br />
<small>The <strong>NéoPixels</strong> are Smart digitals LED that can be controled individually.</small>
<br /><ul>
<li>See <a href="https://shop.mchobby.be/fr/55-neopixels-et-dotstar">NeoPixels</a></li>
<li>See <a href="https://shop.mchobby.be/fr/ci/1041-74ahct125-4x-level-shifter-3v-a-5v-3232100010413.html">74AHCT125</a></li>
</ul>
      </td>
  </tr>
  <tr><td>oled-ssd1306</td>
      <td><strong>Components</strong> : SSD1306, FEATHER-OLED-WING, ADA2900, OLED<br />
      <strong>Interfaces</strong> : I2C, FEATHERWING<br />
      <strong>Tested with</strong> : FEATHER-ESP8266<br />
<small>The SSD1306 is an OLED dislpay contrôler.</small>
<br /><ul>
<li>See <a href="https://shop.mchobby.be/product.php?id_product=879">FeatherWing OLED ssd1306 128x32</a></li>
</ul>
      </td>
  </tr>
  <tr><td>pca9536</td>
      <td><strong>Components</strong> : PCA9536<br />
      <strong>Interfaces</strong> : I2C<br />
      <strong>Tested with</strong> : <br />
<small>4 bit I2C controled GPIO expander.</small>
      </td>
  </tr>
  <tr><td>tsl2561</td>
      <td><strong>Components</strong> : TSL2561, ADA439<br />
      <strong>Interfaces</strong> : I2C<br />
      <strong>Tested with</strong> : FEATHER-ESP8266<br />
<small>The TSL2561 is a visible light <strong>luminosity</strong> sensor having a response close from human Eyes. It produces values in LUX.</small>
<br /><ul>
<li>See <a href="https://shop.mchobby.be/product.php?id_product=238">Capteur Lux/Luminosité/Lumière digital</a></li>
</ul>
      </td>
  </tr>
  <tr><td>umqtt</td>
      <td><strong>Components</strong> : <br />
      <strong>Interfaces</strong> : <br />
      <strong>Tested with</strong> : FEATHER-ESP8266, PYBOARD<br />
<small>MQTT Communication exemples with ESP8266 module.</small>
<br /><ul>
<li>See <a href="https://shop.mchobby.be/product.php?id_product=846">Feather ESP8266</a></li>
</ul>
      </td>
  </tr>
</tbody>
</table>

# Some useful information
* [how-to-install-upy.md](how-to-install-upy.md) how to install MicroPython on ESP8266 from a Linux machine (like the Raspberry-Pi)
 * [erase-esp8266.sh](erase-esp8266.sh) - used to erase the flash from the ESP8266
 * [burn-esp8266.sh](burn-esp8266.sh) - used to flash the [MicroPython binary downloaded from micropython.org/download](https://micropython.org/download/) on a ESP8266
* Configuration file
 * [boot.py](boot.py) - to update with netword SSID and password for the WiFi network. Once copied on the ESP8266 (with RShell), it this file will automatically connect the ESP8266 on the WiFi network.
 * [port_config.py](port_config.py) - to update, it will contain the WebRepl password to protect the connexion. It will be automatically used by WebRepl deamon.  

## RShell

__RShell__ is a wonderfull tool used to edit/transfert/repl your board running MicroPython from a single serial connexion (or Serial over bluetooth).

It is a _really useful_ that would be great to learn... with RShell, you can access the MicroPython filesystem (in Flash memory) to edit and copy files.

The wonderfulnes of RShell, is that it also works great with ESP8266 (thankfully because there are no way to emulate USB Mass Storage on ESP8266, a _flash drive_ like is work with the genuine PyBoard).

 * [French tutorial on RShell](https://wiki.mchobby.be/index.php?title=MicroPython-Hack-RShell)
 * [Rshell GitHub](https://github.com/dhylands/rshell) - with english documentation and installation instruction.
 * [rshell-esp8266.sh](rshell-esp8266.sh) - to update. Calls RShell with a small size exchange buffer (needed for ESP8266).

__WARNING__ : On a ESP8266 it is necessary to reduce the exchange buffer... otherwise, it may corrupt the MicroPython filesystem (and it would be necessary to re-flash the ESP8266 with MicroPython) :-/  See the file [rshell-esp8266.sh](rshell-esp8266.sh) suggested in this repository.

## WebRepl

![Repl](dht11/dht11_webrepl.jpg)

Open WebRepl.html in your WebBrowser to start a REPL Session through an HTTP network connexion.

All you need to know is the IP of the the ESP8266 board on the Network.

__WARNING__ :
* You will have to get your [boot.py](boot.py) file properly configured to connect the WiFi network and to start the WebRepl deamon.
* You can also initialise the WebRepl password in the [port_config.py](port_config.py) file. More recent MicroPython firmware will set the WebRepl password from the Boot.py file.
RShell will be a valuable tool for this configuration task.


# Various links

There are many Adafruit  drivers (various plateforms) on this Github (Tony Dicola)
* https://github.com/adafruit/micropython-adafruit-bundle/tree/master/libraries/drivers

And some IMU (inertial sensor) driver on Github
* https://github.com/micropython-IMU/

# MicroPython Driver for I2C interface
[Return to main page](../../readme_ENG.md)

I2C bus

<table>
<thead>
  <th>Folder</th><th>Description</th>
</thead>
<tbody>
  <tr><td>NCD</td>
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
  <tr><td>UEXT</td>
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
  <tr><td>ads1015-ads1115</td>
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
  <tr><td>am2315</td>
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
  <tr><td>bme280-bmp280</td>
      <td><strong>Components</strong> : BME280, BMP280, ADA2651, ADA2652<br />
      <strong>Interfaces</strong> : I2C<br />
<small>The BMP280 is a very popular <strong>pressure and temperatur</strong> sensor.<br />The BME280 is a sensor for <strong>pressure, temperature and relative HUMIDITY</strong></small><br/><br />
      <strong>Tested with</strong> : FEATHER-ESP8266<br />
      <strong>Manufacturer</strong> : ADAFRUIT<br />
<ul>
<li>See <a href="http://shop.mchobby.be/product.php?id_product=1118">BMP280 Sensor</a></li>
<li>See <a href="http://shop.mchobby.be/product.php?id_product=684">BME280 Sensor</a></li>
</ul>
      </td>
  </tr>
  <tr><td>bmp180</td>
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
  <tr><td>mcp230xx</td>
      <td><strong>Components</strong> : MCP23017, MCP23008<br />
      <strong>Interfaces</strong> : I2C<br />
<small>The MCP23017 (and MCP2308) are <strong>GPIO Expander</strong> adding additionnal input/output to a microcontroler.</small><br/><br />
      <strong>Tested with</strong> : FEATHER-ESP8266<br />
      <strong>Manufacturer</strong> : NONE<br />
<ul>
<li>See <a href="http://shop.mchobby.be/product.php?id_product=218">MCP23017 GPIO Expander</a></li>
</ul>
      </td>
  </tr>
  <tr><td>modio</td>
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
  <tr><td>modio2</td>
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
  <tr><td>modlcd1x9</td>
      <td><strong>Components</strong> : MOD-LCD-1x9<br />
      <strong>Interfaces</strong> : I2C, UEXT<br />
<small>MOD-LCD1x9 is an I2C'based 9 characters alphanumeric display using the <strong>UEXT</strong> connector.</small><br/><br />
      <strong>Tested with</strong> : ESP8266-EVB<br />
      <strong>Manufacturer</strong> : OLIMEX<br />
<ul>
<li>See <a href="https://shop.mchobby.be/esp8266-esp32-wifi-iot/1414-uext-lcd-display-1-line-of-9-alphanumeric-chars-3232100014145-olimex.html">MOD-LCD1x9 @ MCHobby</a></li>
<li>See <a href="https://www.olimex.com/Products/Modules/">UEXT @ Olimex</a></li>
</ul>
      </td>
  </tr>
  <tr><td>modltr501</td>
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
  <tr><td>modmag</td>
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
  <tr><td>modoled128x64</td>
      <td><strong>Components</strong> : SSD1306, MOD-OLED-128x64, OLED<br />
      <strong>Interfaces</strong> : I2C, UEXT<br />
<small>A 128x64 display with the SSD1306 I2C controler exposing a UEXT connector.</small><br/><br />
      <strong>Tested with</strong> : ESP8266-EVB<br />
      <strong>Manufacturer</strong> : OLIMEX<br />
<ul>
<li>See <a href="https://shop.mchobby.be/product.php?id_product=1411">Afficheur OLED 128 x 64 avec interface I2C et UEXT</a></li>
</ul>
      </td>
  </tr>
  <tr><td>modrgb</td>
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
  <tr><td>modwii</td>
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
  <tr><td>ncd-fet-solenoid</td>
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
  <tr><td>ncd-mpl115A2</td>
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
  <tr><td>ncd-oled</td>
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
  <tr><td>ncd-pecmac</td>
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
  <tr><td>ncd-si7005</td>
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
  <tr><td>ncd-water-detect</td>
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
  <tr><td>oled-ssd1306</td>
      <td><strong>Components</strong> : SSD1306, FEATHER-OLED-WING, ADA2900, OLED<br />
      <strong>Interfaces</strong> : I2C, FEATHERWING<br />
<small>The SSD1306 is an OLED display controler.</small><br/><br />
      <strong>Tested with</strong> : FEATHER-ESP8266<br />
      <strong>Manufacturer</strong> : ADAFRUIT<br />
<ul>
<li>See <a href="https://shop.mchobby.be/product.php?id_product=879">FeatherWing OLED ssd1306 128x32</a></li>
</ul>
      </td>
  </tr>
  <tr><td>pca9536</td>
      <td><strong>Components</strong> : PCA9536<br />
      <strong>Interfaces</strong> : I2C<br />
<small>4 bit I2C controled GPIO expander.</small><br/><br />
      <strong>Tested with</strong> : <br />
      <strong>Manufacturer</strong> : NONE<br />
      </td>
  </tr>
  <tr><td>tsl2561</td>
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
</tbody>
</table>

# Pilote MicroPython pour interface I2C
[Retour à la page principale](../../readme.md)

Bus I2C

<table>
<thead>
  <th>Répertoire</th><th>Description</th>
</thead>
<tbody>
  <tr><td><a href="../../../../tree/master/NCD">NCD</a></td>
      <td><strong>Composants</strong> : NCD<br />
      <strong>Interfaces</strong> : I2C, NCD<br />
<small>Connecter facilement une __mini carte I2C__ de NCD (National Control Device) sur une carte MicroPython grâce au connecteur <strong>NCD</strong> qui facilite grandement les raccordements de périphérique I2C. Logique 5V.</small><br/><br />
      <strong>Testé avec</strong> : ESP8266-EVB, FEATHER-ESP8266, WEMOS-D1<br />
      <strong>Fabricant</strong> : NCD<br />
<ul>
<li>Voir <a href="https://ncd.io/">NCD.io</a></li>
<li>Voir <a href="https://ncd.io/">National Control Device</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../../../tree/master/UEXT">UEXT</a></td>
      <td><strong>Composants</strong> : UEXT<br />
      <strong>Interfaces</strong> : I2C, SPI, UART<br />
<small>Connecteur <strong>UEXT</strong> en logique 3.3V est utilisé sur les cartes et capteurs d' Olimex. Il transporte les bus I2C, SPI, UART et alimentation 3.3V</small><br/><br />
      <strong>Testé avec</strong> : ESP8266-EVB<br />
      <strong>Fabricant</strong> : OLIMEX<br />
<ul>
<li>Voir <a href="https://shop.mchobby.be/fr/138-uext">UEXT @ MCHobby</a></li>
<li>Voir <a href="https://www.olimex.com/Products/Modules/">UEXT @ Olimex</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../../../tree/master/adfmotors">adfmotors</a></td>
      <td><strong>Composants</strong> : PCA9685<br />
      <strong>Interfaces</strong> : I2C, UNO-R3<br />
<small>Contrôler des moteurs continu, pas-à-pas ou servo-moteur avec le shield moteur Arduino d'Adafruit.</small><br/><br />
      <strong>Testé avec</strong> : PYBOARD<br />
      <strong>Fabricant</strong> : ADAFRUIT<br />
<ul>
<li>Voir <a href="https://shop.mchobby.be/fr/shields/379-shield-de-controle-moteur-motor-shield-v2-3232100003798-adafruit.html">Adafruit Motor Shield @ MCHobby</a></li>
<li>Voir <a href="https://www.adafruit.com/product/1438">Adafruit Motor Shield @ Adafruit</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../../../tree/master/ads1015-ads1115">ads1015-ads1115</a></td>
      <td><strong>Composants</strong> : ADS1015, ADS1115, ADA1085<br />
      <strong>Interfaces</strong> : I2C<br />
<small>Convertisseur ADC (Analogique vers Digital) 4 canaux pour réaliser des lectures analogiques et lectures différentielles.<br />L'ADS1115 dispose d'un amplificateur interne programmable, ce qui permet de lire des tensions très faibles.</small><br/><br />
      <strong>Testé avec</strong> : FEATHER-ESP8266<br />
      <strong>Fabricant</strong> : ADAFRUIT<br />
<ul>
<li>Voir <a href="https://shop.mchobby.be/breakout/362-ads1115-convertisseur-adc-16bits-i2c-3232100003620-adafruit.html">ADS1115 breakout</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../../../tree/master/am2315">am2315</a></td>
      <td><strong>Composants</strong> : AM2315<br />
      <strong>Interfaces</strong> : I2C<br />
<small>Capteur de <strong>température et humidité</strong> relative (0 à 100%) pour relevés en extérieur.</small><br/><br />
      <strong>Testé avec</strong> : FEATHER-ESP8266<br />
      <strong>Fabricant</strong> : ADAFRUIT<br />
<ul>
<li>Voir <a href="https://shop.mchobby.be/fr/environnemental-press-temp-hrel-gaz/932-am2315-senseur-de-temperature-et-humidite-sous-boitier-3232100009325.html">AM2315 Sensor</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../../../tree/master/bme280-bmp280">bme280-bmp280</a></td>
      <td><strong>Composants</strong> : BME280, BMP280, ADA2651, ADA2652<br />
      <strong>Interfaces</strong> : I2C<br />
<small>Le BMP280 est un senseur de <strong>pression et température</strong> très populaire.<br />Le BME280 est un senseur de <strong>pression, température et HUMIDITÉ</strong> relative</small><br/><br />
      <strong>Testé avec</strong> : FEATHER-ESP8266, PYBOARD<br />
      <strong>Fabricant</strong> : ADAFRUIT<br />
<ul>
<li>Voir <a href="http://shop.mchobby.be/product.php?id_product=1118">BMP280 Sensor</a></li>
<li>Voir <a href="http://shop.mchobby.be/product.php?id_product=684">BME280 Sensor</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../../../tree/master/bmp180">bmp180</a></td>
      <td><strong>Composants</strong> : BMP180<br />
      <strong>Interfaces</strong> : I2C<br />
<small>Le BMP180 est un senseur de <strong>pression et température</strong> aujourd'hui remplacé par le BMP280.</small><br/><br />
      <strong>Testé avec</strong> : FEATHER-ESP8266<br />
      <strong>Fabricant</strong> : ADAFRUIT<br />
<ul>
<li>Voir <a href="http://shop.mchobby.be/product.php?id_product=397">BMP180 Sensor</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../../../tree/master/cardkb">cardkb</a></td>
      <td><strong>Composants</strong> : CARDKB, U035<br />
      <strong>Interfaces</strong> : I2C, GROVE<br />
<small>CardKB - Mini-clavier QWERTY en I2C.</small><br/><br />
      <strong>Testé avec</strong> : PYBOARD, PYBOARD, M5STACK<br />
      <strong>Fabricant</strong> : M5STACK<br />
<ul>
<li>Voir <a href="http://shop.mchobby.be/product.php?id_product=1912">CardKB : Mini Qwerty Keyboard from M5Stack</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../../../tree/master/ccs811">ccs811</a></td>
      <td><strong>Composants</strong> : CCS811<br />
      <strong>Interfaces</strong> : I2C<br />
<small>CCS811 - Capteur qualité d'air - COV et eCO2 avec MicroPython</small><br/><br />
      <strong>Testé avec</strong> : PYBOARD<br />
      <strong>Fabricant</strong> : ADAFRUIT, OLIMEX<br />
<ul>
<li>Voir <a href="https://shop.mchobby.be/product.php?id_product=1274">CCS811 breakout - VOC and eCO2 gaz sensor (ADA3566) @ MCHobby</a></li>
<li>Voir <a href="https://www.adafruit.com/product/3566">CCS811 breakout - VOC and eCO2 gaz sensor (ADA3566) @ Adafruit</a></li>
<li>Voir <a href="https://www.adafruit.com/product/1780">MOD-ENV capteur environnemental @ MC Hobby</a></li>
<li>Voir <a href="https://www.olimex.com/Products/Modules/Sensors/MOD-ENV">MOD-ENV capteur environnemental @ MC Olimex</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../../../tree/master/eeprom">eeprom</a></td>
      <td><strong>Composants</strong> : AT24C512C, AT24C02C, 24LC256<br />
      <strong>Interfaces</strong> : I2C<br />
<small>Utiliser des EEPROM I2C pour stocker des informations.</small><br/><br />
      <strong>Testé avec</strong> : PYBOARD, PYBSTICK<br />
      <strong>Fabricant</strong> : NONE<br />
<ul>
<li>Voir <a href="http://shop.mchobby.be/product.php?id_product=1582">EEPROM 256 Kbit (32Ko), I2C, 24LC256</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../../../tree/master/is31fl">is31fl</a></td>
      <td><strong>Composants</strong> : IS31FL3731<br />
      <strong>Interfaces</strong> : FEATHERWING, I2C<br />
<small>IS31FL3731 - contrôleur CharliePlexing via I2C - sous MicroPython</small><br/><br />
      <strong>Testé avec</strong> : PYBOARD, PYBSTICK<br />
      <strong>Fabricant</strong> : ADAFRUIT<br />
<ul>
<li>Voir <a href="https://shop.mchobby.be/fr/feather-adafruit/1563-featherwing-matrice-led-15x7-en-charlieplexing-pour-feather-3232100015630-adafruit.html">FeatherWing Matrice LED 15x7, ROUGE, CharliePlexing pour Feather @ MCHobby</a></li>
<li>Voir <a href="https://www.adafruit.com/product/3134">FeatherWing Matrice LED 15x7, ROUGE, CharliePlexing pour Feather @ Adafruit</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../../../tree/master/lcdi2c">lcdi2c</a></td>
      <td><strong>Composants</strong> : I2C BackPack, LCD 16x2, LCD 16x4<br />
      <strong>Interfaces</strong> : I2C<br />
<small>Afficheur à cristaux liquides (LCD) commandé via le bus I2C.</small><br/><br />
      <strong>Testé avec</strong> : PYBOARD<br />
      <strong>Fabricant</strong> : NONE<br />
<ul>
<li>Voir <a href="https://shop.mchobby.be/fr/afficheur-lcd-tft-oled/882-lcd-20x4-backpack-i2c-blanc-sur-bleu-3232100008823.html">I2C Backpack for LCD display</a></li>
<li>Voir <a href="https://shop.mchobby.be/fr/afficheur-lcd-tft-oled/881-lcd-20x4-backpack-i2c-blanc-sur-bleu-3232100008816.html">LCD 20x4 + I2C Backpack</a></li>
<li>Voir <a href="https://shop.mchobby.be/fr/nouveaute/1807-afficheur-lcd-16x2-i2c-3232100018075-dfrobot.html">LCD I2C from DFRobot</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../../../tree/master/lsm303">lsm303</a></td>
      <td><strong>Composants</strong> : LSM303D<br />
      <strong>Interfaces</strong> : UNO-R3, I2C<br />
<small>Utiliser une boussole et accéléromètre LSM303D avec MicroPython</small><br/><br />
      <strong>Testé avec</strong> : PYBOARD<br />
      <strong>Fabricant</strong> : POLOLU<br />
<ul>
<li>Voir <a href="https://www.pololu.com/product/2127">LSM303D breakout - 3D Compass and Accelerometer @ Pololu</a></li>
<li>Voir <a href="https://www.pololu.com/product/2510">Robot Zumo pour Arduino (2510) @ Pololu</a></li>
<li>Voir <a href="https://shop.mchobby.be/fr/prototypage-robotique-roue/448-robot-zumo-pour-arduino-assemble-moteurs-3232100004481-pololu.html">Robot Zumo pour Arduino @ MC Hobby</a></li>
<li>Voir <a href="https://shop.mchobby.be/fr/nouveaute/1745-adaptateur-pyboard-vers-uno-r3-extra-3232100017450.html">PYBOARD-UNO-R3 - Adaptateur Pyboard vers UNO-R3 + Extra @ MC Hobby</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../../../tree/master/mcp230xx">mcp230xx</a></td>
      <td><strong>Composants</strong> : MCP23017, MCP23008<br />
      <strong>Interfaces</strong> : I2C<br />
<small>Le MCP23017 (et MCP2308) sont des <strong>GPIO Expander</strong> permettant d'ajouter des entrées/sorties supplémentaires sur un microcontrôleur.</small><br/><br />
      <strong>Testé avec</strong> : FEATHER-ESP8266<br />
      <strong>Fabricant</strong> : NONE<br />
<ul>
<li>Voir <a href="http://shop.mchobby.be/product.php?id_product=218">MCP23017 GPIO Expander</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../../../tree/master/mcp4725">mcp4725</a></td>
      <td><strong>Composants</strong> : MCP4725<br />
      <strong>Interfaces</strong> : I2C<br />
<small>Le MCP4725 (bus I2C) est un DAC -ou- une vraie sortie Analogique 12 bits (0 à 65535).</small><br/><br />
      <strong>Testé avec</strong> : FEATHER-ESP8266, PYBOARD<br />
      <strong>Fabricant</strong> : ADAFRUIT<br />
<ul>
<li>Voir <a href="http://shop.mchobby.be/product.php?id_product=132">MCP4725 12 bits DAC @ MCHobby : Convertisseur Digital/Analogique pour MicroControlleur, interface I2C</a></li>
<li>Voir <a href="https://www.adafruit.com/product/935">MCP4725 12 bits DAC @ Adafruit : 12 bits DAC over I2C bus</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../../../tree/master/mcp9808">mcp9808</a></td>
      <td><strong>Composants</strong> : MCP9808<br />
      <strong>Interfaces</strong> : I2C<br />
<small>Le MCP9808 (bus I2C) permettant de faire un relevé de température avec une précision de 0.25°C.</small><br/><br />
      <strong>Testé avec</strong> : FEATHER-ESP8266, PYBOARD<br />
      <strong>Fabricant</strong> : ADAFRUIT<br />
<ul>
<li>Voir <a href="http://shop.mchobby.be/product.php?id_product=572">MCP9808 @ MCHobby : mesure de température de précision via I2C</a></li>
<li>Voir <a href="https://www.adafruit.com/product/1782">MCP9808 @ Adafruit : High precision temperature sensor</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../../../tree/master/modenv">modenv</a></td>
      <td><strong>Composants</strong> : CCS811, BME280<br />
      <strong>Interfaces</strong> : UEXT, I2C<br />
<small>Capteur environnementale tout-en-un - BME280 + CCS811 - sous MicroPython</small><br/><br />
      <strong>Testé avec</strong> : PYBOARD<br />
      <strong>Fabricant</strong> : OLIMEX<br />
<ul>
<li>Voir <a href="https://shop.mchobby.be/product.php?id_product=1280">MOD-ENV - Capteur environnemental d'Olimex CCS811 + BME280 @ MCHobby</a></li>
<li>Voir <a href="https://www.olimex.com/Products/Modules/Sensors/MOD-ENV">MOD-ENV capteur environnemental @ Olimex</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../../../tree/master/modio">modio</a></td>
      <td><strong>Composants</strong> : MOD-IO<br />
      <strong>Interfaces</strong> : I2C, UEXT<br />
<small>MOD-IO est une carte d'extension I2C avec port de connexion <strong>UEXT</strong>. Cette carte d'Olimex équipé de relais, d'entrée OptoCoupleur (24V) et entrées analogiques (0-3.3V).<br />Cette carte est compatible avec le standard industriel en 24V.</small><br/><br />
      <strong>Testé avec</strong> : ESP8266-EVB<br />
      <strong>Fabricant</strong> : OLIMEX<br />
<ul>
<li>Voir <a href="https://shop.mchobby.be/fr/138-uext">UEXT @ MCHobby</a></li>
<li>Voir <a href="https://www.olimex.com/Products/Modules/">UEXT @ Olimex</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../../../tree/master/modio2">modio2</a></td>
      <td><strong>Composants</strong> : MOD-IO2<br />
      <strong>Interfaces</strong> : I2C, UEXT<br />
<small>MOD-IO est une carte d'extension I2C avec port de connexion <strong>UEXT</strong>. Cette carte d'Olimex équipé de relais, de GPIO aux fonctions multiples (Input, Output, Analog, PWM; 0-3.3V).</small><br/><br />
      <strong>Testé avec</strong> : ESP8266-EVB<br />
      <strong>Fabricant</strong> : OLIMEX<br />
<ul>
<li>Voir <a href="https://shop.mchobby.be/fr/138-uext">UEXT @ MCHobby</a></li>
<li>Voir <a href="https://www.olimex.com/Products/Modules/">UEXT @ Olimex</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../../../tree/master/modirtemp">modirtemp</a></td>
      <td><strong>Composants</strong> : MOD-IR-TEMP, MLX90614<br />
      <strong>Interfaces</strong> : I2C, UEXT<br />
<small>Mesure de température -70°C à 380°C Infrarouge sans contact (MXL90164)</small><br/><br />
      <strong>Testé avec</strong> : FEATHER-ESP8266, PYBOARD<br />
      <strong>Fabricant</strong> : OLIMEX<br />
<ul>
<li>Voir <a href="https://www.olimex.com/Products/Modules/Sensors/MOD-IR-TEMP/open-source-hardware">MOD-IR-TEMP @ Olimex</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../../../tree/master/modlcd1x9">modlcd1x9</a></td>
      <td><strong>Composants</strong> : MOD-LCD-1x9<br />
      <strong>Interfaces</strong> : I2C, UEXT<br />
<small>MOD-LCD1x9 est un afficheur 9 caractères alphanumérique I2C avec port de connexion <strong>UEXT</strong>.</small><br/><br />
      <strong>Testé avec</strong> : ESP8266-EVB, PYBOARD<br />
      <strong>Fabricant</strong> : OLIMEX<br />
<ul>
<li>Voir <a href="https://shop.mchobby.be/esp8266-esp32-wifi-iot/1414-uext-lcd-display-1-line-of-9-alphanumeric-chars-3232100014145-olimex.html">MOD-LCD1x9 @ MCHobby</a></li>
<li>Voir <a href="https://www.olimex.com/Products/Modules/">UEXT @ Olimex</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../../../tree/master/modltr501">modltr501</a></td>
      <td><strong>Composants</strong> : MOD-LTR-501ALS, LTR-501ALS<br />
      <strong>Interfaces</strong> : I2C, UEXT<br />
<small>LTR-501ALS permet de faire une lecture de luminosité de 0.01 à 64.000 Lux (64K lux) et détection de proximité (jusqu'à 10cm). Le MOD-LTR-501ALS dispose d'une connexion <strong>UEXT</strong> facilitant les raccordements.</small><br/><br />
      <strong>Testé avec</strong> : ESP8266-EVB<br />
      <strong>Fabricant</strong> : OLIMEX<br />
<ul>
<li>Voir <a href="https://shop.mchobby.be/uext/1415-senseur-proximite-et-lumiere-ltr501-connecteur-uext-3232100014152-olimex.html">MOD-LTR-501ALS @ MCHobby</a></li>
<li>Voir <a href="https://www.olimex.com/Products/Modules/">UEXT @ Olimex</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../../../tree/master/modmag">modmag</a></td>
      <td><strong>Composants</strong> : MOD-MAG, MAG3110<br />
      <strong>Interfaces</strong> : I2C, UEXT<br />
<small>Le MAG3110 est un magénomètre digital 3 axes de NXP accessible via I2C. Le MOD-MAG dispose d'une connexion <strong>UEXT</strong> facilitant les raccordements.</small><br/><br />
      <strong>Testé avec</strong> : ESP8266-EVB<br />
      <strong>Fabricant</strong> : OLIMEX<br />
<ul>
<li>Voir <a href="https://shop.mchobby.be/esp8266-esp32-wifi-iot/1413-uext-mag3110-magnetometer-module-3232100014138-olimex.html">MOD-MAG @ MCHobby</a></li>
<li>Voir <a href="https://www.olimex.com/Products/Modules/">UEXT @ Olimex</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../../../tree/master/modoled128x64">modoled128x64</a></td>
      <td><strong>Composants</strong> : SSD1306, MOD-OLED-128x64, OLED<br />
      <strong>Interfaces</strong> : I2C, UEXT<br />
<small>Un afficheur OLED 128x64 avec contrôleur SSD1306 (I2C) et connecteur UEXT.</small><br/><br />
      <strong>Testé avec</strong> : ESP8266-EVB<br />
      <strong>Fabricant</strong> : OLIMEX<br />
<ul>
<li>Voir <a href="https://shop.mchobby.be/product.php?id_product=1411">Afficheur OLED 128 x 64 avec interface I2C et UEXT</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../../../tree/master/modrgb">modrgb</a></td>
      <td><strong>Composants</strong> : MOD-RGB<br />
      <strong>Interfaces</strong> : I2C, UEXT<br />
<small>MOD-RGB est une carte d'extension I2C avec port de connexion <strong>UEXT</strong>. Cette carte d'Olimex équipé de MosFet de puissance pour commander des rubans LED RGB analogiques via I2C (ou DMX).</small><br/><br />
      <strong>Testé avec</strong> : ESP8266-EVB<br />
      <strong>Fabricant</strong> : OLIMEX<br />
<ul>
<li>Voir <a href="https://shop.mchobby.be/fr/138-uext">UEXT @ MCHobby</a></li>
<li>Voir <a href="https://www.olimex.com/Products/Modules/">UEXT @ Olimex</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../../../tree/master/modtc-mk2">modtc-mk2</a></td>
      <td><strong>Composants</strong> : MOD-TC-MK2-31855<br />
      <strong>Interfaces</strong> : UEXT, I2C<br />
<small>MAX6MOD-TC-MK2 : Amplificateur Thermocouple Type-K (MAX31855) via I2C - sous MicroPython</small><br/><br />
      <strong>Testé avec</strong> : PYBOARD<br />
      <strong>Fabricant</strong> : OLIMEX<br />
<ul>
<li>Voir <a href="https://shop.mchobby.be/fr/uext/1624-mod-tc-mk2-31855-interface-thermocouple-type-k-avec-max31855-bus-i2c-gpio-3232100016248-olimex.html">MOD-TC-MK2 - Amplificateur Thermocouple Type-K (MAX31855) via I2C d'Olimex @ MCHobby</a></li>
<li>Voir <a href="https://www.olimex.com/Products/Modules/Sensors/MOD-TC-MK2-31855/open-source-hardware">MOD-TC-MK2 - Type-K Thermocouple Amplifier (MAX31855) over I2C from Olimex @ Olimex</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../../../tree/master/modwii">modwii</a></td>
      <td><strong>Composants</strong> : MOD-Wii-UEXT-NUNCHUCK, NUNCHUCK<br />
      <strong>Interfaces</strong> : I2C, UEXT<br />
<small>La Wii NUNCHUCK est une manette de jeu super confortable et s'utilise sur le bus I2C. Ce controleur dispose d'une connexion <strong>UEXT</strong> facilitant les raccordements.</small><br/><br />
      <strong>Testé avec</strong> : ESP8266-EVB<br />
      <strong>Fabricant</strong> : OLIMEX<br />
<ul>
<li>Voir <a href="https://shop.mchobby.be/esp8266-esp32-wifi-iot/1416-uext-wii-nunchuck-controller-3232100014169-olimex.html">Wii Nunchuck game controller (UEXT) @ MCHobby</a></li>
<li>Voir <a href="https://www.olimex.com/Products/Modules/">UEXT @ Olimex</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../../../tree/master/mpr121">mpr121</a></td>
      <td><strong>Composants</strong> : MPR121<br />
      <strong>Interfaces</strong> : I2C<br />
<small>Créer des pastilles/entrées capacitives (tactiles) avec le MPR121</small><br/><br />
      <strong>Testé avec</strong> : PYBOARD, FEATHER-ESP8266<br />
      <strong>Fabricant</strong> : ADAFRUIT<br />
<ul>
<li>Voir <a href="https://shop.mchobby.be/fr/tactile-flex-pot-softpad/1685-capteur-capacitif-12-touches-mpr121-3232100016859-adafruit.html">MPR121 - capteur capacitif 12 entrées/touches @ MCHobby</a></li>
<li>Voir <a href="https://www.adafruit.com/product/1982">12-Key Capacitive Touch Sensor Breakout - MPR121 @ Adafruit</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../../../tree/master/ncd-fet-solenoid">ncd-fet-solenoid</a></td>
      <td><strong>Composants</strong> : I2CDRV8W4I12V, MCP23008<br />
      <strong>Interfaces</strong> : I2C, NCD<br />
<small>Contrôleur de sortie FET + GPIO (basé sur un MCP23008) pour charge résistive / inductive 12V (valve). La <i>carte I2C de NCD</i> propose un  connecteur <strong>NCD</strong> qui facilite grandement les raccordements de périphérique I2C.<br />Ce senseur est également disponible sous forme de breakout.</small><br/><br />
      <strong>Testé avec</strong> : FEATHER-ESP8266, PYBOARD<br />
      <strong>Fabricant</strong> : NCD<br />
<ul>
<li>Voir <a href="https://ncd.io/">NCD.io</a></li>
<li>Voir <a href="https://ncd.io/">National Control Device</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../../../tree/master/ncd-mpl115a2">ncd-mpl115a2</a></td>
      <td><strong>Composants</strong> : MPL115A2, ADA992<br />
      <strong>Interfaces</strong> : I2C, NCD<br />
<small>Le MPL115A2 est un capteur de pression et température I2C. La <i>mini carte I2C de NCD</i> propose un  connecteur <strong>NCD</strong> qui facilite grandement les raccordements de périphérique I2C.<br />Ce senseur est également disponible sous forme de breakout.</small><br/><br />
      <strong>Testé avec</strong> : FEATHER-ESP8266, PYBOARD<br />
      <strong>Fabricant</strong> : NCD, ADAFRUIT<br />
<ul>
<li>Voir <a href="https://ncd.io/">NCD.io</a></li>
<li>Voir <a href="https://ncd.io/">National Control Device</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../../../tree/master/ncd-oled">ncd-oled</a></td>
      <td><strong>Composants</strong> : SSD1306, I2COLED, OLED<br />
      <strong>Interfaces</strong> : I2C, NCD<br />
<small>Un afficheur OLED 128x64 avec contrôleur SSD1306 (I2C) et connecteur NCD.</small><br/><br />
      <strong>Testé avec</strong> : FEATHER-ESP8266, PYBOARD<br />
      <strong>Fabricant</strong> : NCD<br />
<ul>
<li>Voir <a href="https://ncd.io/">NCD.io - National Control Device</a></li>
<li>Voir <a href="https://store.ncd.io/product/oled-128x64-graphic-display-i2c-mini-module/">NCD oled 128x64 i2c mini module</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../../../tree/master/ncd-pecmac">ncd-pecmac</a></td>
      <td><strong>Composants</strong> : DLCT27C10, OPCT16AL, I2CCMAC230A, PECMAC2xxxA<br />
      <strong>Interfaces</strong> : I2C, NCD<br />
<small>Capteur de courant alternatif sur bus I2C (ou interface IoT). La <i>carte I2C de NCD</i> propose un  connecteur <strong>NCD</strong> qui facilite grandement les raccordements de périphérique I2C.<br />Ce senseur est également disponible sous forme de breakout.</small><br/><br />
      <strong>Testé avec</strong> : FEATHER-ESP8266, PYBOARD<br />
      <strong>Fabricant</strong> : NCD<br />
<ul>
<li>Voir <a href="https://ncd.io/">NCD.io</a></li>
<li>Voir <a href="https://ncd.io/">National Control Device</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../../../tree/master/ncd-si7005">ncd-si7005</a></td>
      <td><strong>Composants</strong> : SI7005<br />
      <strong>Interfaces</strong> : I2C, NCD<br />
<small>Le SI7005 est un capteur d'humidité relative et température I2C. La <i>mini carte I2C de NCD</i> propose un  connecteur <strong>NCD</strong> qui facilite grandement les raccordements de périphérique I2C.<br />Ce senseur est également disponible sous forme de breakout.</small><br/><br />
      <strong>Testé avec</strong> : FEATHER-ESP8266, PYBOARD<br />
      <strong>Fabricant</strong> : NCD<br />
<ul>
<li>Voir <a href="https://ncd.io/">NCD.io</a></li>
<li>Voir <a href="https://ncd.io/">National Control Device</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../../../tree/master/ncd-water-detect">ncd-water-detect</a></td>
      <td><strong>Composants</strong> : WATER-DETECT, WDBZ, PCA9536<br />
      <strong>Interfaces</strong> : I2C, NCD<br />
<small>Détecteur de présence d'eau + Buzzer + 2 GPIOs (basé sur un PCA9536). La <i>mini carte I2C de NCD</i> propose un  connecteur <strong>NCD</strong> qui facilite grandement les raccordements de périphérique I2C.<br />Ce senseur est également disponible sous forme de breakout.</small><br/><br />
      <strong>Testé avec</strong> : FEATHER-ESP8266, PYBOARD<br />
      <strong>Fabricant</strong> : NCD<br />
<ul>
<li>Voir <a href="https://ncd.io/">NCD.io</a></li>
<li>Voir <a href="https://ncd.io/">National Control Device</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../../../tree/master/oled-ssd1306">oled-ssd1306</a></td>
      <td><strong>Composants</strong> : SSD1306, FEATHER-OLED-WING, ADA2900, OLED<br />
      <strong>Interfaces</strong> : I2C, FEATHERWING<br />
<small>Le SSD1306 est un contrôleur d'écran OLED</small><br/><br />
      <strong>Testé avec</strong> : FEATHER-ESP8266<br />
      <strong>Fabricant</strong> : ADAFRUIT<br />
<ul>
<li>Voir <a href="https://shop.mchobby.be/product.php?id_product=879">FeatherWing OLED ssd1306 128x32</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../../../tree/master/pca9536">pca9536</a></td>
      <td><strong>Composants</strong> : PCA9536<br />
      <strong>Interfaces</strong> : I2C<br />
<small>Contrôleur GPIO 4 bits I2C.</small><br/><br />
      <strong>Testé avec</strong> : <br />
      <strong>Fabricant</strong> : NONE<br />
      </td>
  </tr>
  <tr><td><a href="../../../../tree/master/pca9685">pca9685</a></td>
      <td><strong>Composants</strong> : PCA9685, PWM-Driver<br />
      <strong>Interfaces</strong> : I2C<br />
<small>Controleur PWM-Driver à base de PCA9685 de NXP, 16 canaux, résolution 12 bits, pour commande des LEDs ou Servo.</small><br/><br />
      <strong>Testé avec</strong> : PYBOARD<br />
      <strong>Fabricant</strong> : ADAFRUIT<br />
<ul>
<li>Voir <a href="https://shop.mchobby.be/fr/breakout/89-adafruit-controleur-pwm-servo-16-canaux-12-bits-i2c-interface-pca9685-3232100000896-adafruit.html">PCA9685 - PWM Driver @ MCHobby</a></li>
<li>Voir <a href="https://www.adafruit.com/product/815">PCA9685 - PWM Driver @ Adafruit</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../../../tree/master/pcf8523">pcf8523</a></td>
      <td><strong>Composants</strong> : PCF8523<br />
      <strong>Interfaces</strong> : I2C<br />
<small>Une Horloge temps réel RTC + alarme avec MicroPython</small><br/><br />
      <strong>Testé avec</strong> : PYBSTICK<br />
      <strong>Fabricant</strong> : ADAFRUIT<br />
<ul>
<li>Voir <a href="https://shop.mchobby.be/fr/pi-extensions/1148-pirtc-pcf8523-real-time-clock-for-raspberry-pi-3232100011489-adafruit.html">PiRTC (PCF8523) @ MCHobby</a></li>
<li>Voir <a href="https://shop.mchobby.be/fr/feather-adafruit/1056-adalogger-featherwing-rtc-pcf8523-microsd-3232100010567-adafruit.html">Adafruit AdaLogger FeatherWing (PCF8523) @ MCHobby</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../../../tree/master/sht3x">sht3x</a></td>
      <td><strong>Composants</strong> : SHT31-F, SHT3x<br />
      <strong>Interfaces</strong> : I2C<br />
<small>Exploiter un capteur d'humidité SHT3x avec MicroPython</small><br/><br />
      <strong>Testé avec</strong> : PYBOARD, PYBSTICK<br />
      <strong>Fabricant</strong> : DFROBOT<br />
<ul>
<li>Voir <a href="https://shop.mchobby.be/fr/environnemental-press-temp-hrel-gaz/1882-sht31-f-capteur-d-humidite-et-temperature-3232100018822-dfrobot.html">Capteur d'humidité SHT31-F SENS0332 @ MCHobby</a></li>
<li>Voir <a href="https://www.dfrobot.com/product-2015.html">Capteur d'humidité SHT31-F SENS0332 @ DFRobot</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../../../tree/master/tcs34725">tcs34725</a></td>
      <td><strong>Composants</strong> : TCS34725<br />
      <strong>Interfaces</strong> : I2C<br />
<small>Capturer la couleur (rgb ou Kelvin) avec un capteur TCS34725 + LED + filtre IR</small><br/><br />
      <strong>Testé avec</strong> : PYBOARD, FEATHER-ESP8266<br />
      <strong>Fabricant</strong> : ADAFRUIT<br />
<ul>
<li>Voir <a href="https://shop.mchobby.be/fr/afficheur-lcd-tft-oled/475-lcd-16x2-rgb-positif-usb-serie-3232100004757.html">TCS34725 - capteur de couleur RGB + Filtre IR + LED blanche @ MCHobby</a></li>
<li>Voir <a href="https://www.adafruit.com/product/1334">RGB Color Sensor with IR filter and White LED - TCS34725 @ Adafruit</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../../../tree/master/trackball">trackball</a></td>
      <td><strong>Composants</strong> : TRACKBALL-BREAKOUT<br />
      <strong>Interfaces</strong> : I2C<br />
<small>Ajouter un Trackball + LED RGBW sur votre projet MicroPython</small><br/><br />
      <strong>Testé avec</strong> : PYBOARD, PYBSTICK<br />
      <strong>Fabricant</strong> : PIMORONI<br />
<ul>
<li>Voir <a href="https://shop.mchobby.be/fr/tactile-flex-pot-softpad/1833-trackball-i2c-avec-retro-eclairage-3232100018334-pimoroni.html">Trackball I2C avec retro-éclairage @ MCHobby</a></li>
<li>Voir <a href="https://shop.pimoroni.com/products/trackball-breakout">Trackball Breakout @ Pimoroni</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../../../tree/master/tsl2561">tsl2561</a></td>
      <td><strong>Composants</strong> : TSL2561, ADA439<br />
      <strong>Interfaces</strong> : I2C<br />
<small>Le TSL2561 est un senseur de <strong>luminosité</strong> en lumière visible ayant un réponse proche de l'oeil humain. Retourne une valeur en LUX</small><br/><br />
      <strong>Testé avec</strong> : FEATHER-ESP8266<br />
      <strong>Fabricant</strong> : ADAFRUIT<br />
<ul>
<li>Voir <a href="https://shop.mchobby.be/product.php?id_product=238">Capteur Lux/Luminosité/Lumière digital</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../../../tree/master/tsl2591">tsl2591</a></td>
      <td><strong>Composants</strong> : TSL2591, ADA1980<br />
      <strong>Interfaces</strong> : I2C<br />
<small>Le TSL2591 est un capteur de <strong>luminosité</strong> en lumière visible ayant un réponse proche de l'oeil humain. Retourne une valeur en LUX</small><br/><br />
      <strong>Testé avec</strong> : FEATHER-ESP8266, PYBOARD<br />
      <strong>Fabricant</strong> : ADAFRUIT<br />
<ul>
<li>Voir <a href="https://shop.mchobby.be/product.php?id_product=1599">TSL2591 @ MCHobby - Capteur Lux/Luminosité/Lumière digital</a></li>
<li>Voir <a href="https://www.adafruit.com/product/1980">TSL2591 @ Adafruit - Capteur Lux/Luminosité/Lumière digital</a></li>
</ul>
      </td>
  </tr>
</tbody>
</table>

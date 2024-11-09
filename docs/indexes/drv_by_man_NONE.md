# Pilote MicroPython par fabriquant NONE
[Retour à la page principale](../../readme.md)

(other)

voir
[(other)](https://m5stack.com/)
<table>
<thead>
  <th>Répertoire</th><th>Description</th>
</thead>
<tbody>
  <tr><td><a href="../../../../tree/master/dht11">dht11</a></td>
      <td><strong>Composants</strong> : DHT11<br />
      <strong>Interfaces</strong> : GPIO<br />
<small>Le DHT11 est un senseur d'<strong>humidité</strong> (20 à 80%) et température très bon marché.</small><br/><br />
      <strong>Testé avec</strong> : FEATHER-ESP8266<br />
      <strong>Fabricant</strong> : NONE<br />
<ul>
<li>Voir <a href="http://shop.mchobby.be/product.php?id_product=708">DHT11 Sensor</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../../../tree/master/ds18b20">ds18b20</a></td>
      <td><strong>Composants</strong> : DS18B20<br />
      <strong>Interfaces</strong> : ONEWIRE<br />
<small>Le DS18B20 est un capteur de <strong>température</strong> numérique très populaire. Il utilise le bus 1-Wire permettant de brancher plusieurs capteurs 1-Wire sur un même bus.</small><br/><br />
      <strong>Testé avec</strong> : FEATHER-ESP8266, PICO, PYBOARD<br />
      <strong>Fabricant</strong> : NONE<br />
<ul>
<li>Voir <a href="http://shop.mchobby.be/product.php?id_product=259">DS18B20 Sensor</a></li>
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
  <tr><td><a href="../../../../tree/master/fsr-fma-25N">fsr-fma-25N</a></td>
      <td><strong>Composants</strong> : FMAMSDXX005WC2C3, FMAMSDXX015WC2C3, FMAMSDXX025WC2C3<br />
      <strong>Interfaces</strong> : I2C<br />
<small>Utiliser un capteur de Force/Dynamomètre I2C HoneyWell FMAMSDXX025WC2C3.</small><br/><br />
      <strong>Testé avec</strong> : PICO<br />
      <strong>Fabricant</strong> : NONE<br />
<ul>
<li>Voir <a href="https://automation.honeywell.com/us/en/products/sensing-solutions/sensors/force-sensors/microforce-fma-series">Honeywell Force Sensor - MicroForce FMA Series</a></li>
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
  <tr><td><a href="../../../../tree/master/mcp230xx">mcp230xx</a></td>
      <td><strong>Composants</strong> : MCP23017, MCP23008<br />
      <strong>Interfaces</strong> : I2C<br />
<small>Le MCP23017 (et MCP2308) sont des <strong>GPIO Expander</strong> sur bus I2C ajoutant des entrées/sorties sur un microcontrôleur.</small><br/><br />
      <strong>Testé avec</strong> : FEATHER-ESP8266<br />
      <strong>Fabricant</strong> : NONE<br />
<ul>
<li>Voir <a href="http://shop.mchobby.be/product.php?id_product=218">MCP23017 GPIO Expander</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../../../tree/master/mcp23Sxx">mcp23Sxx</a></td>
      <td><strong>Composants</strong> : MCP23S17<br />
      <strong>Interfaces</strong> : SPI<br />
<small>Le MCP23S17 est un <strong>GPIO Expander</strong> sur bus SPI ajoutant des entrées/sorties sur un microcontrôleur.</small><br/><br />
      <strong>Testé avec</strong> : PYBOARD, PYBSTICK<br />
      <strong>Fabricant</strong> : NONE<br />
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
  <tr><td><a href="../../../../tree/master/umqtt">umqtt</a></td>
      <td><strong>Composants</strong> : <br />
      <strong>Interfaces</strong> : <br />
<small>Exemples de communication MQTT avec un module ESP8266.</small><br/><br />
      <strong>Testé avec</strong> : FEATHER-ESP8266, PYBOARD<br />
      <strong>Fabricant</strong> : NONE<br />
<ul>
<li>Voir <a href="https://shop.mchobby.be/product.php?id_product=846">Feather ESP8266</a></li>
</ul>
      </td>
  </tr>
</tbody>
</table>

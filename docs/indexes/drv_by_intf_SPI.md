# Pilote MicroPython pour interface SPI
[Retour à la page principale](../../readme.md)

Bus SPI

<table>
<thead>
  <th>Répertoire</th><th>Description</th>
</thead>
<tbody>
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
  <tr><td><a href="../../../../tree/master/ad9833">ad9833</a></td>
      <td><strong>Composants</strong> : AD9833<br />
      <strong>Interfaces</strong> : SPI<br />
<small>Créer un générateur de signal à l'aide de l AD9833</small><br/><br />
      <strong>Testé avec</strong> : PYBOARD<br />
      <strong>Fabricant</strong> : <br />
<ul>
<li>Voir <a href="https://shop.mchobby.be/fr/breakout/1689-generateur-de-signal-sinus-triangle-clock-0-125-mhz.html">AD9833 - signal generator Sinus, triangle and clock @ MCHobby</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../../../tree/master/dotstar">dotstar</a></td>
      <td><strong>Composants</strong> : DOTSTAR, 74AHCT125, APA102<br />
      <strong>Interfaces</strong> : SPI<br />
<small>Les <strong>DotStar / APA102</strong> sont des LEDs digitales intelligentes pouvant être contrôlées indépendamment les unes des autres.</small><br/><br />
      <strong>Testé avec</strong> : PYBOARD, PYBSTICK<br />
      <strong>Fabricant</strong> : ADAFRUIT<br />
<ul>
<li>Voir <a href="https://shop.mchobby.be/fr/55-neopixels-et-dotstar">APA102 / DotStar</a></li>
<li>Voir <a href="https://shop.mchobby.be/fr/ci/1041-74ahct125-4x-level-shifter-3v-a-5v-3232100010413.html">74AHCT125</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../../../tree/master/lcdspi-lcd12864">lcdspi-lcd12864</a></td>
      <td><strong>Composants</strong> : LCD12864<br />
      <strong>Interfaces</strong> : SPI<br />
<small>Afficheur LCD graphique 128 x 64 pixels. Interface SPI (3 fils)</small><br/><br />
      <strong>Testé avec</strong> : PYBOARD, PYBSTICK, PICO<br />
      <strong>Fabricant</strong> : DFROBOT<br />
<ul>
<li>Voir <a href="https://shop.mchobby.be/fr/gravity-boson/1878-afficheur-lcd-128x64-spi-3-fils-3232100018785-dfrobot.html">LCD12864 (DFR0091) 128x64 graphical LCD display @ MCHobby</a></li>
<li>Voir <a href="https://www.dfrobot.com/product-372.html">LCD12864 (DFR0091) 128x64 graphical LCD display @ DFRobot</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../../../tree/master/max31855">max31855</a></td>
      <td><strong>Composants</strong> : MAX31855<br />
      <strong>Interfaces</strong> : SPI<br />
<small>ThermoCouple Type-K + amplificateur MAX31855 - sous MicroPython</small><br/><br />
      <strong>Testé avec</strong> : PICO<br />
      <strong>Fabricant</strong> : ADAFRUIT<br />
<ul>
<li>Voir <a href="https://shop.mchobby.be/fr/temperature/301-thermocouple-type-k-3232100003019.html">MAX31855 - Amplificateur Thermocouple Type-K via SPI d'Adafruit @ MCHobby</a></li>
<li>Voir <a href="https://www.adafruit.com/product/269">AX31855 - Amplificateur Thermocouple Type-K via SPI d'Adafruit @ Adafruit</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../../../tree/master/max6675">max6675</a></td>
      <td><strong>Composants</strong> : MOD-TC, MAX6675<br />
      <strong>Interfaces</strong> : UEXT, SPI<br />
<small>MAX6675 Amplificateur Thermocouple Type-K - MOD-TC - sous MicroPython</small><br/><br />
      <strong>Testé avec</strong> : PYBOARD<br />
      <strong>Fabricant</strong> : OLIMEX<br />
<ul>
<li>Voir <a href="https://shop.mchobby.be/product.php?id_product=1623">MOD-TC - Amplificateur Thermocouple Type-K d'Olimex @ MCHobby</a></li>
<li>Voir <a href="https://www.olimex.com/Products/Modules/Sensors/MOD-TC">MOD-TC - Amplificateur Thermocouple Type-K @ Olimex</a></li>
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
  <tr><td><a href="../../../../tree/master/mcp2515">mcp2515</a></td>
      <td><strong>Composants</strong> : MCP2515<br />
      <strong>Interfaces</strong> : SPI<br />
<small>Le MCP2515 est un <strong>controleur CAN</strong> sur bus SPI permettant au microcontroleur de se connecter sur un bus CAN.</small><br/><br />
      <strong>Testé avec</strong> : PICO<br />
      <strong>Fabricant</strong> : MCHOBBY<br />
<ul>
<li>Voir <a href="http://shop.mchobby.be/product.php?id_product=2881">CAN-SPI-BRK : CAN bus breakout based on MCP2515 controler</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../../../tree/master/modlcd3310">modlcd3310</a></td>
      <td><strong>Composants</strong> : MOD-LCD3310, PCD8544<br />
      <strong>Interfaces</strong> : SPI, UEXT<br />
<small>MOD-LCD3310 est l'afficheur LCD du Nokia 3310 offrant 84 x 48 pixels et un port de connexion <strong>UEXT</strong>.</small><br/><br />
      <strong>Testé avec</strong> : PYBOARD, PICO<br />
      <strong>Fabricant</strong> : OLIMEX<br />
<ul>
<li>Voir <a href="https://shop.mchobby.be/fr/uext/1867-afficheur-noirblanc-84x48-px-nokia-3310-3232100018679-olimex.html">MOD-LCD3310 @ MCHobby</a></li>
<li>Voir <a href="https://www.olimex.com/Products/Modules/LCD/MOD-LCD3310/open-source-hardware">MOD-LCD3310 @ Olimex</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../../../tree/master/modled8x8">modled8x8</a></td>
      <td><strong>Composants</strong> : MOD-LED8x8RGB<br />
      <strong>Interfaces</strong> : GPIO, SPI<br />
<small>Un afficheur 8x8 LEDs RGB chaînable.</small><br/><br />
      <strong>Testé avec</strong> : PYBOARD<br />
      <strong>Fabricant</strong> : OLIMEX<br />
<ul>
<li>Voir <a href="https://shop.mchobby.be/fr/nouveaute/1625-mod-led8x8rgb-matrice-led-rgb-8x8-3232100016255-olimex.html">MOD-LED8x8RGB @ MCHobby</a></li>
<li>Voir <a href="https://www.olimex.com/Products/Modules/LED/MOD-LED8x8RGB/open-source-hardware">MOD-LED8x8RGB @ Olimex</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../../../tree/master/rfm69">rfm69</a></td>
      <td><strong>Composants</strong> : RFM69, RFM69HCW<br />
      <strong>Interfaces</strong> : SPI<br />
<small>Utiliser module Packet Radio RFM69HCW (SPI) avec MicroPython</small><br/><br />
      <strong>Testé avec</strong> : PICO<br />
      <strong>Fabricant</strong> : ADAFRUIT<br />
<ul>
<li>Voir <a href="https://shop.mchobby.be/product.php?id_product=1390">Breakout RFM69HCW Transpondeur Radio - 433 MHz - RadioFruit @ MCHobby</a></li>
<li>Voir <a href="https://www.adafruit.com/product/3071">RFM69HCW radio transceiver breakout - 433 MHz - RadioFruit @ Adafruit</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../../../tree/master/st7687s">st7687s</a></td>
      <td><strong>Composants</strong> : ST7687S<br />
      <strong>Interfaces</strong> : SPI<br />
<small>Exploiter un TFT rond avec MicroPython</small><br/><br />
      <strong>Testé avec</strong> : PYBOARD, PYBSTICK<br />
      <strong>Fabricant</strong> : DFROBOT<br />
<ul>
<li>Voir <a href="https://shop.mchobby.be/fr/afficheur-lcd-tft-oled/1856-tft-couleur-22-rond-spi-breakout-3232100018563-dfrobot.html">Ecran TFT DFRobot DFR0529 @ MCHobby</a></li>
<li>Voir <a href="https://www.dfrobot.com/product-1794.html">Ecran TFT DFRobot DFR0529 @ DFRobot</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../../../tree/master/stmpe610">stmpe610</a></td>
      <td><strong>Composants</strong> : STMPE610<br />
      <strong>Interfaces</strong> : SPI<br />
<small>Utiliser un capteur tactile résistif avec MicroPython</small><br/><br />
      <strong>Testé avec</strong> : PICO<br />
      <strong>Fabricant</strong> : <br />
<ul>
<li>Voir <a href="https://shop.mchobby.be/fr/feather-adafruit/1050-tft-featherwing-24-touch-320x240-3232100010505-adafruit.html">Ecran FeatherWing TFT 2.4 Adafruit @ MCHobby</a></li>
</ul>
      </td>
  </tr>
  <tr><td><a href="../../../../tree/master/winbond">winbond</a></td>
      <td><strong>Composants</strong> : W25Qxx, FLASH<br />
      <strong>Interfaces</strong> : SPI<br />
<small>Utiliser une mémoire Flash QSPI avec MicroPython (en SPI)</small><br/><br />
      <strong>Testé avec</strong> : PICO<br />
      <strong>Fabricant</strong> : <br />
<ul>
<li>Voir <a href="https://www.digikey.be/fr/products/detail/winbond-electronics/W25Q128JVSIQ/5803943">W25Q128JVSIQ @ Digikey</a></li>
</ul>
      </td>
  </tr>
</tbody>
</table>

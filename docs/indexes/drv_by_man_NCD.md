# Pilote MicroPython par fabriquant NCD
[Retour à la page principale](../../readme.md)

National Control Device

voir
[National Control Device](https://ncd.io/)
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
</tbody>
</table>

# Pilote ILI9341/ILI9340 générique pour différent TFT - No FrameBuffer

__<<<=== CE PILOTE EST EN COURS DE REALISATION ===>>>__

![Adafruit 2.4" TFT FeatherWing](docs/_static/tft-wing-00.jpg)

Ce pilote:
* permet de contrôler des écrans à base de contrôleur ILI9341 / ILI9340
* effectue les opérations directement dans la mémoire du contrôleur ILIxxxx.
* __Ne dérive pas de FrameBuffer!__

Le bibliothèque [ili934x](lib/ili934x.py) expose une interface __imitant__ l'[API de FrameBuffer](http://docs.micropython.org/en/latest/library/framebuf.html?highlight=framebufer) de MicroPython. Le but est de pouvoir utiliser ce pilote comme si c'était un FrameBuffer.

L'__API du pilote ILI934x__ [est détaillée dans API.md](api.md)

## Crédit:
Ce pilote est basé sur les travaux suivants:
* [Micropython Driver for ILI9341 display de Jeffmer](https://github.com/jeffmer/micropython-ili9341) (GitHub)
* [Micropython Driver for ILI9341 de Ropod](https://github.com/mchobby/pyboard_drive/tree/master/ILI9341) (GitHub)
* [FreeType generator (binary font file for MicroControler)](https://github.com/mchobby/freetype-generator) (GitHub)

# Brancher

## PYBStick - PYBStick + Feather-Face


``` python
spi = SPI( 1, baudrate=40000000 )
cs_pin = Pin("S15")
dc_pin = Pin("S13")
rst_pin = None

display = ILI9341( spi, cs=cs_pin, dc=dc_pin, rst=rst_pin, w=320, h=240, r=3)
```

# Tester

xxx

# Resources

* [ILI9341 Datasheet](https://cdn-shop.adafruit.com/datasheets/ILI9341.pdf) _stored at Adafruit Industries_

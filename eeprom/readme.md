# Utiliser une EEPROM T24Cxxx ou 24Cxx avec MicroPython

Le T24Cxxx est une EEPROM I2C de Peas semiconductor.

Le 24Cxxx est une EEPROM I2C de MicroChip semiconductor.

![EEProm](docs/_static/t24cxx.jpg)

Ces modules I2C peuvent stocker quelques 10 d'octets voir plusieurs dizaines de KiloOctets selon les modèles disponibles.

Dans les deux cas, l'adresse par défaut du module est 0x50.

## Credit

Cette bibliothèque est basée sur le [code source EEPROM.py proposé sur le GitHub de MicroPython](https://raw.githubusercontent.com/dda/MicroPython/master/EEPROM.py) .

# Brancher

TODO

# Tester

Il est nécessaire de copier les bibliothèques adéquate sur la carte MicroPython pour pouvoir tester les différents scripts.

* `mcp24cxx.py` pour les modules EEPROM 24Cxxx produit par MicroChip.
* `t24cxx.py` pour les modules EEPROM T24Cxx produit pas peas semiconductor.

Le script [test_mcp24c02c_read.py](examples/test_mcp24c02c_read.py) présenté ci-dessous lit les 256 octets présents dans une EEPROM 24C02C (256 octets) produit par MicroChip.

```
from machine import I2C
from mcp24cxx import MCP24Cxx, CHIP_MCP24C02C

i2c = I2C( 2 )

eeprom = MCP24Cxx( i2c, addr=0x50, chip=CHIP_MCP24C02C ) # 256 octets

# Addresse de 0 à 255
for mem_addr in range( 256 ):
	data = eeprom.read( mem_addr ) # Lecture de 1 octets
	print( "0x%2s = %s" % ( hex(mem_addr), data[0]) )
```

Ce qui produit:

```
0x0x0 = 255
0x0x1 = 255
0x0x2 = 255
...
0x0xf5 = 178
0x0xf6 = 64
0x0xf7 = 213
0x0xf8 = 0
0x0xf9 = 0
0x0xfa = 0
0x0xfb = 0
0x0xfc = 0
0x0xfd = 0
0x0xfe = 0
0x0xff = 0
```

# TCA9554A - 8 bits GPIO Expander via I2C

Le TCA9554A de Texas Instrument permet d'ajouter 8 entrées/sorties avec une sortie d'interruption et registres de configuration.

![TCA9554A brochage](docs/_static/tca9554a.jpg)

Ce composant:
* fonctionne avec une tension logique de 1.65V à 5.5V.
* dispose de 3 bits d'adresse (0x38 par défaut).
* dispose d'une configuration "polarity" (pour inverser la polarité d'une broche)
* active une résistance pull-up de 100 KOhms sur les broches en entrées.

Voir la [fiche technique tu TCA9554A](https://www.ti.com/lit/gpn/tca9554a) pour plus d'information.

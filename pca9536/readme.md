[This file also exists in ENGLISH](readme_ENG.md)

# PCA9536 - Extension GPIO 4 Bits, bus I2C

![Brochage PCA9536](docs/_static/pca9536-pinout.png)

Le PCA9536 est un composant à 8 broches (tolérant 5V) qui offre un GPIO (General Purpose parallel Input/Output) sur 4 bits.

Le PCA9536 est utilisé comme interface I2C sur certaines cartes d'extension. Cette section du GitHub ne contient que le pilote et quelques exemples.

Vous trouverez ci-dessous un exemple d'utilisation du PCA9536.

![Utilisation PCA9536](docs/_static/pca9536-usecase.png)

__Le PCA9536 a une fonctionnalité très particulière__ avec une résistance pull-up interne de 100 kΩ (non désactivable!) sur les broches d'entrées.

La fonctionnalité "_power-on_" initialise les registres et leurs valeurs par défaut et initialise la machine a état fini.

Caractéristiques principales:
* [fiche technique du PCA9536](https://www.nxp.com/products/analog/interfaces/ic-bus/ic-general-purpose-i-o/4-bit-i2c-bus-and-smbus-i-o-port:PCA9536)
* GPIO 4-bits sur I2C (fréquence d'horloge de 0 Hz à 400 kHz)
* Tension d'alimentation de l'ordre de 2.3 V à 5.5 V
* I/O tolérant 5V
* Registre d'inversion de polarité (_Polarity Inversion register_)
* Faible courant en mode veille
* Pas de parasite à la mise sous tension
* _Power-on reset_ interne
* 4 broches I/O pins configurée par défaut en 4 entrées avec résistance pull-up interne de 100 kΩ.
* Protection ESD protection excédent 2000 V
* Latch-up testing is done to JEDEC Standard JESD78 which exceeds 100 mA

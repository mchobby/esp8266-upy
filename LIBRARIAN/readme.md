[This file also exists in ENGLISH](readme_ENG.md)

# Librarian

Collection de fonction, classes et utilitaires, ... utiles pour le développement

N'hésitez pas à consulter le contenu des bibliothèques et ressources pour plus d'informations.

# Installer les bibliothèques

La bibliothèque doit être copiée sur la carte MicroPython avant d'utiliser les examples.

On a WiFi capable plateform:

```
>>> import mip
>>> mip.install("github:mchobby/esp8266-upy/LIBRARIAN")
```

Ou via l'utilitaire mpremote :

```
mpremote mip install github:mchobby/esp8266-upy/LIBRARIAN
```

# Bibliothèques

* [hyst.py](lib/hyst.py) : Cycle avec hystéresis pour thermostat, voir [ce readme specifique](hyst_readme.md)
* [lfpwm.py](lib/lfpwm.py) : Low Frequency PWM signal (utilisé avec les système a très grande inertie), voir [ce readme spécifique](lfpwm_readme.md).
* [maps.py](lib/maps.py) : equivalent du `map()` Arduino (compatible float), `ranking()`, etc. voir [ce readme specifique](maps_readme.md)
* [ostls.py](lib/ostls.py) : "os tools" quelques fonctions pratiques autour du module `os`.
* [pid.py](lib/pid.py) : PID logiciel
* [ringbuf.py](lib/ringbuf.py) : Ring buffer implementation
* [rp2lib/](rp2lib/) : Ensemble de bibliothèques PIO pour Raspberry-Pi Pico RP2 series, voir [ce readme spécifique](rp2lib_readme.md).

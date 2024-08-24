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

* [ostls.py](lib/ostls.py) : "os tools" quelques fonctions pratiques autour du module `os`.
* [maps.py](lib/maps.py) : equivalent of Arduino `map()` (float compatible)
* [ringbuf.py](lib/ringbuf.py) : Ring buffer implementation

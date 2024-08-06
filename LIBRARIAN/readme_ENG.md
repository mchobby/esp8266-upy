[Ce fichier existe également en FRANCAIS](readme.md)

# Librarian

Collection of useful functions, classes, utilities, ... for development

Do not hesitate to browse the libraries and ressources for more information.

# Intall libraries

The library must be copied on the MicroPython board before using the examples.

On a WiFi capable plateform:

```
>>> import mip
>>> mip.install("github:mchobby/esp8266-upy/LIBRARIAN")
```

Or via the mpremote utility :

```
mpremote mip install github:mchobby/esp8266-upy/LIBRARIAN
```

# Libraries

* [maps.py](lib/maps.py) : equivalent of Arduino `map()` (float compatible)
* [ringbuf.py](lib/ringbuf.py) : Ring buffer implementation

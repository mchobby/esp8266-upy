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

* [ostls.py](lib/ostls.py) : "os tools" some useful functions relatives to os module.
* [maps.py](lib/maps.py) : equivalent of Arduino `map()` (float compatible)
* [ringbuf.py](lib/ringbuf.py) : Ring buffer implementation
* [lfpwm.py](lib/lfpwm.py) : Low Frequency PWM signal (used in system with very high inertia), see [this specific readme](lfpwm_readme.md).
* [rp2lib/](rp2lib/) : set of PIO library for Raspberry-Pi Pico RP2 series, see [this specific readme](rp2lib_readme.md).

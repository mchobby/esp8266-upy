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

* [hyst.py](lib/hyst.py) : Hysteresis cycling for thermostat, see [this specific readme](hyst_readme.md)
* [lfpwm.py](lib/lfpwm.py) : Low Frequency PWM signal (used in system with very high inertia), see [this specific readme](lfpwm_readme.md).
* [ledtls.py](lib/ledtls.py) : `LedError`, `Pulse`, `HeartBeat` classes for LED control. `SuperLed` can even use several modes on a single LED. See examples.
* [maps.py](lib/maps.py) : equivalent of Arduino `map()` (float compatible), `ranking()`, etc. See [this specific readme](maps_readme.md)
* [ostls.py](lib/ostls.py) : "os tools" some useful functions relatives to os module.
* [timetls.py](lib/timetls.py) : `TimeOutTimer` class to measure check when the processing time exceed a timeout.
* [pid.py](lib/pid.py) : Software PID
* [ringbuf.py](lib/ringbuf.py) : Ring buffer implementation
* [rp2lib/](rp2lib/) : set of PIO library for Raspberry-Pi Pico RP2 series, see [this specific readme](rp2lib_readme.md).
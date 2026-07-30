[This file also exists in ENGLISH](readme_ENG.md)

# PCF8523 : Horloge RTC pour MicroPython

Le PCF8523 de NXP est une horloge RTC I2C capable de poursuivre l'écoulement du temps même lorsque qu'elle n'est pas sous-tension. En effet, la pile bouton permet à l'horloge de continuer à fonctionner.

Le PCF8523 est assez populaire et équipe de nombreux produits, la capture ci-dessous reprend le [Pico-Clock-Boot](https://shop.mchobby.be/fr/pico-rp2x/2960-pico-clock-boot-carte-horloge-rtc-pcf8523-pour-raspberry-pico-3232100029606.html), le [Pico-DataLogger-Boot](https://shop.mchobby.be/fr/pico-rp2x/2912-carte-data-logger-pour-raspberry-pi-pico-3232100029125.html) 

![Exemple d'horloge PCF8523](docs/_static/pcf8523_sample2.jpg)

ainsi que la [PiRTC](https://shop.mchobby.be/fr/pi-extensions/1148-pirtc-pcf8523-real-time-clock-for-raspberry-pi-3232100011489-adafruit.html) et l'[Adafruit AdaLogger FeatherWing](https://shop.mchobby.be/fr/feather-adafruit/1056-adalogger-featherwing-rtc-pcf8523-microsd-3232100010567-adafruit.html).

![Exemple d'horloge PCF8523](docs/_static/pcf8523_sample.jpg)

L'horloge PCF8523 dispose aussi de quelques fonctionnalités intéressantes:
* Détection de batterie faible
* Détection de perte d'alimentation (changement de pile)
* __Alarme configurable__
* détection logiciel d'alarme.
* activation d'un signal d'interruption sur alarme.

Le signal d'interruption est particulièrement intéressant car il permet d'activer/réveiller un microcontrôleur à intervalle régulier.

# Library

The library must be copied on the MicroPython board before using the examples.

On a WiFi capable plateform:

```
>>> import mip
>>> mip.install("github:mchobby/esp8266-upy/pcf8523")
```

Or via the mpremote utility :

```
mpremote mip install github:mchobby/esp8266-upy/pcf8523
```

# Brancher

## Avec la PYBStick

![Brancher un Feather AdaLogger (PCF8523) branché sur PYBStick](docs/_static/pcf8523-to-pybstick.jpg)

## Avec la Raspberry-Pi Pico

![Brancher un Feather AdaLogger (PCF8523) branché sur Raspberry-Pi Pico](docs/_static/pcf8523-to-pico.jpg)

![Brancher un PCF8523 RTC breakout sur Raspberry-Pi Pico](docs/_static/pcf8523-brk-to-pico.jpg)


# Test

Avant de pouvoir utiliser les scripts d'exemples, il est nécessaire de copier la bibliothèque `pcf8523.py` sur la carte MicroPython.

__A propos des exemples:__

Le sous-répertoire `examples` contient des scripts d'exemples abondamment commentés.

Il est vivement recommandé de les consulter pour avoir une idée des toutes les fonctionnalités disponibles.

## Fixer l'heure

Avant de pouvoir utiliser l'horloge RTC, il est nécessaire d'initialiser l'heure de l'horloge.

Le code suivant est issu de l'exemple [test_setdate.py](examples/test_setdate.py) .

```
from machine import I2C, Pin
from pcf8523 import PCF8523
import time

DAY_NAMES = ['monday','tuesday', 'wednesday', 'thursday', 'friday', 'saterday', 'sunday' ]

# PYBStick - S3=sda, S5=scl
# Raspberry-Pi Pico - GP6=sda, GP7=scl
i2c = I2C(1, sda=Pin(6), scl=Pin(7))
pcf_rtc = PCF8523( i2c )

# Year: 2020, month: 6, day: 22, hour: 0, min: 14, sec: 6, weekday: 0 (monday), yearday: 174
# yearday can be set to 0 when setting the date... it will be recomputed
pcf_rtc.datetime = (2020, 6, 22, 0, 0, 14, 6, 0)
time.sleep(1)

# Reread as datetime
print( "y/m/d weekday h:m:s.ms =>", pcf_rtc.datetime )

# Reread as timestamp
_time = pcf_rtc.timestamp
print( "Time: %s secs" % _time )
print( "Year: %s, month: %s, day: %s, hour: %s, min: %s, sec: %s, weekday: %s, yearday: %s" % time.localtime(_time) )
weekday = time.localtime(_time)[6]
print( 'Day of week: %s' % DAY_NAMES[weekday] )
```

## Lire l'heure

Le code suivant permet de lire l'heure stockée dans l'horloge.

Voir le script [test_getdate.py](examples/test_getdate.py) .

```
from machine import I2C, Pin
from pcf8523 import PCF8523
import time
DAY_NAMES = ['monday','tuesday', 'wednesday', 'thursday', 'friday', 'saterday', 'sunday' ]

# PYBStick - S3=sda, S5=scl
# Raspberry-Pi Pico - GP6=sda, GP7=scl
i2c = I2C(1, sda=Pin(6), scl=Pin(7))

pcf_rtc = PCF8523( i2c )

_dt = pcf_rtc.datetime
print( "y/m/d weekday h:m:s.ms =>", _dt )
print( "Day of Week:", DAY_NAMES[_dt[3]])

_time = pcf_rtc.timestamp
print( "Time: %s secs" % _time )
print( "Year: %s, month: %s, day: %s, hour: %s, min: %s, sec: %s, weekday: %s, yearday: %s" % time.localtime(_time) )
weekday = time.localtime(_time)[6]
print( 'Day of week: %s' % DAY_NAMES[weekday] )
```

## Test d'alarme

La RTC dispose d'une fonction permettant d'activer une alarme (registre ou broche d'interruption)
lorsque les conditions d'alarmes sont rencontrées.

La condition d'alarme peut être composer d'un (ou plusieurs) des critères suivants:
* Jour de la semaine (0=lundi, 6=dimanche)
* Jour du mois
* Heure
* Minute

Lorsque plusieurs éléments sont utilisés pour l'alarme, la condition doit être rencontrée pour tous les critères en même temps.

Le script [test_alarm.py](examples/test_alarm.py) repris ci-dessous indique comment activer l'alarme toutes les heures.

Pour ne pas faire trop attendre l'utilisateur, le script déclenche l'alarme une minute après le démarrage du script
```
from machine import I2C, Pin
from pcf8523 import PCF8523
import time

# PYBStick - S3=sda, S5=scl
# Raspberry-Pi Pico - GP6=sda, GP7=scl
i2c = I2C(1, sda=Pin(6), scl=Pin(7))

rtc = PCF8523( i2c )

# Get the current datetime as timestamp
now = rtc.timestamp
print( "now   @ Year: %s, month: %s, day: %s, hour: %s, min: %s, sec: %s, weekday: %s, yearday: %s" % time.localtime(now) )

# Calculate Alarm 1 minute in the future
alarm_time = now + 60
alarm_tuple = time.localtime(alarm_time) # Year, month, day, hour, min, sec, weekday, yearday
alarm_minutes = alarm_tuple[4]

# set the alarm for activerate every hour & <alarm_min>
rtc.alarm_weekday( enable=False )
rtc.alarm_day    ( enable=False )
rtc.alarm_hour   ( enable=False )
rtc.alarm_min( alarm_minutes, True )

# set the alarm for activerate every day at 6:30
# rtc.alarm_weekday( enable=False )
# rtc.alarm_day    ( enable=False )
# rtc.alarm_hour   (  6, True )
# rtc.alarm_min    ( 30, True )

# set the alarm for activerate every monday at 8:00
# rtc.alarm_weekday(  1, True ) # 0 = Sunday
# rtc.alarm_day    ( enable=False )
# rtc.alarm_hour   (  8, True )
# rtc.alarm_min    (  0, True )

# Re-read alarm setting
print( "alarm_wday:", rtc.alarm_weekday() )
print( "alarm_day :", rtc.alarm_day() )
print( "alarm_hour:", rtc.alarm_hour() )
print( "alarm_min :", rtc.alarm_min() )

# Activate PCF8523 interrupt pin on alarm. Quite handy to wake-up a microcontroler
#  Interrupt pin goes to 3.3V on alarm
#rtc.alarm_interrupt = True

counter = 0
while True:
	counter += 1
	print('Testing alarm status, pass %i' % counter )
	if rtc.alarm_status:
		print( "Alarm catched!")
		print( "Tuuut Tuuut Tuuut Tuuut Tuuut Tuuut")
		print( "Reset alarm status ")
		rtc.alarm_status = False
		break
	time.sleep( 10 )


print( "That s all Folks!" )
```

Ce qui affiche les messages suivants:

```
$ mpremote run examples/test_alarm.py 
now   @ Year: 2026, month: 7, day: 30, hour: 1, min: 29, sec: 42, weekday: 3, yearday: 211
alarm_wday: (0, False)
alarm_day : (0, False)
alarm_hour: (0, False)
alarm_min : (30, True)
Testing alarm status, pass 1
Testing alarm status, pass 2
Testing alarm status, pass 3
Alarm catched!
Tuuut Tuuut Tuuut Tuuut Tuuut Tuuut
Reset alarm status 
That s all Folks!
```

__Remarque:__ il est possible d'activer l'interruption sur alarme avec l'instruction `rtc.alarm_interrupt = True` .

# Où acheter
* [Pico-Clock-Boot](https://shop.mchobby.be/fr/pico-rp2x/2960-pico-clock-boot-carte-horloge-rtc-pcf8523-pour-raspberry-pico-3232100029606.html) pour Raspberry-Pi Pico
* [Pico-DataLogger-Boot](https://shop.mchobby.be/fr/pico-rp2x/2912-carte-data-logger-pour-raspberry-pi-pico-3232100029125.html) pour Raspberry-Pi Pico
* [Carte PYBStick](https://shop.mchobby.be/fr/recherche?controller=search&orderby=position&orderway=desc&search_query=pybstick&submit_search=)
* [Carte Raspberry-Pi Pico](https://shop.mchobby.be/fr/157-pico-rp2040)
* [PiRTC (PCF8523)](https://shop.mchobby.be/fr/pi-extensions/1148-pirtc-pcf8523-real-time-clock-for-raspberry-pi-3232100011489-adafruit.html) @ MC Hobby
* [Adafruit AdaLogger FeatherWing (PCF8523)](https://shop.mchobby.be/fr/feather-adafruit/1056-adalogger-featherwing-rtc-pcf8523-microsd-3232100010567-adafruit.html) @ MC Hobby

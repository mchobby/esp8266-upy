# Client MQTT sur ESP8266 en MicroPython

Ce document contient des notes concernant la création d'un client MQTT sur ESP8266 en MicroPython.

# Installer la bibliothèque 
La biblothèque n'a pas besoin d'être installée sur ESP8266, elle est déjà disponible dans le firmware MicroPython

from umqtt.simple import MQTTClient

Sinon, sur d'autre plateforme, vous pourriez copier le fichier simple.py de l'archive umqtt.simple (également disponible dans ce répertoire) sur votre ESP8266. La section ressource contient également des références vers des releases officielles.

# Installer Mosquitto Client
Les utilisateur de machine Linux pourront utiliser le broker et les applications  clientes Mosquitto.
* __Mosquitto Client__ propose des utilitaires clients pour le MQTT mosquitto.
* __Mosquitto__ propose également un broker MQTT de test sur test.mosquitto.org 

sudo apt-get install mosquitto-clients

Par exemple, vous pourrez surveiller le topic "domeu" à l'aide de la commande suivante:

```
mosquitto_sub -h test.mosquitto.org -t "domeu/#" -v
```

# Raccordement

Aucun concernant ce tuto.

# Code de test ESP8266 - Publisher

```
>>> from umqtt.simple import MQTTClient
>>> q = MQTTClient( client_id = 'abc', server = 'test.mosquitto.org' )
>>> q.connect()
0
>>> # MQTT n'envoi que des données au format texte
>>> # L'envoi d'un entier provoquera une erreur.
>>> q.publish( 'domeu/test', 120 )
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "simple.py", line 110, in publish
TypeError: object of type 'int' has no len()
>>> #
>>> # La publication de valeur texte que l'on pourra 
>>> # constater en démarrant une souscription avec
>>> # mosquitto_sub (voir ci-dessous).
>>> # 
>>> q.publish( 'domeu/test', '120' )
>>> q.publish( 'domeu/test', '121' )
>>> q.publish( 'domeu/test', '122' )
>>> q.publish( 'domeu/test', 'impressionnant' )
>>> q.publish( 'domeu/test/hello', 'impressionnant' )
>>> q.disconnect()
```

Ce qui produit le résultat suivant sur le subscriber démarré avec la commande suivante (il faut démarrer la souscription avant d'exécuter les instructions `q.publish(...)`

```
mosquitto_sub -h test.mosquitto.org -t "domeu/#" -v
```

La souscription produira le résultat suivant :

```
domeu/test 120
domeu/test 121
domeu/test 122
domeu/test/hello impressionnant
```

# Code de test ESP8266 - Subscriber

```
>>> from umqtt.simple import MQTTClient
>>> q = MQTTClient( client_id = 'abc', server = 'test.mosquitto.org' )
>>> q.connect()
0
>>> def notify_me( topic, msg ):
...     print( topic )
...     print( msg )
...     
...     
... 
>>> q.set_callback( notify_me )
>>> q.subscribe( 'domeu' )
```

ce qui produirait le résultat suivant sur l'esp8266 ....

```
>>> q.wait_msg()
b'domeu'
b'test'
>>> q.wait_msg()
b'domeu'
b'120'
>>> q.wait_msg()
b'domeu'
b'125'
>>> 
```

...en utilisant les commandes de publication suivantes sur une machine Linux :


```
$ mosquitto_pub -h test.mosquitto.org -t "domeu" -m "test"
$ mosquitto_pub -h test.mosquitto.org -t "domeu" -m "120"
$ mosquitto_pub -h test.mosquitto.org -t "domeu" -m "125"
```

# Ressources

Vous pouvez consulter la bibliothèque micropython-umqtt.simple 1.3.3 que vous trouverez sur pypi.
* [Release officielle MQTT](https://github.com/micropython/micropython-lib/tree/master/umqtt.simple)
* [umqtt.simple sur pypi](https://pypi.python.org/pypi/micropython-umqtt.simple)



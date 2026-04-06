[This file also exists in ENGLISH](btntls_readme_ENG.md)

# Bibliothèques btntls

La bibliothèque [btntls.py](lib/btntls.py) propose des functions et classes relatives à l'implementation de 
fonctionnalités autour des boutons.

# classe BtnClicks
La classe `BtnClicks` est utilisée pour compter le nombre de pressions consécutives sur un bouton.

`BtnClicks` met en place un déparasitage logiciel (25ms) et prévoit aussi un temps minimum
 (250ms, configurable) pour détecter une pression subsequente sur le bouton. Enfin le compte 
 de pressions sur le bouton est disponible après un temps de déclenchement (1000ms, configurable) 
 après la dernière pression sur le bouton.

`BtnClicks` met le compte de pressions à disposition sur la propriété `count`, uniquement après 
le temps de déclenchement (trigger_timeout). Dans le cas contraire la propriété retourne `None`.

Une fois que le compte de pressions est disponible, la lecture du compte est unique. Juste 
après, la valeur retournée sera a nouveau `None`.

__Notes Importantes:__
* La classe active la résistance pull-up de la broche. Le bouton enfoncé place donc la broche à la masse.
* La classe utilise le mecanisme d'interruption pour capturer les pressions sur le bouton.

``` python
import micropython
import time
from btntls import BtnClicks

# because ClickBtn use IRQ
micropython.alloc_emergency_exception_buf(100)

btn_mode = BtnClicks( 17 ) # Bouton branché sur broche 17
btn_both = BtnClicks( 18 ) # Bouton branché sur broche 18

while True:
	_m = btn_mode.count
	_b = btn_both.count
	if (_m==None) and (_b==None):
		time.sleep_ms( 10 )
		continue
	if _m:
		print( "Mode was pressed %i times" % _m)
	if _b:
		print( "Both was pressed %i times" % _b )
```

Ce qui affiche le résultat en fonction de la pression sur le bouton

```
Both was pressed 2 times
Mode was pressed 1 times
Mode was pressed 3 times
Both was pressed 1 times
Both was pressed 5 times
Mode was pressed 1 times
Mode was pressed 1 times
Both was pressed 4 times
```


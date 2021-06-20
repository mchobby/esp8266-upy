[This file also exists in ENGLISH](readme_ENG.md)

# FrameBuffer GFX - Utilitaires pour FrameBuffer
Cette section contient des classes et exemples permettant manipuler le contenu de FrameBuffer.

* __[fbutil.py](lib/fbutil.py)__ :  circle, fill_circle, oval, fill_oval, rrect, fill_rrect, etc. Exemple: [ici](https://github.com/mchobby/esp8266-upy/tree/master/ili934x/examples/fbutil)
* __[icon.py](lib/icon.py)__ :  définition d'icone du Micro:bit en 5x5 (provient du projet sense-hat).

# Dessiner une icone dans un FrameBuffer

``` python
def icon( fb, icon, x=1, y=1, color=0x7BEF ):
  """ Affiche un icone dans le FrameBuffer fb à la poistion x,y avec la couleur C.
      Les icones sont stockées dans le fichier icons.py . Dessine uniquement les Pixels (ne les effaces pas) """
  size = icon[0]
  for row in range( size ):
    for col in range( size ):
      if (icon[row+1] & (1<<col)) > 0:
        fb.pixel(col+y,row+y,color)
```



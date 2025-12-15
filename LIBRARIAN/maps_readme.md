[This file also exists in ENGLISH](maps_readme_ENG.md)

# Bibliothèques maps

La bibliothèque [maps.py](lib/maps.py) propose des functions permettant d'implémenter facilement des traitement d'interpolation, de catégorisation et autres.

# fonction map()
La fonction `map()` est utilisée pour effectuer une interpolation linéaire entre deux valeurs. `maps()` retourne un float qui peut éventuellement être transformé en entier en réalisant un casting avec `int()`.
``` python
def map(value, istart, istop, ostart, ostop):
```

avec:

* __value__ : valeur d'entrée (entier ou float) située entre un minimum `istart` et un maximum `istop`.
* __istart__ : valeur minimale de la plage d'entrée (entier ou float).
* __istop__ : valeur maximale de la plage d'entrée (entier ou float).
* __ostart__ : borne inférieure de la valeur de sortie (entier ou float).
* __ostop__ : borne supérieur de la valeur de sortie (entier ou float).

retourne:

La fonction retourne la valeur de sortie (float) correspondant à la valeur d'entrée `value`

# fonction ranking()
La fonction `ranking()` permet de catégoriser facilement une valeur d'entrée parmi une liste de valeurs précisée dans `ranges`. La fonction permet également de transposer la valeur catégorisée avec une des valeurs de sortie mentionnées dans `transposed` (si celui-ci est défini).

``` python
def ranking( value, ranges, transposed=None ):
```

avec:

* __value__ : valeur comparée aux différents intervalles. Lorsqu'une valeur tombe dans un intervalle, la limite inférieure de celui-ci est retourné (ou valeur transposée correspondante). `None` est retourné si `value` est en dessous du premier intervalle.
* __ranges__ : liste des valeurs croissantes définissant les n intervalles.
* __transposed__ : (optionnel) liste des valeurs transposées correspondant à aux intervalles. Si définit c'est la valeur transposée qui est retournée n lieu et place de la borne inférieure de l'intervalle.

retourne:

La borne inférieure de l'intervalle dans lequel la valeur `value` tombe ou `None`. Si une liste de valeurs transposée existe alors le résultat (borne inférieure) est extrait de la liste `transposed` avant d'être retourné

Exemple:
```
result = ranking( val, [10,20,30,40] )
```

* retourne None si val < 10
* retourne 10 si val>= 10 et val < 20
* retourne 20 si val>= 20 et val < 30
* retourne 30 si val>= 30 et val < 40
* retourne 40 si val>= 40

```
result = ranking( val, [10,20,30,40], ["A", "B", "C", "D"] )
```

* retourne None si val < 10
* retourne "A" si val>= 10 et val < 20
* retourne "B" si val>= 20 et val < 30
* retourne "C" si val>= 30 et val < 40
* retourne "D" si val>= 40

remarks: l'appel pourrait également être écrit `result = ranking( val, [10,20,30,40], "ABCD" )`

# fonction slice_by()
La fonction `slice_by()` permet diviser un liste en sous-listes de N éléments.

``` python
def slice_by( lst, by_len ):
```

avec:

* __lst__ : la liste source.
* __by_len__ : le nombre d'élément dans chaque sous-liste.


Exemple:
``` python
from maps import slice_by

l = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26]
print( "slice by 5", slice_by(l,5) )
```

ce qui affiche le resultat suivant:

```
slice by 5 [[1, 2, 3, 4, 5], [6, 7, 8, 9, 10], [11, 12, 13, 14, 15], [16, 17, 18, 19, 20], [21, 22, 23, 24, 25], [26]]
```
[Ce fichier existe également en FRANCAIS](maps_readme.md)

# maps library

The [maps.py](lib/maps.py) library offers functions allowing the quick implementation of interpolation, category selection, etc.

# map() function
The `map()` function is used to perform linear interpolation between two ranges of values. `maps()` return a float that can be casted to integer with `int()`.
``` python
def map(value, istart, istop, ostart, ostop):
```

With:

* __value__ : input value (integer or float) between the minimum `istart` and the maximum `istop`.
* __istart__ : minimal value of the input range (integer or float).
* __istop__ : maximal value of the input range (integer or float).
* __ostart__ : lower limit of the output value (integer or float).
* __ostop__ : upper limit of the output value (integer or float).

Returns:

The function returns the output value (float) corresponding to the input  `value`

# ranking() function
The `ranking()` function allows you to easily categorize an input value among a list of ​​specified `ranges` values. The function also allows you to transpose the categorized value to one of the output values ​​specified in `transposed` list (if defined).

``` python
def ranking( value, ranges, transposed=None ):
```

with:

* __value__ : value compared to various intervals. When a value falls within an interval, the lower limit of the interval is returned by the function. If transposed is defined then the corresponding transposed value is returned instead. `None` is resturned when `value` is below the lower interval.
* __ranges__ : listelist of increasing values ​​defining the n intervals des valeurs croissantes définissant les n intervalles.
* __transposed__ : (optional) list of transposed values ​​corresponding to the intervals. If defined, the transposed value is returned instead of the lower bound of the interval.

Returns:

The lower bound of the range in which the `value` falls or `None`. If a transposed list of values ​​exists then the result (lower bound) is taken from the `transposed` list before being returned.

Example:
```
result = ranking( val, [10,20,30,40] )
```

* returns None when val < 10
* returns 10 when val>= 10 and val < 20
* returns 20 when val>= 20 and val < 30
* returns 30 when val>= 30 and val < 40
* returns 40 when val>= 40

```
result = ranking( val, [10,20,30,40], ["A", "B", "C", "D"] )
```

* Returns None when val < 10
* Returns "A" when val>= 10 and val < 20
* Returns "B" when val>= 20 and val < 30
* Returns "C" when val>= 30 and val < 40
* Returns "D" when val>= 40

remarks: the call could also be writtent `result = ranking( val, [10,20,30,40], "ABCD" )`

# slice_by() function
The `slice_by()` function can be used to divide a list into sub-lists of N items.

``` python
def slice_by( lst, by_len ):
```

avec:

* __lst__ : the source list.
* __by_len__ : the number of items into each sub-lists.


Example:
``` python
from maps import slice_by

l = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26]
print( "slice by 5", slice_by(l,5) )
```

Which displays the following results:

```
slice by 5 [[1, 2, 3, 4, 5], [6, 7, 8, 9, 10], [11, 12, 13, 14, 15], [16, 17, 18, 19, 20], [21, 22, 23, 24, 25], [26]]
```

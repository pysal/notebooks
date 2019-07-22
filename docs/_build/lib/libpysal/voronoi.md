---
interact_link: content/lib/libpysal/voronoi.ipynb
kernel_name: python3
has_widgets: false
title: 'voronoi'
prev_page:
  url: /lib/libpysal/weights
  title: 'weights'
next_page:
  url: 
  title: ''
comment: "***PROGRAMMATICALLY GENERATED, DO NOT EDIT. SEE ORIGINAL FILES IN /content***"
---


## Voronoi Polygons for 2-D Point Sets

Author: Serge Rey (http://github.com/sjsrey)




### Basic Usage



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
import sys
import os
sys.path.append(os.path.abspath('..'))
import libpysal

```
</div>

</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
from libpysal.cg.voronoi  import voronoi, voronoi_frames

```
</div>

</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
points = [(10.2, 5.1), (4.7, 2.2), (5.3, 5.7), (2.7, 5.3)]

```
</div>

</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
regions, vertices = voronoi(points)

```
</div>

</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
regions

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
[[1, 3, 2], [4, 5, 1, 0], [0, 1, 7, 6], [9, 0, 8]]
```


</div>
</div>
</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
vertices

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
array([[  4.21783296,   4.08408578],
       [  7.51956025,   3.51807539],
       [  9.4642193 ,  19.3994576 ],
       [ 14.98210684, -10.63503022],
       [ -9.22691341,  -4.58994414],
       [ 14.98210684, -10.63503022],
       [  1.78491801,  19.89803294],
       [  9.4642193 ,  19.3994576 ],
       [  1.78491801,  19.89803294],
       [ -9.22691341,  -4.58994414]])
```


</div>
</div>
</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
region_df, point_df = voronoi_frames(points)

```
</div>

</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
%matplotlib inline
import matplotlib
import numpy as np
import matplotlib.pyplot as plt

```
</div>

</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
fig, ax = plt.subplots()
region_df.plot(ax=ax, color='blue',edgecolor='black', alpha=0.3)
point_df.plot(ax=ax, color='red')


```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
<matplotlib.axes._subplots.AxesSubplot at 0x7f85e38b94a8>
```


</div>
</div>
<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">

{:.output_png}
![png](../../images/lib/libpysal/voronoi_10_1.png)

</div>
</div>
</div>



### Larger Problem



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
n_points = 200
np.random.seed(12345)
points = np.random.random((n_points,2))*10 + 10
results = voronoi(points)
mins = points.min(axis=0)
maxs = points.max(axis=0)

```
</div>

</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
regions, vertices = voronoi(points)

```
</div>

</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
regions_df, points_df = voronoi_frames(points)

```
</div>

</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
fig, ax = plt.subplots()
points_df.plot(ax=ax, color='red')

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
<matplotlib.axes._subplots.AxesSubplot at 0x7f85e39dae10>
```


</div>
</div>
<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">

{:.output_png}
![png](../../images/lib/libpysal/voronoi_15_1.png)

</div>
</div>
</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
fig, ax = plt.subplots()
regions_df.plot(ax=ax, color='blue',edgecolor='black', alpha=0.3)
points_df.plot(ax=ax, color='red')

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
<matplotlib.axes._subplots.AxesSubplot at 0x7f85e1fbd240>
```


</div>
</div>
<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">

{:.output_png}
![png](../../images/lib/libpysal/voronoi_16_1.png)

</div>
</div>
</div>



### Trimming



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
points = np.array(points)
maxs = points.max(axis=0)
mins = points.min(axis=0)
xr = maxs[0] - mins[0]
yr = maxs[1] - mins[1]
buff = 0.05
r = max(yr, xr) * buff
minx = mins[0] - r
miny = mins[1] - r
maxx = maxs[0] + r
maxy = maxs[1] + r

```
</div>

</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
fig, ax = plt.subplots()
regions_df.plot(ax=ax, edgecolor='black', facecolor='blue', alpha=0.2 )
points_df.plot(ax=ax, color='red')
plt.xlim(minx, maxx)
plt.ylim(miny, maxy)
plt.title("buffer: %f, n: %d"%(r,n_points))
plt.show()


```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">

{:.output_png}
![png](../../images/lib/libpysal/voronoi_19_0.png)

</div>
</div>
</div>



## Voronoi Weights



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
from libpysal.weights.contiguity import Voronoi as Vornoi_weights

```
</div>

</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
w = Vornoi_weights(points)

```
</div>

</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
w.n

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
200
```


</div>
</div>
</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
w.pct_nonzero

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
2.915
```


</div>
</div>
</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
w.histogram

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
[(3, 3),
 (4, 28),
 (5, 52),
 (6, 65),
 (7, 34),
 (8, 10),
 (9, 5),
 (10, 2),
 (11, 0),
 (12, 1)]
```


</div>
</div>
</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
idx = [i for i in range(w.n) if w.cardinalities[i]==12]

```
</div>

</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
points[idx]

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
array([[16.50851787, 13.12932895]])
```


</div>
</div>
</div>


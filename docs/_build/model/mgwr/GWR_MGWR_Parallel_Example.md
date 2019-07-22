---
redirect_from:
  - "/model/mgwr/gwr-mgwr-parallel-example"
interact_link: content/model/mgwr/GWR_MGWR_Parallel_Example.ipynb
kernel_name: python3
has_widgets: false
title: 'GWR_MGWR_Parallel_Example'
prev_page:
  url: /model/mgwr/MGWR_Georgia_example
  title: 'MGWR_Georgia_example'
next_page:
  url: /lib/libpysal/intro
  title: 'libpysal'
comment: "***PROGRAMMATICALLY GENERATED, DO NOT EDIT. SEE ORIGINAL FILES IN /content***"
---


<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
import numpy as np
import geopandas as gp
import multiprocessing as mp
import pysal.lib as ps
import sys
sys.path.append('/Users/Ziqi/Desktop/mgwr/')
from pysal.model.mgwr.gwr import GWR,MGWR
from pysal.model.mgwr.sel_bw import Sel_BW

```
</div>

</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
#Load Berlin example
prenz = gp.read_file(ps.examples.get_path('prenzlauer.zip'))

```
</div>

</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
b_y = np.log(prenz['price'].values.reshape((-1, 1)))
b_X = prenz[['review_sco','accommodat','bathrooms']].values 
b_X = (b_X - b_X.mean(axis=0)) / b_X.std(axis=0)
b_y = (b_y - b_y.mean(axis=0)) / b_y.std(axis=0)
u = prenz['X']
v = prenz['Y']
b_coords = list(zip(u, v))

```
</div>

</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
#This might be needed to turn off the OpenMP multi-threading
%env OMP_NUM_THREADS = 1

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">
{:.output_stream}
```
env: OMP_NUM_THREADS=1
```
</div>
</div>
</div>



### GWR No Parallel



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
%%time
gwr_selector = Sel_BW(b_coords, b_y, b_X)
gwr_bw = gwr_selector.search()
print(gwr_bw)
gwr_results = GWR(b_coords, b_y, b_X, gwr_bw).fit()

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">
{:.output_stream}
```
192.0
CPU times: user 13.9 s, sys: 116 ms, total: 14 s
Wall time: 14.2 s
```
</div>
</div>
</div>



### MGWR No Parallel



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
%%time
mgwr_selector = Sel_BW(b_coords, b_y, b_X, multi=True)
mgwr_bw = mgwr_selector.search()
print(mgwr_bw)
mgwr_results = MGWR(b_coords, b_y, b_X, selector=mgwr_selector).fit()

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">
{:.output_stream}
```
[ 191. 1279.   79. 2200.]
CPU times: user 3min 37s, sys: 2.73 s, total: 3min 40s
Wall time: 3min 18s
```
</div>
</div>
</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
#Parrallelization is more favored when you your data are large and/or your machine have many many cores.
#mgwr has soft dependency of numba, please install numba if you need better performance (pip install numba).

n_proc = 2 #two processors
pool = mp.Pool(n_proc) 

```
</div>

</div>



### GWR Parallel



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
%%time
gwr_selector = Sel_BW(b_coords, b_y, b_X)
gwr_bw = gwr_selector.search(pool=pool) #add pool to Sel_BW.search
print(gwr_bw)
gwr_results = GWR(b_coords, b_y, b_X, gwr_bw).fit(pool=pool) #add pool to GWR.fit

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">
{:.output_stream}
```
192.0
CPU times: user 303 ms, sys: 42.3 ms, total: 346 ms
Wall time: 7.05 s
```
</div>
</div>
</div>



### MGWR Parallel



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
%%time
mgwr_selector = Sel_BW(b_coords, b_y, b_X, multi=True)
mgwr_bw = mgwr_selector.search(pool=pool) #add pool to Sel_BW.search
print(mgwr_bw)
mgwr_results = MGWR(b_coords, b_y, b_X, selector=mgwr_selector).fit(pool=pool) #add pool to MGWR.fit

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">
{:.output_stream}
```
[ 191. 1279.   79. 2200.]
CPU times: user 5.08 s, sys: 388 ms, total: 5.46 s
Wall time: 2min 2s
```
</div>
</div>
</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
pool.close() # Close the pool when you finish
pool.join()

```
</div>

</div>


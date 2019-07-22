---
redirect_from:
  - "/model/spint/test-grav"
interact_link: content/model/spint/test_grav.ipynb
kernel_name: Python [Root]
has_widgets: false
title: 'test_grav'
prev_page:
  url: /model/spint/sparse_categorical
  title: 'sparse_categorical'
next_page:
  url: /model/spint/sparse_grav
  title: 'sparse_grav'
comment: "***PROGRAMMATICALLY GENERATED, DO NOT EDIT. SEE ORIGINAL FILES IN /content***"
---


<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
import numpy as np
import pandas as pd
import os
os.chdir('../')
from gravity import Gravity, Production, Attraction, Doubly, BaseGravity
import statsmodels.formula.api as smf
from statsmodels.api import families
import matplotlib.pyplot as plt
%pylab inline

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">
{:.output_stream}
```
Populating the interactive namespace from numpy and matplotlib
```
</div>
</div>
</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python

n = 3000
o = np.tile(np.arange(n),n)
d = np.repeat(np.arange(n),n)
loc_size = np.random.randint(25000,500000, n)
o_vars = np.tile(loc_size, n)
d_vars = np.repeat(loc_size, n)
dij = np.random.exponential(2500, n**2)
f = o_vars**.3*d_vars**.4*np.exp(dij*-.00005)
o = np.reshape(o, (-1,1))
d = np.reshape(d, (-1,1))
o_vars = np.reshape(o_vars, (-1,1))
d_vars = np.reshape(d_vars, (-1,1))
dij = np.reshape(dij, (-1,1))
f = np.reshape(f, (-1,1))
f = f.astype(np.int64)

```
</div>

</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
%time Gravity(f, o_vars, d_vars, dij, 'exp')

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">
{:.output_stream}
```
CPU times: user 14.3 s, sys: 1.46 s, total: 15.8 s
Wall time: 7.41 s
```
</div>
</div>
<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
<gravity.Gravity at 0x118346850>
```


</div>
</div>
</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
%time Production(f, o, d_vars, dij, 'exp')

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">
{:.output_stream}
```
CPU times: user 38.3 s, sys: 4 s, total: 42.3 s
Wall time: 24.6 s
```
</div>
</div>
<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
<gravity.Production at 0x118353510>
```


</div>
</div>
</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
%time Attraction(f, d, o_vars, dij, 'exp')

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">
{:.output_stream}
```
CPU times: user 36 s, sys: 4.25 s, total: 40.2 s
Wall time: 21.4 s
```
</div>
</div>
<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
<gravity.Attraction at 0x118353310>
```


</div>
</div>
</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
%time Doubly(f, o, d, dij, 'exp')

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">
{:.output_stream}
```
CPU times: user 1min 19s, sys: 6.3 s, total: 1min 25s
Wall time: 37.4 s
```
</div>
</div>
<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
<gravity.Doubly at 0x118353250>
```


</div>
</div>
</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
from glm import GLM
from iwls import iwls
import line_profiler
import IPython
ip = IPython.get_ipython()
ip.define_magic('lprun', line_profiler.magic_lprun)
instance = Production(f, o, d_vars, dij, 'exp')


```
</div>

</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
%lprun -f BaseGravity.__init__ instance.__init__(f, o, d_vars, dij, 'exp')

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">
{:.output_stream}
```
correct sparse
```
</div>
</div>
</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
glm_inst = GLM(instance.y, instance.X, family=families.Poisson())
%lprun -f GLM.__init__ glm_inst.__init__(instance.y, instance.X, family=families.Poisson())

```
</div>

</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
%lprun -f iwls iwls(instance.y, instance.X, family=families.Poisson(), offset=None, y_fix=None)

```
</div>

</div>


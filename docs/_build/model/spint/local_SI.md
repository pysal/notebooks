---
redirect_from:
  - "/model/spint/local-si"
interact_link: content/model/spint/local_SI.ipynb
kernel_name: python3
has_widgets: false
title: 'local_SI'
prev_page:
  url: /model/spint/sparse_scipy_optim
  title: 'sparse_scipy_optim'
next_page:
  url: /model/spint/validate_gravity
  title: 'validate_gravity'
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
austria = pd.read_csv('http://dl.dropbox.com/u/8649795/AT_Austria.csv')
austria = austria[austria['Origin'] != austria['Destination']]
f = austria['Data'].values
o = austria['Origin'].values
d = austria['Destination'].values
dij = austria['Dij'].values
o_vars = austria['Oi2007'].values
d_vars = austria['Dj2007'].values

```
</div>

</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
model = Gravity(f, o_vars, d_vars, dij, 'exp')
print model.params[-1]

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">
{:.output_stream}
```
-0.00976746026969
```
</div>
</div>
</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
local = model.local(loc_index=o, locs=np.unique(o))
local['param2']

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
[-0.01699776161094757,
 -0.0053210259160796358,
 -0.0028594272276957211,
 -0.006533037784217155,
 -0.0024666647861060209,
 -0.0058258251130860472,
 -0.010739622617965516,
 -0.0046867791898773659,
 -0.0065940756391066335]
```


</div>
</div>
</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
model = Production(f, o, d_vars, dij, 'exp')
print model.params[-1]

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">
{:.output_stream}
```
-0.00727113391179
```
</div>
</div>
</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
local = model.local()
local['param2']

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
[-0.016997761610949791,
 -0.005321025916080413,
 -0.0028594272276953325,
 -0.0065330377842177101,
 -0.0024666647861060209,
 -0.0058258251130863803,
 -0.010739622617965183,
 -0.0046867791898770328,
 -0.0065940756391070776]
```


</div>
</div>
</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
model = Attraction(f, d, o_vars, dij, 'exp')
print model.params[-1]

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">
{:.output_stream}
```
-0.00693754909526
```
</div>
</div>
</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
local = model.local()
local['param2']

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
[-0.010872636479707154,
 -0.0054690202130680543,
 -0.0025567421332022833,
 -0.0051439340488994012,
 -0.0036020461535491433,
 -0.010088935906795271,
 -0.012926843651020203,
 -0.0075750287063747201,
 -0.0081576735088411123]
```


</div>
</div>
</div>


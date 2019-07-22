---
redirect_from:
  - "/model/spint/validate-gravity"
interact_link: content/model/spint/validate_gravity.ipynb
kernel_name: Python [Root]
has_widgets: false
title: 'validate_gravity'
prev_page:
  url: /model/spint/local_SI
  title: 'local_SI'
next_page:
  url: /model/spint/dispersion_test
  title: 'dispersion_test'
comment: "***PROGRAMMATICALLY GENERATED, DO NOT EDIT. SEE ORIGINAL FILES IN /content***"
---


<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
#import sys
#sys.path.append('/Users/toshan/dev/pysal/pysal/contrib/glm')
#from utils import 
import numpy as np
import pandas as pd
import sys
sys.path.append('/Users/toshan/dev/pysal/pysal/contrib/spint')
from gravity import Gravity, Production, Attraction, Doubly, BaseGravity
import gravity
from utils import sorensen
import statsmodels.formula.api as smf
from statsmodels.api import families as families

```
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
grav = Gravity(f, o_vars, d_vars, dij, 'exp', framework='glm', constant=True)
print grav.params

gravity = smf.glm('Data~np.log(Oi2007)+np.log(Dj2007)+Dij', family=families.Poisson(), data=austria).fit()
print gravity.params.values

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">
{:.output_stream}
```
[ -7.95447436e+00   8.63867812e-01   8.80474585e-01  -6.20544765e-03]
[ -7.95447436e+00   8.63867812e-01   8.80474585e-01  -6.20544766e-03]
```
</div>
</div>
</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
production = Production(f, o, d_vars, dij, 'exp', framework='glm')
print production.params

gravity = smf.glm('Data~Origin+np.log(Dj2007)+Dij', family=families.Poisson(), data=austria).fit()
print gravity.params.values

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">
{:.output_stream}
```
[-1.11700938  1.68662317  2.15188689  0.60300297  0.88380784  1.20926104
  0.68938983  1.15472804  1.02479968  0.89278717 -0.00727113]
[-1.11700938  1.68662317  2.15188689  0.60300297  0.88380784  1.20926105
  0.68938983  1.15472805  1.02479968  0.89278717 -0.00727113]
```
</div>
</div>
</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
attraction = Attraction(f, d, o_vars, dij, 'exp', framework='glm', constant=True)
print attraction.params

gravity = smf.glm('Data~np.log(Oi2007)+Destination + Dij', family=families.Poisson(), data=austria).fit()
print gravity.params.values

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">
{:.output_stream}
```
[-0.88439723  1.62180605  1.92772078  0.12462001  0.62378812  0.69646073
  0.20909411  0.6856777   0.48539625  0.89235874 -0.00693755]
[-0.88439723  1.62180605  1.92772078  0.12462002  0.62378812  0.69646073
  0.20909411  0.6856777   0.48539625  0.89235874 -0.00693755]
```
</div>
</div>
</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
doubly = Doubly(f, o, d, dij, 'exp', framework='glm', constant=True)
print doubly.params

gravity = smf.glm('Data~Origin+Destination+Dij', family=families.Poisson(), data=austria).fit()
print gravity.params.values

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">
{:.output_stream}
```
[ 6.20471518  1.5449095   2.4414292   0.69924374  0.94869185  1.28967637
  0.74270015  1.19468573  0.98874193  1.49709841  2.18492741  0.18784818
  0.66434515  0.74264938  0.21334535  0.66765781  0.39986094 -0.00791533]
[ 6.20471518  1.5449095   2.4414292   0.69924374  0.94869185  1.28967637
  0.74270016  1.19468574  0.98874192  1.49709841  2.18492741  0.18784818
  0.66434515  0.74264938  0.21334535  0.66765782  0.39986087 -0.00791533]
```
</div>
</div>
</div>


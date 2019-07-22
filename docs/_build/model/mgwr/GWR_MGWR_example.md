---
redirect_from:
  - "/model/mgwr/gwr-mgwr-example"
interact_link: content/model/mgwr/GWR_MGWR_example.ipynb
kernel_name: python3
has_widgets: false
title: 'GWR_MGWR_example'
prev_page:
  url: /model/mgwr/GWR_prediction_example
  title: 'GWR_prediction_example'
next_page:
  url: /model/mgwr/MGWR_Georgia_example
  title: 'MGWR_Georgia_example'
comment: "***PROGRAMMATICALLY GENERATED, DO NOT EDIT. SEE ORIGINAL FILES IN /content***"
---


<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
import numpy as np
# import scipy as sp
from pysal.model.mgwr.sel_bw import Sel_BW
# from pysal.model.mgwr.gwr import GWR, MGWR
import pandas as pd
import pysal.lib as ps
# import pickle as pk
# import os

```
</div>

</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
data = ps.io.open(ps.examples.get_path('GData_utm.csv'))
coords = list(zip(data.by_col('X'), data.by_col('Y')))
y = np.array(data.by_col('PctBach')).reshape((-1,1))
rural  = np.array(data.by_col('PctRural')).reshape((-1,1))
pov = np.array(data.by_col('PctPov')).reshape((-1,1)) 
black = np.array(data.by_col('PctBlack')).reshape((-1,1))
fb = np.array(data.by_col('PctFB')).reshape((-1,1))
pop = np.array(data.by_col('TotPop90')).reshape((-1,1))


X = np.hstack([fb, black, rural])


```
</div>

</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
X = (X - X.mean(axis=0)) / X.std(axis=0)

y = y.reshape((-1,1))

y = (y - y.mean(axis=0)) / y.std(axis=0)

sel = Sel_BW(coords, y, X)

bw = sel.search()
print('bw:', bw)
gwr = GWR(coords, y, X, bw)
gwr_results = gwr.fit()
print('aicc:', gwr_results.aicc)
print('ENP:', gwr_results.ENP)
print('sigma2:', gwr_results.sigma2)

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">
{:.output_stream}
```
bw: 117.0
```
</div>
</div>
<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">
{:.output_traceback_line}
```

    ---------------------------------------------------------------------------

    NameError                                 Traceback (most recent call last)

    <ipython-input-3-2da488ac544f> in <module>
          9 bw = sel.search()
         10 print('bw:', bw)
    ---> 11 gwr = GWR(coords, y, X, bw)
         12 gwr_results = gwr.fit()
         13 print('aicc:', gwr_results.aicc)


    NameError: name 'GWR' is not defined


```
</div>
</div>
</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
X = (X - X.mean(axis=0)) / X.std(axis=0)

y = y.reshape((-1,1))

y = (y - y.mean(axis=0)) / y.std(axis=0)

selector = Sel_BW(coords, y, X, multi=True, constant=True)
bw = selector.search(multi_bw_min=[2], multi_bw_max=[159])
print('bw(intercept):', bw[0])
print('bw(foreign):', bw[1])
print('bw(african_amer):', bw[2])
print('bw(rural):', bw[3])
mgwr = MGWR(coords, y, X, selector, constant=True)
mgwr_results = mgwr.fit()
print('aicc:', mgwr_results.aicc)
print('sigma2:', mgwr_results.sigma2)
print('ENP(model):', mgwr_results.ENP)
print('adj_alpha(model):', mgwr_results.adj_alpha[1])
print('critical_t(model):', mgwr_results.critical_tval(alpha=mgwr_results.adj_alpha[1]))
alphas = mgwr_results.adj_alpha_j[:,1]
critical_ts = mgwr_results.critical_tval()
print('ENP(intercept):', mgwr_results.ENP_j[0])
print('adj_alpha(intercept):', alphas[0])
print('critical_t(intercept):', critical_ts[0])
print('ENP(foreign):', mgwr_results.ENP_j[1])
print('adj_alpha(foreign):', alphas[1])
print('critical_t(foreign):', critical_ts[1])
print('ENP(african_amer):', mgwr_results.ENP_j[2])
print('adj_alpha(african_amer):', alphas[2])
print('critical_t(african_amer):', critical_ts[2])
print('ENP(rural):', mgwr_results.ENP_j[3])
print('adj_alpha(rural):', alphas[3])
print('critical_t(rural):', critical_ts[3])

```
</div>

</div>


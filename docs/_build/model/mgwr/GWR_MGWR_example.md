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
from pysal.model.mgwr.sel_bw import Sel_BW
from pysal.model.mgwr.gwr import GWR, MGWR
import pandas as pd
import pysal.lib as ps

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
aicc: 299.0508086830288
ENP: 11.804769716730096
sigma2: 0.3477435474978281
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

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">
{:.output_stream}
```
bw(intercept): 92.0
bw(foreign): 101.0
bw(african_amer): 136.0
bw(rural): 158.0
aicc: 297.12013812258783
sigma2: 0.34477258292171475
ENP(model): 11.368250872698306
adj_alpha(model): 0.017592855949398054
critical_t(model): 2.399257840857394
ENP(intercept): 3.8446710802641415
adj_alpha(intercept): 0.013005013681577368
critical_t(intercept): 2.512107491068591
ENP(foreign): 3.5137708051516503
adj_alpha(foreign): 0.01422972719982004
critical_t(foreign): 2.4788879239423856
ENP(african_amer): 2.258052527889825
adj_alpha(african_amer): 0.022142974701622888
critical_t(african_amer): 2.3106911297007184
ENP(rural): 1.7517564593926895
adj_alpha(rural): 0.02854278043726143
critical_t(rural): 2.210001836555586
```
</div>
</div>
</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
mgwr_results.summary()

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">
{:.output_stream}
```
===========================================================================
Model type                                                         Gaussian
Number of observations:                                                 159
Number of covariates:                                                     4

Global Regression Results
---------------------------------------------------------------------------
Residual sum of squares:                                             71.793
Log-likelihood:                                                    -162.399
AIC:                                                                332.798
AICc:                                                               335.191
BIC:                                                               -713.887
R2:                                                                   0.548
Adj. R2:                                                              0.540

Variable                              Est.         SE  t(Est/SE)    p-value
------------------------------- ---------- ---------- ---------- ----------
X0                                  -0.000      0.054     -0.000      1.000
X1                                   0.458      0.066      6.988      0.000
X2                                  -0.084      0.055     -1.525      0.127
X3                                  -0.374      0.065     -5.734      0.000

Multi-Scale Geographically Weighted Regression (MGWR) Results
---------------------------------------------------------------------------
Spatial kernel:                                           Adaptive bisquare
Criterion for optimal bandwidth:                                       AICc
Score of Change (SOC) type:                                     Smoothing f
Termination criterion for MGWR:                                       1e-05

MGWR bandwidths
---------------------------------------------------------------------------
Variable             Bandwidth      ENP_j   Adj t-val(95%)   Adj alpha(95%)
X0                      92.000      3.845            2.512            0.013
X1                     101.000      3.514            2.479            0.014
X2                     136.000      2.258            2.311            0.022
X3                     158.000      1.752            2.210            0.029

Diagnostic information
---------------------------------------------------------------------------
Residual sum of squares:                                             50.899
Effective number of parameters (trace(S)):                           11.368
Degree of freedom (n - trace(S)):                                   147.632
Sigma estimate:                                                       0.587
Log-likelihood:                                                    -135.056
AIC:                                                                294.849
AICc:                                                               297.120
BIC:                                                                332.806
R2                                                                    0.680
Adjusted R2                                                           0.655

Summary Statistics For MGWR Parameter Estimates
---------------------------------------------------------------------------
Variable                   Mean        STD        Min     Median        Max
-------------------- ---------- ---------- ---------- ---------- ----------
X0                        0.017      0.171     -0.260      0.058      0.271
X1                        0.479      0.216      0.117      0.500      0.722
X2                       -0.069      0.036     -0.146     -0.064     -0.014
X3                       -0.304      0.019     -0.347     -0.302     -0.266
===========================================================================

```
</div>
</div>
</div>


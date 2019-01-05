---
redirect_from:
  - "/model/spint/sparse-scipy-optim"
interact_link: content/model/spint/sparse_scipy_optim.ipynb
title: 'sparse_scipy_optim'
prev_page:
  url: /model/spint/New_DistanceBand
  title: 'New_DistanceBand'
next_page:
  url: /model/spint/local_SI
  title: 'local_SI'
comment: "***PROGRAMMATICALLY GENERATED, DO NOT EDIT. SEE ORIGINAL FILES IN /content***"
---



{:.input_area}
```python
import pandas as pd
import scipy.optimize as sc
import scipy.sparse as sp
```




{:.input_area}
```python
data = np.random.poisson(100, (10000,1))
```




{:.input_area}
```python
data = sp.csr_matrix(data)
```




{:.input_area}
```python
def poiss_loglike(x, data, a):
    print x
    return -np.sum(data*np.log(x)-x)*a


params = sc.fmin(poiss_loglike, 0, args=(data ,1))
print params
```


{:.output_stream}
```
[ 0.]
[ 0.00025]
[ 0.0005]
[ 0.00075]
[ 0.00125]
[ 0.00175]
[ 0.00275]
[ 0.00375]
[ 0.00575]
[ 0.00775]
[ 0.01175]
[ 0.01575]
[ 0.02375]
[ 0.03175]
[ 0.04775]
[ 0.06375]
[ 0.09575]
[ 0.12775]
[ 0.19175]
[ 0.25575]
[ 0.38375]
[ 0.51175]
[ 0.76775]
[ 1.02375]
[ 1.53575]
[ 2.04775]
[ 3.07175]
[ 4.09575]
[ 6.14375]
[ 8.19175]
[ 12.28775]
[ 16.38375]
[ 24.57575]
[ 32.76775]
[ 49.15175]
[ 65.53575]
[ 98.30375]
[ 131.07175]
[ 131.07175]
[ 114.68775]
[ 81.91975]
[ 106.49575]
[ 90.11175]
[ 102.39975]
[ 94.20775]
[ 100.35175]
[ 102.39975]
[ 99.32775]
[ 98.30375]
[ 99.83975]
[ 100.35175]
[ 99.58375]
[ 100.09575]
[ 99.71175]
[ 99.58375]
[ 99.77575]
[ 99.83975]
[ 99.74375]
[ 99.80775]
[ 99.75975]
[ 99.74375]
[ 99.76775]
[ 99.77575]
[ 99.76375]
[ 99.77175]
[ 99.76575]
[ 99.76975]
[ 99.76675]
[ 99.76875]
[ 99.76725]
[ 99.76825]
[ 99.7675]
[ 99.76725]
[ 99.767625]
[ 99.76775]
[ 99.7675625]
Optimization terminated successfully.
         Current function value: -3594470.473058
         Iterations: 38
         Function evaluations: 76
[ 99.767625]

```

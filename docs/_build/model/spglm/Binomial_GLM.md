---
redirect_from:
  - "/model/spglm/binomial-glm"
interact_link: content/model/spglm/Binomial_GLM.ipynb
title: 'Binomial_GLM'
prev_page:
  url: /model/spglm/Gaussian_GLM
  title: 'Gaussian_GLM'
next_page:
  url: 
  title: ''
comment: "***PROGRAMMATICALLY GENERATED, DO NOT EDIT. SEE ORIGINAL FILES IN /content***"
---



{:.input_area}
```python
from spglm.glm import GLM
from spglm.family import Binomial
import libpysal.api as ps
import numpy as np
```




{:.input_area}
```python
#Load sample dataset - Subset of london house price dataset
db = ps.open(ps.get_path('columbus.dbf'),'r')

#Set dependent variable
y = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
y = y.reshape((316,1))

#Set independent variable (FLOORSZ)
X = np.array([ 77,  75,  64,  95, 107, 100,  81, 151,  98, 260, 171, 161,  91,
    80,  50,  85,  52,  69,  60,  84, 155,  97,  69, 126,  90,  43,
    51,  41, 140,  80,  52,  86,  66,  60,  40, 155, 138,  97, 115,
    148, 206,  60,  53,  96,  88, 160,  31,  43, 154,  60, 131,  60,
    46,  61, 125, 150,  76,  92,  96, 100, 105,  72,  48,  41,  72,
    65,  60,  65,  98,  33, 144, 111,  91, 108,  38,  48,  95,  63,
    98, 129, 108,  51, 131,  66,  48, 127,  76,  68,  52,  64,  57,
    121,  67,  76, 112,  96,  90,  53,  93,  64,  97,  58,  44, 157,
    53,  70,  71, 167,  47,  70,  96,  77,  75,  71,  67,  47,  71,
    90,  69,  64,  65,  95,  60,  60,  65,  54, 121, 105,  50,  85,
    69,  69,  62,  65,  93,  93,  70,  62, 155,  68, 117,  80,  80,
    75,  98, 114,  86,  70,  50,  51, 163, 124,  59,  95,  51,  63,
    85,  53,  46, 102, 114,  83,  47,  40,  63, 123, 100,  63, 110,
    79,  98,  99, 120,  52,  48,  37,  81,  30,  88,  50,  35, 116,
    67,  45,  80,  86, 109,  59,  75,  60,  71, 141, 121,  50, 168,
    90,  51, 133,  75, 133, 127,  37,  68, 105,  61, 123, 151, 110,
    77, 220,  94,  77,  70, 100,  98, 126,  55, 105,  60, 176, 104,
    68,  62,  70,  48, 102,  80,  97,  66,  80, 102, 160,  55,  60,
    71, 125,  85,  85, 190, 137,  48,  41,  42,  51,  57,  60, 114,
    88,  84, 108,  66,  85,  42,  98,  90, 127, 100,  55,  76,  82,
    63,  80,  71,  76, 121, 109,  92, 160, 109, 185, 100,  90,  90,
    86,  88,  95, 116, 135,  61,  74,  60, 235,  76,  66, 100,  49,
    50,  37, 100,  88,  90,  52,  95,  81,  79,  96,  75,  91,  86,
    83, 180, 108,  80,  96,  49, 117, 117,  86,  46,  66,  95,  57,
    120, 137,  68, 240])
X = X.reshape((316,1))
```




{:.input_area}
```python
#Estimate Binomial GLM

#First instantiate a GLM model object
model = GLM(y, X, family=Binomial()) #Set family to Binomial family object for Binomial GLM

#Then use the fit method to estimate coefficients and compute diagnostics
results = model.fit()
```




{:.input_area}
```python
#Estimated prameters, intercept is always the first column on the left
print(results.params)
```


{:.output_stream}
```
[-5.33638276  0.0287754 ]

```



{:.input_area}
```python
#Parameter standard errors
print(results.bse)
```


{:.output_stream}
```
[0.64499904 0.00518312]

```



{:.input_area}
```python
#Parameter t-values
print(results.tvalues)
```


{:.output_stream}
```
[-8.27347396  5.55175826]

```



{:.input_area}
```python
#Model AIC
print(results.aic)
```


{:.output_stream}
```
155.19347530342466

```

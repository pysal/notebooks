---
redirect_from:
  - "/model/spglm/gaussian-glm"
interact_link: content/model/spglm/Gaussian_GLM.ipynb
title: 'Gaussian_GLM'
prev_page:
  url: /model/spglm/Binomial_GLM
  title: 'Binomial_GLM'
next_page:
  url: /model/spglm/Poisson_GLM
  title: 'Poisson_GLM'
comment: "***PROGRAMMATICALLY GENERATED, DO NOT EDIT. SEE ORIGINAL FILES IN /content***"
---



{:.input_area}
```python
from spglm.glm import GLM
import libpysal.api as ps
import numpy as np
```




{:.input_area}
```python
#Load sample dataset - columbus dataset 
db = ps.open(ps.get_path('columbus.dbf'),'r')

#Set dependent variable
y = np.array(db.by_col("HOVAL"))
y = np.reshape(y, (49,1))

#Set indepdent varibLES
X = []
X.append(db.by_col("INC"))
X.append(db.by_col("CRIME"))
X = np.array(X).T
```




{:.input_area}
```python
#Estimate Gaussian GLM

#First instantiate a GLM model object
model = GLM(y, X) #Gaussian is the default family parameter so it doesn't need to be set

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
[46.42818268  0.62898397 -0.48488854]

```



{:.input_area}
```python
#Parameter standard errors
print(results.bse)
```


{:.output_stream}
```
[13.19175703  0.53591045  0.18267291]

```



{:.input_area}
```python
#Parameter t-values
print(results.tvalues)
```


{:.output_stream}
```
[ 3.51948437  1.17367365 -2.65440864]

```



{:.input_area}
```python
#Model AIC
print(results.aic)
```


{:.output_stream}
```
408.73548964604873

```

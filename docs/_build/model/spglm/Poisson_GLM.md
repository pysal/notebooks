---
redirect_from:
  - "/model/spglm/poisson-glm"
interact_link: content/model/spglm/Poisson_GLM.ipynb
title: 'Poisson_GLM'
prev_page:
  url: /model/spglm/Gaussian_GLM
  title: 'Gaussian_GLM'
next_page:
  url: /model/spint/intro
  title: 'spint'
comment: "***PROGRAMMATICALLY GENERATED, DO NOT EDIT. SEE ORIGINAL FILES IN /content***"
---



{:.input_area}
```python
from spglm.glm import GLM
from spglm.family import Poisson
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
#Round dependent variable and convert to integer for the example since Poisson is for discrete data
y = np.round(y).astype(int)

#Set indepdent varibLES
X = []
X.append(db.by_col("INC"))
X.append(db.by_col("CRIME"))
X = np.array(X).T
```




{:.input_area}
```python
#Estimate Poisson GLM

#First instantiate a GLM model object
model = GLM(y, X, family=Poisson()) #Set family to Poisson family object for Poisson GLM

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
[ 3.92159085  0.01183491 -0.01371397]

```



{:.input_area}
```python
#Parameter standard errors
print(results.bse)
```


{:.output_stream}
```
[0.13049161 0.00511599 0.00193769]

```



{:.input_area}
```python
#Parameter t-values
print(results.tvalues)
```


{:.output_stream}
```
[30.0524361   2.31331634 -7.07748998]

```



{:.input_area}
```python
#Model AIC
print(results.aic)
```


{:.output_stream}
```
500.8518417993879

```

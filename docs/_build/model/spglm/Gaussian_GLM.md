---
redirect_from:
  - "/model/spglm/gaussian-glm"
interact_link: content/model/spglm/Gaussian_GLM.ipynb
kernel_name: Python [Root]
has_widgets: false
title: 'Gaussian_GLM'
prev_page:
  url: /model/spglm/Poisson_GLM
  title: 'Poisson_GLM'
next_page:
  url: /model/spglm/Binomial_GLM
  title: 'Binomial_GLM'
comment: "***PROGRAMMATICALLY GENERATED, DO NOT EDIT. SEE ORIGINAL FILES IN /content***"
---


<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
from pysal.model.spglm.glm import GLM
import pysal.lib.api as ps
import numpy as np

```
</div>

</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
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
</div>

</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
#Estimate Gaussian GLM

#First instantiate a GLM model object
model = GLM(y, X) #Gaussian is the default family parameter so it doesn't need to be set

#Then use the fit method to estimate coefficients and compute diagnostics
results = model.fit()

```
</div>

</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
#Estimated prameters, intercept is always the first column on the left
print(results.params)

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">
{:.output_stream}
```
[46.42818268  0.62898397 -0.48488854]
```
</div>
</div>
</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
#Parameter standard errors
print(results.bse)

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">
{:.output_stream}
```
[13.19175703  0.53591045  0.18267291]
```
</div>
</div>
</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
#Parameter t-values
print(results.tvalues)

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">
{:.output_stream}
```
[ 3.51948437  1.17367365 -2.65440864]
```
</div>
</div>
</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
#Model AIC
print(results.aic)

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">
{:.output_stream}
```
408.73548964604873
```
</div>
</div>
</div>


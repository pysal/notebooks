---
redirect_from:
  - "/model/spglm/poisson-glm"
interact_link: content/model/spglm/Poisson_GLM.ipynb
kernel_name: Python [Root]
has_widgets: false
title: 'Poisson_GLM'
prev_page:
  url: /model/spglm/intro
  title: 'spglm'
next_page:
  url: /model/spglm/Gaussian_GLM
  title: 'Gaussian_GLM'
comment: "***PROGRAMMATICALLY GENERATED, DO NOT EDIT. SEE ORIGINAL FILES IN /content***"
---


<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
from pysal.model.spglm.glm import GLM
from pysal.model.spglm.family import Poisson
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
#Round dependent variable and convert to integer for the example since Poisson is for discrete data
y = np.round(y).astype(int)

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
#Estimate Poisson GLM

#First instantiate a GLM model object
model = GLM(y, X, family=Poisson()) #Set family to Poisson family object for Poisson GLM

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
[ 3.92159085  0.01183491 -0.01371397]
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
[0.13049161 0.00511599 0.00193769]
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
[30.0524361   2.31331634 -7.07748998]
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
500.8518417993879
```
</div>
</div>
</div>


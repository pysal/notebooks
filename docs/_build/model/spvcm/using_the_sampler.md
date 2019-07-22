---
redirect_from:
  - "/model/spvcm/using-the-sampler"
interact_link: content/model/spvcm/using_the_sampler.ipynb
kernel_name: ana
has_widgets: false
title: 'using_the_sampler'
prev_page:
  url: /model/spvcm/spatially-varying-coefficients
  title: 'spatially-varying-coefficients'
next_page:
  url: /model/spint/intro
  title: 'spint'
comment: "***PROGRAMMATICALLY GENERATED, DO NOT EDIT. SEE ORIGINAL FILES IN /content***"
---


# Using the sampler

`spvcm` is a generic gibbs sampling framework for spatially-correlated variance components models. The current supported models are:

- `spvcm.both` contains specifications with correlated errors in both levels, with the first statement `se/sma` describing the lower level and the second statement `se/sma` describing the upper level. In addition, `MVCM`, the multilevel variance components model with no spatial correlation, is in the `both` namespace. 
- `spvcm.lower` contains two specifications, `se/sma`, that can be used for a variance components model with correlated lower-level errors.
- `spvcm.upper` contains two specifications, `se/sma` that can be used for a variance components model with correlated upper-level errors. 

### Specification

These derive from a variance components specification: 

$$ Y \sim \mathcal{N}(X\beta, \Psi_1(\lambda, \sigma^2) + \Delta\Psi_2(\rho, \tau^2)\Delta') $$

Where:
1. $\beta$, called `Betas` in code, is the marginal effect parameter. In this implementation, any region-level covariates $Z$ get appended to the end of $X$. So, if $X$ is $n \times p$ ($n$ observations of $p$ covariates)  and $Z$ is $J \times p'$ ($p'$ covariates observed for $J$ regions), then the model's $X$ matrix is $n \times (p + p')$ and $\beta$ is $p + p' \times 1$. 
2. $\Psi_1$ is the covariance function for the response-level model. In the software, a separable covariance is assumed, so that $\Psi_1(\rho, \sigma^2) = \Psi_1(\rho) * I \sigma^2)$, where $I$ is the $n \times n$ covariance matrix. Thus, $\rho$ is the spatial autoregressive parameter and $\sigma^2$ is the variance parameter. In the software, $\Psi_1$ takes any of the following forms:
    - Spatial Error (`SE`): $\Psi_1(\rho) = [(I - \rho \mathbf{W})'(I - \rho \mathbf{W})]^{-1} \sigma^2$
    - Spatial Moving Average (`SMA`): $\Psi_1(\rho) = (I + \rho \mathbf{W})(I + \lambda \mathbf{W})'$
    - Identity: $\Psi_1(\rho) = I$
2. $\Psi_2$ is the region-level covariance function, with region-level autoregressive parameter $\lambda$ and region-level variance $\tau^2$. It has the same potential forms as $\Psi_1$. 
3. $\alpha$, called `Alphas` in code, is the region-level random effect. In a variance components model, this is interpreted as a random effect for the upper-level. For a Varying-intercept format, this random component should be added to a region-level fixed effect to provide the varying intercept. This may also make it more difficult to identify the spatial parameter. 

## Softare implementation

All of the possible combinations of Spatial Moving Average and Spatial Error processes are contained in the following classes. I will walk through estimating one below, and talk about the various features of the package. 

First, the API of the package is defined by the `spvcm.api` submodule. To load it, use `from pysal.model import spvcm.api as spvcm`:



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
from pysal.model import spvcm as spvcm #package API
spvcm.both_levels.Generic # abstract customizable class, ignores rho/lambda, equivalent to MVCM
spvcm.both_levels.MVCM # no spatial effect
spvcm.both_levels.SESE #  both spatial error (SE)
spvcm.both_levels.SESMA # response-level SE, region-level spatial moving average
spvcm.both_levels.SMASE # response-level SMA, region-level SE
spvcm.both_levels.SMASMA # both levels SMA
spvcm.upper_level.Upper_SE # response-level uncorrelated, region-level SE
spvcm.upper_level.Upper_SMA # response-level uncorrelated, region-level SMA
spvcm.lower_level.Lower_SE # response-level SE, region-level uncorrelated
spvcm.lower_level.Lower_SMA # response-level SMA, region-level uncorrelated 

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
spvcm.lower_level.sma.model.Lower_SMA
```


</div>
</div>
</div>



Depending on the structure of the model, you need at least:
- `X`, data at the response (lower) level
- `Y`, system response in the lower level
- `membership` or `Delta`, the membership vector relating each observation to its group or the "dummy variable" matrix encoding the same information. 

Then, if spatial correlation is desired, `M` is the "upper-level" weights matrix and `W` the lower-level weights matrix. 

Any upper-level data should be passed in $Z$, and have $J$ rows. To fit a varying-intercept model, include an identity matrix in $Z$. You can include state-level and response-level intercept terms simultaneously. 

Finally, there are many configuration and tuning options that can be passed in at the start, or assigned after the model is initialized. 

First, though, let's set up some data for a model on southern counties predicting `HR90`, the Homicide Rate in the US South in 1990, using the the percent of the labor force that is unemployed (`UE90`), a principal component expressing the population structure (`PS90`), and a principal component expressing resource deprivation. 

We will also use the state-level average percentage of families below the poverty line and the average Gini coefficient at the state level for a $Z$ variable. 



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
#seaborn is required for the traceplots
import pysal as ps
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import geopandas as gpd
%matplotlib inline

```
</div>

</div>



Reading in the data, we'll extract these values we need from the dataframe.



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
data = ps.pdio.read_files(ps.examples.get_path('south.shp'))
gdf = gpd.read_file(ps.examples.get_path('south.shp'))
data = data[data.STATE_NAME != 'District of Columbia']
X = data[['UE90', 'PS90', 'RD90']].values
N = X.shape[0]
Z = data.groupby('STATE_NAME')[['FP89', 'GI89']].mean().values
J = Z.shape[0]

Y = data.HR90.values.reshape(-1,1)

```
</div>

</div>



Then, we'll construct some queen contiguity weights from the files to show how to run a model. 



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
W2 = ps.queen_from_shapefile(ps.examples.get_path('us48.shp'), 
                             idVariable='STATE_NAME')
W2 = ps.w_subset(W2, ids=data.STATE_NAME.unique().tolist()) #only keep what's in the data
W1 = ps.queen_from_shapefile(ps.examples.get_path('south.shp'),
                             idVariable='FIPS')
W1 = ps.w_subset(W1, ids=data.FIPS.tolist()) #again, only keep what's in the data

W1.transform = 'r'
W2.transform = 'r'

```
</div>

</div>



With the data, upper-level weights, and lower-level weights, we can construct a membership vector *or* a dummy data matrix. For now, I'll create the membership vector.



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
membership = data.STATE_NAME.apply(lambda x: W2.id_order.index(x)).values

```
</div>

</div>



But, we could also build the dummy variable matrix using `pandas`, if we have a suitable categorical variable:



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
Delta_frame = pd.get_dummies(data.STATE_NAME)
Delta = Delta_frame.values

```
</div>

</div>



Every call to the sampler is of the following form:

`sampler(Y, X, W, M, Z, membership, Delta, n_samples, **configuration)`

Where `W`, `M` are passed if appropriate, `Z` is passed if used, and only one of `membership` or `Delta` is required. In the end, `Z` is appended to `X`, so the effects pertaining to the upper level will be at the tail end of the $\beta$ effects vector. If both `Delta` and `membership` are supplied, they're verified against each other to ensure that they agree before they are used in the model. 

For all models, the membership vector or an equivalent dummy variable matrix is required. For models with correlation in the upper level, only the upper-level weights matrix $\mathbf{M}$ is needed. For lower level models, the lower-level weights matrix $\mathbf{W}$ is required. For models with correlation in both levels, both $\mathbf{W}$ and $\mathbf{M}$ are required. 

Every sampler uses, either in whole or in part, `spvcm.both.generic`, which implements the full generic sampler discussed in the working paper. For efficiency, the upper-level samplers modify this runtime to avoid processing the full lower-level covariance matrix. 

Like many of the `R` packages dedicated to bayesian models, configuration occurs by passing the correct dictionary to the model call. In addition, you can "setup" the model, configure it, and then run samples in separate steps. 

The most common way to call the sampler is something like:



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
vcsma = spvcm.upper_level.Upper_SMA(Y, X, M=W2, Z=Z, 
                                    membership=membership, 
                                    n_samples=5000,
                                    configs=dict(tuning=1000, 
                                                 adapt_step=1.01))

```
</div>

</div>



This model, `spvcm.upper_level.Upper_SMA`, is a variance components/varying intercept model with a state-level SMA-correlated error. 

Thus, there are only five parameters in this model, since $\rho$, the lower-level autoregressive parameter, is constrained to zero:



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
vcsma.trace.varnames

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
['Alphas', 'Betas', 'Sigma2', 'Tau2', 'Lambda']
```


</div>
</div>
</div>



The results and state of the sampler are stored within the `vcsma` object. I'll step through the most important parts of this object. 

# `trace`

The quickest way to get information out of the model is via the trace object. This is where the results of the tracked parameters are stored each iteration. Any variable in the sampler state can be added to the tracked params. Trace objects are essentially dictionaries with the keys being the name of the tracked parameter and the values being a list of each iteration's sampler output.



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
vcsma.trace.varnames

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
['Alphas', 'Betas', 'Sigma2', 'Tau2', 'Lambda']
```


</div>
</div>
</div>



In this case, `Lambda` is the upper-level moving average parameter, `Alphas` is the vector of correlated group-level random effects, `Tau2` is the upper-level variance, `Betas` are the marginal effects, and `Sigma2` is the lower-level error variance.

I've written two helper functions for working with traces. First is to just dump all the output into a pandas dataframe, which makes it super easy to do work on the samples, or write them out to `csv` and assess convergence in R's `coda` package.



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
trace_dataframe = vcsma.trace.to_df()

```
</div>

</div>



the dataframe will have columns containing the elements of the parameters and each row is a single iteration of the sampler:



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
trace_dataframe.head()

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">



<div markdown="0" class="output output_html">
<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Sigma2</th>
      <th>Tau2</th>
      <th>Lambda</th>
      <th>Alphas_0</th>
      <th>Alphas_1</th>
      <th>Alphas_2</th>
      <th>Alphas_3</th>
      <th>Alphas_4</th>
      <th>Alphas_5</th>
      <th>Alphas_6</th>
      <th>...</th>
      <th>Alphas_12</th>
      <th>Alphas_13</th>
      <th>Alphas_14</th>
      <th>Alphas_15</th>
      <th>Betas_0</th>
      <th>Betas_1</th>
      <th>Betas_2</th>
      <th>Betas_3</th>
      <th>Betas_4</th>
      <th>Betas_5</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>31.233393</td>
      <td>0.923435</td>
      <td>-0.047215</td>
      <td>-1.261656</td>
      <td>-0.736935</td>
      <td>-0.399375</td>
      <td>-0.034331</td>
      <td>-2.236596</td>
      <td>-1.213818</td>
      <td>-0.568231</td>
      <td>...</td>
      <td>0.106951</td>
      <td>1.516595</td>
      <td>-1.364607</td>
      <td>2.041536</td>
      <td>10.531876</td>
      <td>-0.483666</td>
      <td>2.109549</td>
      <td>4.480676</td>
      <td>0.003791</td>
      <td>-0.540474</td>
    </tr>
    <tr>
      <th>1</th>
      <td>34.099349</td>
      <td>2.240627</td>
      <td>-0.047215</td>
      <td>-1.842016</td>
      <td>-0.847182</td>
      <td>-0.389802</td>
      <td>-0.111497</td>
      <td>-2.765864</td>
      <td>-2.446336</td>
      <td>-0.447575</td>
      <td>...</td>
      <td>0.798257</td>
      <td>1.826385</td>
      <td>0.221681</td>
      <td>2.458930</td>
      <td>5.712048</td>
      <td>-0.236144</td>
      <td>2.160096</td>
      <td>4.133212</td>
      <td>-0.054797</td>
      <td>10.323832</td>
    </tr>
    <tr>
      <th>2</th>
      <td>32.481750</td>
      <td>2.785222</td>
      <td>-0.047215</td>
      <td>-2.489083</td>
      <td>0.720136</td>
      <td>-1.188099</td>
      <td>-0.501012</td>
      <td>-3.213930</td>
      <td>-2.258950</td>
      <td>-1.216194</td>
      <td>...</td>
      <td>0.859106</td>
      <td>2.192760</td>
      <td>-1.669444</td>
      <td>3.091403</td>
      <td>12.897608</td>
      <td>-0.215380</td>
      <td>1.741864</td>
      <td>3.757071</td>
      <td>-0.011310</td>
      <td>-9.057812</td>
    </tr>
    <tr>
      <th>3</th>
      <td>34.457911</td>
      <td>1.190100</td>
      <td>-0.047215</td>
      <td>-1.201301</td>
      <td>-1.893444</td>
      <td>-0.217819</td>
      <td>-0.681230</td>
      <td>-2.466085</td>
      <td>-1.134824</td>
      <td>-1.307211</td>
      <td>...</td>
      <td>0.386158</td>
      <td>1.437928</td>
      <td>-0.062408</td>
      <td>2.459207</td>
      <td>4.788274</td>
      <td>-0.172863</td>
      <td>1.685140</td>
      <td>3.760042</td>
      <td>-0.049314</td>
      <td>11.777028</td>
    </tr>
    <tr>
      <th>4</th>
      <td>32.185869</td>
      <td>2.298772</td>
      <td>-0.047215</td>
      <td>-1.554065</td>
      <td>-0.884244</td>
      <td>1.800027</td>
      <td>-0.027299</td>
      <td>-2.574601</td>
      <td>-1.991742</td>
      <td>-0.659893</td>
      <td>...</td>
      <td>-0.148268</td>
      <td>1.202387</td>
      <td>-0.822042</td>
      <td>1.747517</td>
      <td>3.763874</td>
      <td>-0.237071</td>
      <td>2.108391</td>
      <td>3.923432</td>
      <td>-0.041574</td>
      <td>15.185345</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 25 columns</p>
</div>
</div>


</div>
</div>
</div>



You can write this out to a csv or analyze it in memory like a typical pandas dataframes:



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
trace_dataframe.mean()

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
Sigma2       32.191602
Tau2          1.875002
Lambda        0.590718
Alphas_0     -1.511708
Alphas_1     -0.091938
Alphas_2     -0.034680
Alphas_3      0.119041
Alphas_4     -2.194331
Alphas_5     -0.865278
Alphas_6     -0.313610
Alphas_7      1.154932
Alphas_8      0.196744
Alphas_9     -0.106956
Alphas_10     1.071748
Alphas_11     0.372573
Alphas_12     0.264176
Alphas_13     1.943292
Alphas_14    -0.562918
Alphas_15     2.167571
Betas_0       8.178978
Betas_1      -0.261140
Betas_2       1.793932
Betas_3       3.974848
Betas_4      -0.006224
Betas_5       2.013807
dtype: float64
```


</div>
</div>
</div>



The second is a method to plot the traces:



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
fig, ax = vcsma.trace.plot()
plt.show()

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">

{:.output_png}
![png](../../images/model/spvcm/using_the_sampler_25_0.png)

</div>
</div>
</div>



The trace object can be sliced by (chain, parameter, index) tuples, or any subset thereof. 



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
vcsma.trace['Lambda',-4:] #last 4 draws of lambda

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
array([0.72462283, 0.72462283, 0.34900417, 0.34900417])
```


</div>
</div>
</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
vcsma.trace[['Tau2', 'Sigma2'], 0:2] #the first 2 variance parameters

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
{'Tau2': [0.923435131177113, 2.240627234434746],
 'Sigma2': [31.23339280347621, 34.09934860150135]}
```


</div>
</div>
</div>



We only ran a single chain, so the first index is assumed to be zero. You can run more than one chain in parallel, using the builtin python `multiprocessing` library:



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
vcsma_p = spvcm.upper_level.Upper_SMA(Y, X, M=W2, Z=Z, 
                                      membership=membership, 
                                      #run 3 chains
                                      n_samples=5000, n_jobs=3, 
                                      configs=dict(tuning=500, 
                                                   adapt_step=1.01))

```
</div>

</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
vcsma_p.trace[0, 'Betas', -1] #the last draw of Beta on the first chain. 

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
array([[ 8.34392377],
       [-0.29268161],
       [ 1.85086248],
       [ 4.0572153 ],
       [ 0.12809572],
       [-2.34258149]])
```


</div>
</div>
</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
vcsma_p.trace[1, 'Betas', -1] #the last draw of Beta on the second chain

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
array([[ 8.12849684],
       [-0.26135619],
       [ 1.43630595],
       [ 4.01361537],
       [ 0.15468895],
       [-4.25558513]])
```


</div>
</div>
</div>



and the chain plotting works also for the multi-chain traces. In addition, there are quite a few traceplot options, and all the plots are returned by the methods as matplotlib objects, so they can also be saved using `plt.savefig()`. 



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
vcsma_p.trace.plot(burn=1000, thin=10)
plt.suptitle('SMA of Homicide Rate in Southern US Counties', y=0, fontsize=20)
#plt.savefig('trace.png') #saves to a file called "trace.png"
plt.show()

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">

{:.output_png}
![png](../../images/model/spvcm/using_the_sampler_34_0.png)

</div>
</div>
</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
vcsma_p.trace.plot(burn=-100, varnames='Lambda') #A negative burn-in works like negative indexing in Python & R 
plt.suptitle('First 100 iterations of $\lambda$', fontsize=20, y=.02)
plt.show() #so this plots Lambda in the first 100 iterations. 

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">

{:.output_png}
![png](../../images/model/spvcm/using_the_sampler_35_0.png)

</div>
</div>
</div>



To get stuff like posterior quantiles, you can use the attendant pandas dataframe functionality, like `describe`. 



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
df = vcsma.trace.to_df()

```
</div>

</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
df.describe()

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">



<div markdown="0" class="output output_html">
<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Sigma2</th>
      <th>Tau2</th>
      <th>Lambda</th>
      <th>Alphas_0</th>
      <th>Alphas_1</th>
      <th>Alphas_2</th>
      <th>Alphas_3</th>
      <th>Alphas_4</th>
      <th>Alphas_5</th>
      <th>Alphas_6</th>
      <th>...</th>
      <th>Alphas_12</th>
      <th>Alphas_13</th>
      <th>Alphas_14</th>
      <th>Alphas_15</th>
      <th>Betas_0</th>
      <th>Betas_1</th>
      <th>Betas_2</th>
      <th>Betas_3</th>
      <th>Betas_4</th>
      <th>Betas_5</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>count</th>
      <td>5000.000000</td>
      <td>5000.000000</td>
      <td>5000.000000</td>
      <td>5000.000000</td>
      <td>5000.000000</td>
      <td>5000.000000</td>
      <td>5000.000000</td>
      <td>5000.000000</td>
      <td>5000.000000</td>
      <td>5000.000000</td>
      <td>...</td>
      <td>5000.000000</td>
      <td>5000.000000</td>
      <td>5000.000000</td>
      <td>5000.000000</td>
      <td>5000.000000</td>
      <td>5000.000000</td>
      <td>5000.000000</td>
      <td>5000.000000</td>
      <td>5000.000000</td>
      <td>5000.000000</td>
    </tr>
    <tr>
      <th>mean</th>
      <td>32.191602</td>
      <td>1.875002</td>
      <td>0.590718</td>
      <td>-1.511708</td>
      <td>-0.091938</td>
      <td>-0.034680</td>
      <td>0.119041</td>
      <td>-2.194331</td>
      <td>-0.865278</td>
      <td>-0.313610</td>
      <td>...</td>
      <td>0.264176</td>
      <td>1.943292</td>
      <td>-0.562918</td>
      <td>2.167571</td>
      <td>8.178978</td>
      <td>-0.261140</td>
      <td>1.793932</td>
      <td>3.974848</td>
      <td>-0.006224</td>
      <td>2.013807</td>
    </tr>
    <tr>
      <th>std</th>
      <td>1.215098</td>
      <td>1.109614</td>
      <td>0.310978</td>
      <td>0.851727</td>
      <td>1.316852</td>
      <td>0.994013</td>
      <td>0.741269</td>
      <td>0.711876</td>
      <td>0.824202</td>
      <td>0.845083</td>
      <td>...</td>
      <td>0.766177</td>
      <td>0.721764</td>
      <td>0.841160</td>
      <td>0.834297</td>
      <td>3.238247</td>
      <td>0.078861</td>
      <td>0.202619</td>
      <td>0.229363</td>
      <td>0.086044</td>
      <td>9.466125</td>
    </tr>
    <tr>
      <th>min</th>
      <td>28.402067</td>
      <td>0.191395</td>
      <td>-0.559725</td>
      <td>-4.727676</td>
      <td>-5.917587</td>
      <td>-3.671202</td>
      <td>-3.125425</td>
      <td>-4.846071</td>
      <td>-4.800286</td>
      <td>-3.748046</td>
      <td>...</td>
      <td>-3.088506</td>
      <td>-0.282006</td>
      <td>-3.737387</td>
      <td>-0.651108</td>
      <td>-1.523421</td>
      <td>-0.567038</td>
      <td>1.083104</td>
      <td>3.093189</td>
      <td>-0.329770</td>
      <td>-29.672208</td>
    </tr>
    <tr>
      <th>25%</th>
      <td>31.350144</td>
      <td>1.131752</td>
      <td>0.396936</td>
      <td>-2.059361</td>
      <td>-0.923023</td>
      <td>-0.692784</td>
      <td>-0.382492</td>
      <td>-2.664186</td>
      <td>-1.400970</td>
      <td>-0.882462</td>
      <td>...</td>
      <td>-0.243498</td>
      <td>1.435780</td>
      <td>-1.129984</td>
      <td>1.588522</td>
      <td>5.942375</td>
      <td>-0.313919</td>
      <td>1.658467</td>
      <td>3.822273</td>
      <td>-0.063075</td>
      <td>-4.347806</td>
    </tr>
    <tr>
      <th>50%</th>
      <td>32.154740</td>
      <td>1.613698</td>
      <td>0.652983</td>
      <td>-1.480018</td>
      <td>-0.099072</td>
      <td>-0.078723</td>
      <td>0.084165</td>
      <td>-2.191222</td>
      <td>-0.870115</td>
      <td>-0.329271</td>
      <td>...</td>
      <td>0.245405</td>
      <td>1.902598</td>
      <td>-0.552477</td>
      <td>2.149598</td>
      <td>8.184837</td>
      <td>-0.260328</td>
      <td>1.794327</td>
      <td>3.974249</td>
      <td>-0.004559</td>
      <td>2.020761</td>
    </tr>
    <tr>
      <th>75%</th>
      <td>33.023853</td>
      <td>2.324573</td>
      <td>0.856933</td>
      <td>-0.939373</td>
      <td>0.718350</td>
      <td>0.599587</td>
      <td>0.583585</td>
      <td>-1.722762</td>
      <td>-0.313782</td>
      <td>0.226628</td>
      <td>...</td>
      <td>0.760613</td>
      <td>2.404884</td>
      <td>-0.009692</td>
      <td>2.697399</td>
      <td>10.406652</td>
      <td>-0.209999</td>
      <td>1.929081</td>
      <td>4.129607</td>
      <td>0.049533</td>
      <td>8.396030</td>
    </tr>
    <tr>
      <th>max</th>
      <td>36.857707</td>
      <td>16.142846</td>
      <td>0.996376</td>
      <td>1.885945</td>
      <td>5.544127</td>
      <td>4.107627</td>
      <td>2.975758</td>
      <td>0.513466</td>
      <td>1.952173</td>
      <td>3.301225</td>
      <td>...</td>
      <td>3.775299</td>
      <td>4.693092</td>
      <td>2.795567</td>
      <td>5.473443</td>
      <td>21.099968</td>
      <td>0.063420</td>
      <td>2.660798</td>
      <td>4.763580</td>
      <td>0.346991</td>
      <td>31.900158</td>
    </tr>
  </tbody>
</table>
<p>8 rows × 25 columns</p>
</div>
</div>


</div>
</div>
</div>



There is also a `trace.summarize` function that will compute various things contained in `spvcm.diagnostics` on the chain. It takes a while for large chains, because the `statsmodels.tsa.AR` estimator is much slower than the `ar` estimator in `R`. If you have rpy2 installed *and* `CODA` installed in your R environment, I attempt to use R directly. 



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
vcsma.trace.summarize()

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">



<div markdown="0" class="output output_html">
<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th></th>
      <th>mean</th>
      <th>HPD_low</th>
      <th>median</th>
      <th>HPD_high</th>
      <th>std</th>
      <th>N_iters</th>
      <th>N_effective</th>
      <th>AR_loss</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th rowspan="25" valign="top">Chain_0</th>
      <th>Sigma2</th>
      <td>32.191602</td>
      <td>29.907175</td>
      <td>32.154740</td>
      <td>34.637546</td>
      <td>1.215098</td>
      <td>5000</td>
      <td>4788</td>
      <td>0.0424</td>
    </tr>
    <tr>
      <th>Tau2</th>
      <td>1.875002</td>
      <td>0.363706</td>
      <td>1.613698</td>
      <td>3.967562</td>
      <td>1.109614</td>
      <td>5000</td>
      <td>1156</td>
      <td>0.7688</td>
    </tr>
    <tr>
      <th>Lambda</th>
      <td>0.590718</td>
      <td>-0.010077</td>
      <td>0.652983</td>
      <td>0.988580</td>
      <td>0.310978</td>
      <td>5000</td>
      <td>243</td>
      <td>0.9514</td>
    </tr>
    <tr>
      <th>Alphas_0</th>
      <td>-1.511708</td>
      <td>-3.261126</td>
      <td>-1.480018</td>
      <td>0.112208</td>
      <td>0.851727</td>
      <td>5000</td>
      <td>558</td>
      <td>0.8884</td>
    </tr>
    <tr>
      <th>Alphas_1</th>
      <td>-0.091938</td>
      <td>-2.717617</td>
      <td>-0.099072</td>
      <td>2.510040</td>
      <td>1.316852</td>
      <td>5000</td>
      <td>2415</td>
      <td>0.5170</td>
    </tr>
    <tr>
      <th>Alphas_2</th>
      <td>-0.034680</td>
      <td>-1.939546</td>
      <td>-0.078723</td>
      <td>1.956138</td>
      <td>0.994013</td>
      <td>5000</td>
      <td>871</td>
      <td>0.8258</td>
    </tr>
    <tr>
      <th>Alphas_3</th>
      <td>0.119041</td>
      <td>-1.240382</td>
      <td>0.084165</td>
      <td>1.660025</td>
      <td>0.741269</td>
      <td>5000</td>
      <td>419</td>
      <td>0.9162</td>
    </tr>
    <tr>
      <th>Alphas_4</th>
      <td>-2.194331</td>
      <td>-3.625861</td>
      <td>-2.191222</td>
      <td>-0.832241</td>
      <td>0.711876</td>
      <td>5000</td>
      <td>419</td>
      <td>0.9162</td>
    </tr>
    <tr>
      <th>Alphas_5</th>
      <td>-0.865278</td>
      <td>-2.595160</td>
      <td>-0.870115</td>
      <td>0.644972</td>
      <td>0.824202</td>
      <td>5000</td>
      <td>398</td>
      <td>0.9204</td>
    </tr>
    <tr>
      <th>Alphas_6</th>
      <td>-0.313610</td>
      <td>-1.913203</td>
      <td>-0.329271</td>
      <td>1.459151</td>
      <td>0.845083</td>
      <td>5000</td>
      <td>303</td>
      <td>0.9394</td>
    </tr>
    <tr>
      <th>Alphas_7</th>
      <td>1.154932</td>
      <td>-0.462574</td>
      <td>1.116507</td>
      <td>2.936222</td>
      <td>0.874826</td>
      <td>5000</td>
      <td>484</td>
      <td>0.9032</td>
    </tr>
    <tr>
      <th>Alphas_8</th>
      <td>0.196744</td>
      <td>-1.471783</td>
      <td>0.157301</td>
      <td>1.876040</td>
      <td>0.875341</td>
      <td>5000</td>
      <td>237</td>
      <td>0.9526</td>
    </tr>
    <tr>
      <th>Alphas_9</th>
      <td>-0.106956</td>
      <td>-1.671481</td>
      <td>-0.119013</td>
      <td>1.397663</td>
      <td>0.780549</td>
      <td>5000</td>
      <td>447</td>
      <td>0.9106</td>
    </tr>
    <tr>
      <th>Alphas_10</th>
      <td>1.071748</td>
      <td>-0.629166</td>
      <td>1.058539</td>
      <td>2.726753</td>
      <td>0.861175</td>
      <td>5000</td>
      <td>497</td>
      <td>0.9006</td>
    </tr>
    <tr>
      <th>Alphas_11</th>
      <td>0.372573</td>
      <td>-1.162294</td>
      <td>0.366974</td>
      <td>1.930433</td>
      <td>0.799864</td>
      <td>5000</td>
      <td>409</td>
      <td>0.9182</td>
    </tr>
    <tr>
      <th>Alphas_12</th>
      <td>0.264176</td>
      <td>-1.130617</td>
      <td>0.245405</td>
      <td>1.871470</td>
      <td>0.766177</td>
      <td>5000</td>
      <td>484</td>
      <td>0.9032</td>
    </tr>
    <tr>
      <th>Alphas_13</th>
      <td>1.943292</td>
      <td>0.589564</td>
      <td>1.902598</td>
      <td>3.395755</td>
      <td>0.721764</td>
      <td>5000</td>
      <td>249</td>
      <td>0.9502</td>
    </tr>
    <tr>
      <th>Alphas_14</th>
      <td>-0.562918</td>
      <td>-2.205367</td>
      <td>-0.552477</td>
      <td>1.125969</td>
      <td>0.841160</td>
      <td>5000</td>
      <td>510</td>
      <td>0.8980</td>
    </tr>
    <tr>
      <th>Alphas_15</th>
      <td>2.167571</td>
      <td>0.555624</td>
      <td>2.149598</td>
      <td>3.804761</td>
      <td>0.834297</td>
      <td>5000</td>
      <td>409</td>
      <td>0.9182</td>
    </tr>
    <tr>
      <th>Betas_0</th>
      <td>8.178978</td>
      <td>1.900055</td>
      <td>8.184837</td>
      <td>14.474289</td>
      <td>3.238247</td>
      <td>5000</td>
      <td>2668</td>
      <td>0.4664</td>
    </tr>
    <tr>
      <th>Betas_1</th>
      <td>-0.261140</td>
      <td>-0.410947</td>
      <td>-0.260328</td>
      <td>-0.101738</td>
      <td>0.078861</td>
      <td>5000</td>
      <td>2513</td>
      <td>0.4974</td>
    </tr>
    <tr>
      <th>Betas_2</th>
      <td>1.793932</td>
      <td>1.384019</td>
      <td>1.794327</td>
      <td>2.176764</td>
      <td>0.202619</td>
      <td>5000</td>
      <td>4310</td>
      <td>0.1380</td>
    </tr>
    <tr>
      <th>Betas_3</th>
      <td>3.974848</td>
      <td>3.508665</td>
      <td>3.974249</td>
      <td>4.408589</td>
      <td>0.229363</td>
      <td>5000</td>
      <td>3408</td>
      <td>0.3184</td>
    </tr>
    <tr>
      <th>Betas_4</th>
      <td>-0.006224</td>
      <td>-0.178816</td>
      <td>-0.004559</td>
      <td>0.162295</td>
      <td>0.086044</td>
      <td>5000</td>
      <td>418</td>
      <td>0.9164</td>
    </tr>
    <tr>
      <th>Betas_5</th>
      <td>2.013807</td>
      <td>-16.324642</td>
      <td>2.020761</td>
      <td>20.862976</td>
      <td>9.466125</td>
      <td>5000</td>
      <td>4064</td>
      <td>0.1872</td>
    </tr>
  </tbody>
</table>
</div>
</div>


</div>
</div>
</div>



So, 5000 iterations, but many parameters have an effective sample size that's much less than this. There's debate about whether it's necesasry to thin these samples in accordance with the effective size, and I think you should thin your sample to the effective size and see if it affects your HPD/Standard Errorrs. 



The existing python packages for MCMC diagnostics were incorrect. So, I've implemented many of the diagnostics from `CODA`, and have verified that the diagnostics comport with `CODA` diagnostics. One can also use `numpy` & `statsmodels` functions. I'll show some types of analysis.



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
from statsmodels.api import tsa
#if you don't have it, try removing the comment and:
#! pip install statsmodels

```
</div>

</div>



For example, a plot of the partial autocorrelation in $\lambda$, the upper-level spatial moving average parameter, over the last half of the chain is:



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
plt.plot(tsa.pacf(vcsma.trace['Lambda', -2500:]))

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
[<matplotlib.lines.Line2D at 0x7fcfe122d7f0>]
```


</div>
</div>
<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">

{:.output_png}
![png](../../images/model/spvcm/using_the_sampler_45_1.png)

</div>
</div>
</div>



So, the chain is close-to-first order:



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
tsa.pacf(df.Lambda)[0:3]

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
array([1.        , 0.90178845, 0.03398422])
```


</div>
</div>
</div>



We could do this for many parameters, too. An Autocorrelation/Partial Autocorrelation plot can be made of the marginal effects by:



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
betas = [c for c in df.columns if c.startswith('Beta')]
f,ax = plt.subplots(len(betas), 2, figsize=(10,8))
for i, col in enumerate(betas):
    ax[i,0].plot(tsa.acf(df[col].values))
    ax[i,1].plot(tsa.pacf(df[col].values)) #the pacf plots take a while
    ax[i,0].set_title(col +' (ACF)')
    ax[i,1].set_title('(PACF)')
f.tight_layout()
plt.show()

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">

{:.output_png}
![png](../../images/model/spvcm/using_the_sampler_49_0.png)

</div>
</div>
</div>



As far as the builtin diagnostics for convergence and simulation quality, the `diagnostics` module exposes a few things:



Geweke statistics for differences in means between chain components:



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
gstats = spvcm.diagnostics.geweke(vcsma, varnames='Tau2') #takes a while
print(gstats)

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">
{:.output_stream}
```
[{'Tau2': array([-0.70525936, -0.86465127, -0.66491713, -1.10260496, -0.85742401,
       -0.57409951, -0.41226321, -1.20085802, -1.45556743, -1.50305192,
       -1.36917624, -1.7651641 , -1.62251801, -1.91653818, -2.95959606,
       -3.25223318, -3.00471879, -1.58320811, -1.49846186, -1.84009018,
       -1.94378006, -1.55312447, -1.74487948, -1.77123135, -1.25633365,
       -1.75786086, -0.88990747, -0.68509239, -0.66391378,  0.32228814,
        0.98220296,  1.03257125,  0.93549226,  0.88218052,  0.41084557,
        0.80814834, -0.23443594,  0.2413701 , -0.73956236, -0.77123872,
       -0.74954084,  0.1017357 , -0.141298  , -0.11990577,  1.05561834,
        1.04085492,  1.58169489,  1.69289289,  2.08680592,  1.98418018])}]
```
</div>
</div>
</div>



Typically, this means the chain is converged at the given "bin" count if the line stays within $\pm2$. The geweke statistic is a test of differences in means between the given chunk of the chain and the remaining chain. If it's outside of +/- 2 in the early part of the chain, you should discard observations early in the chain. If you get extreme values of these statistics throughout, you need to keep running the chain. 



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
plt.plot(gstats[0]['Tau2'][:-1])

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
[<matplotlib.lines.Line2D at 0x7fcfe12a9eb8>]
```


</div>
</div>
<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">

{:.output_png}
![png](../../images/model/spvcm/using_the_sampler_54_1.png)

</div>
</div>
</div>



We can also compute Monte Carlo Standard Errors like in the `mcse` R package, which represent the intrinsic error contained in the estimate:



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
spvcm.diagnostics.mcse(vcsma, varnames=['Tau2', 'Sigma2'])

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
{'Sigma2': 0.01727439579905615, 'Tau2': 0.031562453419661775}
```


</div>
</div>
</div>



Another handy statistic is the Partial Scale Reduction factor, which measures of how likely a set of chains run in parallel have converged to the same stationary distribution. It provides the difference in variance between between chains vs. within chains. 

If these are significantly larger than one (say, 1.5), the chain probably has not converged. Being marginally below $1$ is fine, too.



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
spvcm.diagnostics.psrf(vcsma_p, varnames=['Tau2', 'Sigma2'])

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
{'Tau2': 1.0077401382404925, 'Sigma2': 0.9998141761817744}
```


</div>
</div>
</div>



Highest posterior density intervals provide a kind of interval estimate for parameters in Bayesian models:



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
spvcm.diagnostics.hpd_interval(vcsma, varnames=['Betas', 'Lambda', 'Sigma2'])

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
{'Betas': [(1.9000548460393478, 14.474288717664574),
  (-0.41094673834079987, -0.10173775264997412),
  (1.384018831652215, 2.1767635687081506),
  (3.508665394133376, 4.408589008319321),
  (-0.17881562058023562, 0.16229519966707567),
  (-16.32464174373274, 20.862975934687753)],
 'Sigma2': (29.9071748836272, 34.63754603742357),
 'Lambda': (-0.010077055754050324, 0.9885795446636961)}
```


</div>
</div>
</div>



Sometimes, you want to apply arbitrary functions to each parameter trace. To do this, I've written a `map` function that works like the python builtin `map`. For example, if you wanted to get arbitrary percentiles from the chain:



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
vcsma.trace.map(np.percentile, 
                varnames=['Lambda', 'Tau2', 'Sigma2'],
                #arguments to pass to the function go last
                q=[25, 50, 75]) 

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
[{'Lambda': array([0.39693634, 0.65298256, 0.85693311]),
  'Tau2': array([1.13175212, 1.61369846, 2.32457265]),
  'Sigma2': array([31.35014374, 32.15473988, 33.02385302])}]
```


</div>
</div>
</div>



In addition, you can pop the trace results pretty simply to a `.csv` file and analyze it elsewhere, like if you want to use use the `coda` Bayesian Diagnostics package in `R`. 

To write out a model to a csv, you can use:



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
vcsma.trace.to_csv('./model_run.csv')

```
</div>

</div>



And, you can even load traces from csvs:



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
tr = spvcm.abstracts.Trace.from_csv('./model_run.csv')
print(tr.varnames)
tr.plot(varnames=['Tau2'])

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">
{:.output_stream}
```
['Lambda', 'Sigma2', 'Tau2', 'Alphas', 'Betas']
```
</div>
</div>
<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
(<Figure size 576x144 with 2 Axes>,
 array([[<matplotlib.axes._subplots.AxesSubplot object at 0x7fcfe12fd5f8>,
         <matplotlib.axes._subplots.AxesSubplot object at 0x7fcfe12c5198>]],
       dtype=object))
```


</div>
</div>
<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">

{:.output_png}
![png](../../images/model/spvcm/using_the_sampler_66_2.png)

</div>
</div>
</div>



#  Working with models: `draw` and `sample`

These two functions are used to call the underlying Gibbs sampler. They take no arguments, and operate on the sampler in place. `draw` provides a single new sample:



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
vcsma.draw()

```
</div>

</div>



And sample steps forward an arbitrary number of times:



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
vcsma.sample(10)

```
</div>

</div>



At this point, we did 5000 initial samples and 11 extra samples. Thus:



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
vcsma.cycles

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
5011
```


</div>
</div>
</div>



Parallel models can suspend/resume sampling too:



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
vcsma_p.sample(10)

```
</div>

</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
vcsma_p.cycles

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
5010
```


</div>
</div>
</div>



Under the hood, it's the `draw` method that actually ends up calling one run of `model._iteration`, which is where the actual statistical code lives. Then, it updates all `model.traced_params` by adding their current value in `model.state` to `model.trace.` In addition, `model._finalize` is called the first time sampling is run, which computes some of the constants & derived quantities that save computing time.



# Working with models:  `state`

This is the collection of current values in the sampler. To be efficient, Gibbs sampling must keep around some of the computations used in the simulation, since sometimes the same terms show up in different conditional posteriors. So, the current values of the sampler are stored in `state`.

All of the following are tracked in the state:



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
print(vcsma.state.keys())

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">
{:.output_stream}
```
dict_keys(['X', 'Y', 'M', 'W', 'Delta', 'N', 'J', 'p', 'Sigma2_a0', 'Sigma2_b0', 'Betas_cov0', 'Betas_mean0', 'Tau2_a0', 'Tau2_b0', 'Log_Lambda0', 'Log_Rho0', 'Rho_min', 'Rho_max', 'Lambda_min', 'Lambda_max', 'Betas', 'Alphas', 'Sigma2', 'Tau2', 'Rho', 'Lambda', 'Psi_1', 'Psi_1i', 'Psi_2', 'Psi_2i', 'In', 'Ij', 'Betas_cov0i', 'Betas_covm', 'Sigma2_an', 'Tau2_an', 'PsiRhoi', 'PsiLambdai', 'XtX', 'DeltatDelta', 'DeltaAlphas', 'XBetas', 'initial_values'])
```
</div>
</div>
</div>



If you want to track how something (maybe a hyperparameter) changes over sampling, you can pass `extra_traced_params` to the model declaration:



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
example = spvcm.upper_level.Upper_SMA(Y, X, M=W2, Z=Z, 
                                      membership=membership, 
                                      n_samples=250, 
                                      extra_traced_params = ['DeltaAlphas'],
                                      configs=dict(tuning=500, adapt_step=1.01))
example.trace.varnames

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
['Alphas', 'Betas', 'Sigma2', 'Tau2', 'Lambda', 'DeltaAlphas']
```


</div>
</div>
</div>



# `configs`
this is where configuration options for the various MCMC steps are stored. For multilevel variance components models, these are called $\rho$ for the lower-level error parameter and $\lambda$ for the upper-level parameter. Two exact sampling methods are implemented, Metropolis sampling & Slice sampling. 

Each MCMC step has its own config:



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
vcsma.configs

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
{'Rho': <spvcm.steps.Metropolis at 0x7fcfe1438780>,
 'Lambda': <spvcm.steps.Metropolis at 0x7fcfe1438828>}
```


</div>
</div>
</div>



Since `vcsma` is an upper-level-only model, the `Rho` config is skipped. But, we can look at the `Lambda` config. The number of accepted `lambda` draws is contained in :



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
vcsma.configs.Lambda.accepted

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
725
```


</div>
</div>
</div>



so, the acceptance rate is



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
vcsma.configs.Lambda.accepted / float(vcsma.cycles)

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
0.14468170025942925
```


</div>
</div>
</div>



Also, if you want to get verbose output from the metropolis sampler, there is a "debug" flag:



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
example = spvcm.upper_level.Upper_SMA(Y, X, M=W2, Z=Z, 
                                      membership=membership, 
                                      n_samples=500, 
                                      configs=dict(tuning=250, 
                                                   adapt_step=1.01, 
                                                   debug=True))

```
</div>

</div>



Which stores the information about each iteration in a list, accessible from `model.configs.<parameter>._cache`:



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
example.configs.Lambda._cache[-1] #let's only look at the last one

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
{'jump': 2.1374234835161063,
 'current_logp': array([-8.76422011]),
 'new_logp': array([-8.76422011]),
 'accepted': False}
```


</div>
</div>
</div>



Configuration of the MCMC steps is done using the `config` options dictionary, like done in `spBayes` in `R`. The actual configuration classes exist in spvcm.steps:



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
from pysal.model.spvcm.steps import Metropolis, Slice

```
</div>

</div>



Most of the common options are:

### Metropolis
- `jump`: the starting standard deviation of the proposal distribution
- `tuning`: the number of iterations to tune the scale of the proposal
- `ar_low`: the lower bound of the target acceptance rate range
- `ar_hi`: the upper bound of the target acceptance rate range
- `adapt_step`: a number (bigger than 1) that will be used to modify the jump in order to keep the acceptance rate betwen `ar_lo` and `ar_hi`. Values much larger than `1` result in much more dramatic tuning. 

### Slice
- `width`: starting width of the level set
- `adapt`: number of previous slices use in the weighted average for the next slice. If `0`, the `width` is not dynamically tuned. 



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
example = spvcm.upper_level.Upper_SMA(Y, X, M=W2, Z=Z, 
                                      membership=membership, 
                                      n_samples=500, 
                                      configs=dict(tuning=250, 
                                                   adapt_step=1.01, 
                                      debug=True, ar_low=.1, ar_hi=.4))

```
</div>

</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
example.configs.Lambda.ar_hi, example.configs.Lambda.ar_low

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
(0.4, 0.1)
```


</div>
</div>
</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
example_slicer = spvcm.upper_level.Upper_SMA(Y, X, M=W2, Z=Z, 
                                             membership=membership, 
                                             n_samples=500, 
                                             configs=dict(Lambda_method='slice'))

```
</div>

</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
example_slicer.trace.plot(varnames='Lambda')
plt.show()

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">

{:.output_png}
![png](../../images/model/spvcm/using_the_sampler_97_0.png)

</div>
</div>
</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
example_slicer.configs.Lambda.adapt, example_slicer.configs.Lambda.width

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
(0, 0.5)
```


</div>
</div>
</div>



# Working with models: customization



If you're doing heavy customization, it makes the most sense to first initialize the class without sampling. We did this before when showing how the "extra_traced_params" option worked. 

To show, let's initialize a double-level SAR-Error variance components model, but not actually draw anything.

To do this, you pass the option `n_samples=0`.



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
vcsese = spvcm.both_levels.SESE(Y, X, W=W1, M=W2, Z=Z, 
                                membership=membership, 
                                n_samples=0)

```
</div>

</div>



This sets up a two-level spatial error model with the default uninformative configuration. This means the prior precisions are all `I * .001*`, prior means are all 0, spatial parameters are set to `-1/(n-1)`, and prior scale factors are set arbitrarily. 



### Configs



Options are set by assgning to the relevant property in `model.configs`. 

The model configuration object is another dictionary with a few special methods. 

Configuration options are stored for each parameter separately:



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
vcsese.configs

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
{'Rho': <spvcm.steps.Metropolis at 0x7fcfe13004a8>,
 'Lambda': <spvcm.steps.Metropolis at 0x7fcfe13002b0>}
```


</div>
</div>
</div>



So, for example, if we wanted to turn off adaptation in the upper-level parameter, and fix the Metrpolis jump variance to `.25`:



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
vcsese.configs.Lambda.max_tuning = 0
vcsese.configs.Lambda.jump  = .25

```
</div>

</div>



### Priors



Another thing that might be interesting (though not "bayesian") would be to fix the prior mean of $\beta$ to the OLS estimates. One way this could be done would be to pull the `Delta` matrix out from the state, and estimate:
$$ Y = X\beta + \Delta Z + \epsilon $$
using `PySAL`: 



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
Delta = vcsese.state.Delta
DeltaZ = Delta.dot(Z)
vcsese.state.Betas_mean0 = ps.spreg.OLS(Y, np.hstack((X, DeltaZ))).betas

```
</div>

</div>



### Starting Values



If you wanted to start the sampler at a given starting value, you can do so by assigning that value to the `Lambda` value in `state`. 



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
vcsese.state.Lambda = -.25

```
</div>

</div>



Sometimes, it's suggested that you start the beta vector randomly, rather than at zero. For the parallel sampling, the model starting values are adjusted to induce overdispersion in the start values. 

You could do this manually, too:



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
vcsese.state.Betas += np.random.uniform(-10, 10, size=(vcsese.state.p,1))

```
</div>

</div>



### Spatial Priors



Changing the spatial parameter priors is also done by changing their prior in state. This prior must be a function that takes a value of the parameter and return the log of the prior probability for that value. 

For example, we could assign `P(\lambda) = Beta(2,1)` and zero if outside $(0,1)$, and asign $\rho$ a truncated $\mathcal{N}(0,.5)$ prior by first defining their functional form:



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
from scipy import stats

```
</div>

</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
def Lambda_prior(val):
    if (val < 0) or (val > 1):
        return -np.inf
    return np.log(stats.beta.pdf(val, 2,1))

```
</div>

</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
def Rho_prior(val):
    if (val > .5) or (val < -.5):
        return -np.inf
    return np.log(stats.truncnorm.pdf(val, -.5, .5, loc=0, scale=.5))

```
</div>

</div>



And then assigning to their symbols, `LogLambda0` and `LogRho0` in the state:



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
vcsese.state.LogLambda0 = Lambda_prior
vcsese.state.LogRho0 = Rho_prior

```
</div>

</div>



### Performance



The efficiency of the sampler is contingent on the lower-level size. If we were to estimate the draw in a dual-level SAR-Error Variance Components iteration:



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
%timeit vcsese.draw()

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">
{:.output_stream}
```
26 ms ± 2.37 ms per loop (mean ± std. dev. of 7 runs, 10 loops each)
```
</div>
</div>
</div>



To make it easy to work with the model, you can interrupt and resume sampling using keyboard interrupts (`ctrl-c` or the `stop` button in the notebook). 



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
%time vcsese.sample(100)

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">
{:.output_stream}
```
CPU times: user 10.4 s, sys: 148 ms, total: 10.5 s
Wall time: 2.64 s
```
</div>
</div>
</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
vcsese.sample(10)

```
</div>

</div>



# Under the Hood



### Package Structure



Most of the tools in the package are stored in relevant python files in the top level or a dedicated subfolder. Explaining a few:

- `abstracts.py` - the abstract class machinery to iterate over a sampling loop. This is where the classes are defined, like `Trace`, `Sampler_Mixin`, or `Hashmap`. 
- `plotting.py` - tools for plotting output
- `steps.py` - the step method definitions
- `verify.py` - like `user` checks in `pysal.spreg`, this contains a few sanity checks. 
- `utils.py`- contains statistical or numerical utilities to make the computation easier, like cholesky multivariate normal sampling, more sparse utility functions, etc. 
- `diagnostics.py` - all the diagnostics
- `priors.py` - definitions of alternative prior forms. Right now, this is pretty simple. 
- `sqlite.py` - functions to use a sqlite database instead of an in-memory chain are defined here. 



### The implementation of a Model

The package is implemented so that every "model type" first sends off to the `spvcm.both.Base_Generic`, which sets up the state, trace, and priors. 

Models are added by writing a `model.py` file and possibly a `sample.py` file. The `model.py` file defines a `Base/User` class pair (like `spreg`) that sets up the state and trace. It must define hyperparameters, and can precompute objects used in the sampling loop. The base class should inherit from `Sampler_Mixin`, which defines all of the machinery of sampling. 

The loop through the conditional posteriors should be defined in `model.py`, in the `model._iteration` function. This should update the model state in place.

The model may also define a `_finalize` function which is run once before sampling. 

So, if I write a new model, like a varying-intercept model with endogenously-lagged intercepts, I would write a `model.py` containing something like:
```python

class Base_VISAR(spvcm.generic.Base_Generic):
    def __init__(self, Y, X, M, membership=None, Delta=None,
                 extra_traced_params=None, #record extra things in state
                 n_samples=1000, n_jobs=1, #sampling config
                 priors = None, # dict with prior values for params
                 configs=None, # dict with configs for MCMC steps
                 starting_values=None, # dict with starting values
                 truncation=None, # options to truncate MCMC step priors
                 center=False, # Whether to center the X,Z matrices
                 scale=False # Whether re-scale the X,Z matrices
                 ):
        super(Base_VISAR, self).__init__(self, Y, X, M, W=None,
                                         membership=membership,
                                         Delta=Delta,
                                         n_samples=0, n_jobs=n_jobs,
                                         priors=priors, configs=configs,
                                         starting_values=starting_values,
                                         truncation=truncation,
                                         center=center,
                                         scale=scale
                                         )
        self.sample(n_samples, n_jobs=n_jobs)
        
        def _finalize(self):
            # the degrees of freedom of the variance parameter is constant
            self.state.Sigma2_an = self.state.N/2 + self.state.Sigma2_a0
            ...
        
        def _iteration(self):
            
            # computing the values needed to sample from the conditional posteriors
            mean = spdot(X.T, spdot(self.PsiRhoi, X)) / Sigma2 + self.state.bmean0
            ...
    ...
```
I've organized the directories in this project into `both_levels`, `upper_level`, `lower_level`, and `hierarchical`, which contains some of the spatially-varying coefficient models & other models I'm working on that are unrelated to the multilevel variance components stuff. 



Since most of the `_iteration` loop is the same between models, most of the models share the same sampling code, but customize the structure of the covariance in each level. These covariance variables are stored in the `state.Psi_1`, for the lower-level covariance, and `state.Psi_2` for the upper-level covariance. Likewise, the precision functions are `state.Psi_1i` and `state.Psi_2i`. 

For example:



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
vcsese.state.Psi_1 #lower-level covariance

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
<function spvcm.utils.se_covariance(param, W, sparse=False)>
```


</div>
</div>
</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
vcsese.state.Psi_2 #upper-level covariance

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
<function spvcm.utils.se_covariance(param, W, sparse=False)>
```


</div>
</div>
</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
vcsma.state.Psi_2 #upper-level covariance

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
<function spvcm.utils.sma_covariance(param, W, sparse=True)>
```


</div>
</div>
</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
vcsma.state.Psi_2i

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
<function spvcm.utils.sma_precision(param, W, sparse=False)>
```


</div>
</div>
</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
vcsma.state.Psi_1

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
<function spvcm.utils.ind_covariance(param, W, sparse=False)>
```


</div>
</div>
</div>



The functions that generate the covariance matrices are stored in `spvcm.utils`. They can be arbitrarily overwritten for alternative covariance specifications. 

Thus, if we want to sample a model with a new covariance specification, then we need to define functions for the variance and precision.


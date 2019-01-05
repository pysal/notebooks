---
redirect_from:
  - "/model/spint/glm-speed"
interact_link: content/model/spint/glm_speed.ipynb
title: 'glm_speed'
prev_page:
  url: /model/spint/dispersion_test
  title: 'dispersion_test'
next_page:
  url: /model/spint/netW
  title: 'netW'
comment: "***PROGRAMMATICALLY GENERATED, DO NOT EDIT. SEE ORIGINAL FILES IN /content***"
---



{:.input_area}
```python
import numpy as np
import pandas as pd
from spint.gravity import Gravity, Production, Attraction, Doubly, BaseGravity
#from entropy import Unconstrained, ProductionConstrained, AttractionConstrained, DoublyConstrained
import statsmodels.formula.api as smf
from statsmodels.api import families
import matplotlib.pyplot as plt
%pylab inline

import time                                                

def timeit(method):

    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        elapsed = te-ts
        
        return result, elapsed

    return timed
```




{:.input_area}
```python
@timeit
def gravity(f ,o, d, o_vars, d_vars, dij, cost='exp', framework='glm'):
    results = Gravity(f, o_vars, d_vars, dij, cost, framework=framework)
    return results
    
@timeit    
def production(f ,o, d, o_vars, d_vars, dij, cost='exp', framework='glm'):
    results = Production(f, o, d_vars, dij, 'exp', framework=framework)
    return results

@timeit    
def attraction(f ,o, d, o_vars, d_vars, dij, cost='exp', framework='glm'):
    results = Attraction(f, d, o_vars, dij, 'exp', framework=framework)
    return results

@timeit    
def doubly(f ,o, d, o_vars, d_vars, dij, cost='exp', framework='glm'):
    results = Doubly(f, o, d, dij, 'exp', framework=framework)
    return results


```




{:.input_area}
```python
def sim_data(n):
    o = np.tile(np.arange(n),n)
    d = np.repeat(np.arange(n),n)
    loc_size = np.random.randint(25000,500000, n)
    o_vars = np.tile(loc_size, n)
    d_vars = np.repeat(loc_size, n)
    dij = np.random.exponential(2500, n**2)
    f = o_vars**.3*d_vars**.4*np.exp(dij*-.00005)
    o = np.reshape(o, (-1,1))
    d = np.reshape(d, (-1,1))
    o_vars = np.reshape(o_vars, (-1,1))
    d_vars = np.reshape(d_vars, (-1,1))
    dij = np.reshape(dij, (-1,1))
    f = np.reshape(f, (-1,1))
    f = f.astype(np.int64)
    return f, o, d, o_vars, d_vars, dij

```




{:.input_area}
```python
def loop(func, start, stop, step, framework='glm'):
    results = []
    for n in np.arange(start, stop, step):
        f, o, d, o_vars, d_vars, dij = sim_data(n)
        out, elapsed = func(f, o, d, o_vars, d_vars, dij, 'exp', framework=framework)
        print(out.params[-2:])
        results.append(elapsed)
    return results
```




{:.input_area}
```python
glm_grav = loop(gravity, 50, 250, 50)
glm_prod = loop(production, 50, 250, 50)
glm_att = loop(attraction, 50, 250, 50)
glm_doub = loop(doubly, 50, 250, 50)
```




{:.input_area}
```python
smglm_grav = loop(gravity, 50, 250, 50, framework='sm_glm')
smglm_prod = loop(production, 50, 250, 50, framework='sm_glm')
smglm_att = loop(attraction, 50, 250, 50, framework='sm_glm')
smglm_doub = loop(doubly, 50, 250, 50, framework='sm_glm')
```




{:.input_area}
```python
x = np.arange(50, 250, 50)
```




{:.input_area}
```python
plt.plot(x, glm_grav, x, glm_prod, x, glm_att, x, glm_doub)
plt.legend(('unconstrained', 'production', 'attraction', 'doubly'))
plt.title('Custom GLM Framework')
plt.xlabel('Sample Size')
plt.ylabel('Seconds')
```




{:.input_area}
```python
plt.plot(x, smglm_grav, x, smglm_prod, x, smglm_att, x, smglm_doub)
plt.legend(('unconstrained', 'production', 'attraction', 'doubly'))
plt.legend(('unconstrained', 'production', 'attraction', 'doubly'))
plt.title('Statsmodels GLM Framework')
plt.xlabel('Sample Size')
plt.ylabel('Seconds')
```




{:.input_area}
```python
f, o, d, o_vars, d_vars, dij = sim_data(100)
test = Production(f, o, d_vars, dij, 'exp')
```




{:.input_area}
```python
test.
```


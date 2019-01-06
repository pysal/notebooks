---
redirect_from:
  - "/model/spint/test-grav"
interact_link: content/model/spint/test_grav.ipynb
title: 'test_grav'
prev_page:
  url: /model/spint/sparse_categorical
  title: 'sparse_categorical'
next_page:
  url: /model/spint/sparse_grav
  title: 'sparse_grav'
comment: "***PROGRAMMATICALLY GENERATED, DO NOT EDIT. SEE ORIGINAL FILES IN /content***"
---



{:.input_area}
```python
import numpy as np
import pandas as pd
import os
os.chdir('../')
from gravity import Gravity, Production, Attraction, Doubly, BaseGravity
import statsmodels.formula.api as smf
from statsmodels.api import families
import matplotlib.pyplot as plt
%pylab inline
```


{:.output_stream}
```
Populating the interactive namespace from numpy and matplotlib

```



{:.input_area}
```python

n = 3000
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
```




{:.input_area}
```python
%time Gravity(f, o_vars, d_vars, dij, 'exp')
```


{:.output_stream}
```
CPU times: user 14.3 s, sys: 1.46 s, total: 15.8 s
Wall time: 7.41 s

```




{:.output_data_text}
```
<gravity.Gravity at 0x118346850>
```





{:.input_area}
```python
%time Production(f, o, d_vars, dij, 'exp')
```


{:.output_stream}
```
CPU times: user 38.3 s, sys: 4 s, total: 42.3 s
Wall time: 24.6 s

```




{:.output_data_text}
```
<gravity.Production at 0x118353510>
```





{:.input_area}
```python
%time Attraction(f, d, o_vars, dij, 'exp')
```


{:.output_stream}
```
CPU times: user 36 s, sys: 4.25 s, total: 40.2 s
Wall time: 21.4 s

```




{:.output_data_text}
```
<gravity.Attraction at 0x118353310>
```





{:.input_area}
```python
%time Doubly(f, o, d, dij, 'exp')
```


{:.output_stream}
```
CPU times: user 1min 19s, sys: 6.3 s, total: 1min 25s
Wall time: 37.4 s

```




{:.output_data_text}
```
<gravity.Doubly at 0x118353250>
```





{:.input_area}
```python
from glm import GLM
from iwls import iwls
import line_profiler
import IPython
ip = IPython.get_ipython()
ip.define_magic('lprun', line_profiler.magic_lprun)
instance = Production(f, o, d_vars, dij, 'exp')

```




{:.input_area}
```python
%lprun -f BaseGravity.__init__ instance.__init__(f, o, d_vars, dij, 'exp')
```


{:.output_stream}
```
correct sparse

```



{:.input_area}
```python
glm_inst = GLM(instance.y, instance.X, family=families.Poisson())
%lprun -f GLM.__init__ glm_inst.__init__(instance.y, instance.X, family=families.Poisson())
```




{:.input_area}
```python
%lprun -f iwls iwls(instance.y, instance.X, family=families.Poisson(), offset=None, y_fix=None)
```


---
redirect_from:
  - "/viz/splot/moran-bv-test"
interact_link: content/viz/splot/moran_bv_test.ipynb
title: 'moran_bv_test'
prev_page:
  url: /viz/splot/intro
  title: 'splot'
next_page:
  url: /viz/splot/esda_moran_matrix_viz
  title: 'esda_moran_matrix_viz'
comment: "***PROGRAMMATICALLY GENERATED, DO NOT EDIT. SEE ORIGINAL FILES IN /content***"
---



{:.input_area}
```python
%matplotlib inline

import matplotlib.pyplot as plt
import pysal as ps
import libpysal.api as lp
import numpy as np
import pandas as pd
import geopandas as gpd
import os
import splot

from libpysal import examples

from importlib import reload
```


## Example Data

First, we will load the Guerry.shp data from `examples` in `libpysal`.



{:.input_area}
```python
f = lp.open(lp.get_path("sids2.dbf"))

varnames = ['SIDR74',  'SIDR79',  'NWR74',  'NWR79']
vars = [np.array(f.by_col[var]) for var in varnames]

w = lp.open(lp.get_path("sids2.gal")).read()

from esda.moran import Moran_BV_matrix
moran_matrix = Moran_BV_matrix(vars,  w,  varnames = varnames)
```




{:.input_area}
```python
len(moran_matrix)
moran_matrix[(0,  1)].varnames
moran_matrix[(0,1)].varnames['x']
```





{:.output_data_text}
```
'SIDR74'
```





{:.input_area}
```python
from splot._viz_esda_mpl import moran_facette
from importlib import reload

reload(splot._viz_esda_mpl)
from splot._viz_esda_mpl import moran_facette
```




{:.input_area}
```python
fig, axarr = moran_facette(moran_matrix)
plt.show()
```



![png](../../images/viz/splot/moran_bv_test_5_0.png)


### Moran_Tests



{:.input_area}
```python
import geopandas
from shapely.geometry import Polygon
import random
import matplotlib
```




{:.input_area}
```python
link_to_data = examples.get_path('Guerry.shp')
gdf = gpd.read_file(link_to_data)
```




{:.input_area}
```python
y = gdf['Donatns'].values
x = gdf['Suicids'].values
w = lp.Queen.from_dataframe(gdf)
w.transform = 'r'
```




{:.input_area}
```python
from splot.esda import moran_scatterplot
from esda.moran import (Moran, Moran_BV, Moran_Local,
                        Moran_Local_BV)
```




{:.input_area}
```python
moran = Moran(y,w)
moran_bv = Moran_BV(y, x, w)
moran_loc = Moran_Local(y, w)
moran_loc_bv = Moran_Local_BV(y, x, w)
```




{:.input_area}
```python
fig, axs = plt.subplots(2, 2, figsize=(10,10),
                        subplot_kw={'aspect': 'equal'})

moran_scatterplot(moran, p=0.05, ax=axs[0,0])
moran_scatterplot(moran_loc, p=0.05, ax=axs[1,0])
moran_scatterplot(moran_bv, p=0.05, ax=axs[0,1])
moran_scatterplot(moran_loc_bv, p=0.05, ax=axs[1,1])
plt.show()
```



![png](../../images/viz/splot/moran_bv_test_12_0.png)


### VBA



{:.input_area}
```python
from splot.mapping import vba_choropleth, value_by_alpha_cmap
```




{:.input_area}
```python
fig, ax = vba_choropleth(x, y, gdf)
plt.show()
```



![png](../../images/viz/splot/moran_bv_test_15_0.png)




{:.input_area}
```python
import libpysal
from libpysal import examples
```



{:.output_traceback_line}
```
---------------------------------------------------------------------------
```

{:.output_traceback_line}
```
ModuleNotFoundError                       Traceback (most recent call last)
```

{:.output_traceback_line}
```
<ipython-input-1-ce16f54df5e0> in <module>()
----> 1 import libpysal
      2 from libpysal import examples

```

{:.output_traceback_line}
```
~/code/libpysal/libpysal/__init__.py in <module>()
     26 """
     27 from . import cg
---> 28 from . import io
     29 from . import weights
     30 from . import examples

```

{:.output_traceback_line}
```
~/code/libpysal/libpysal/io/__init__.py in <module>()
      1 from . import fileio
      2 from .tables import *
----> 3 from .iohandlers import *
      4 from .util import *
      5 open = fileio.FileIO

```

{:.output_traceback_line}
```
ModuleNotFoundError: No module named 'libpysal.io.iohandlers'
```


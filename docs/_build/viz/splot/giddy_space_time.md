---
redirect_from:
  - "/viz/splot/giddy-space-time"
interact_link: content/viz/splot/giddy_space_time.ipynb
kernel_name: python3
has_widgets: false
title: 'giddy_space_time'
prev_page:
  url: /viz/splot/esda_morans_viz
  title: 'esda_morans_viz'
next_page:
  url: /viz/splot/mapping_vba
  title: 'mapping_vba'
comment: "***PROGRAMMATICALLY GENERATED, DO NOT EDIT. SEE ORIGINAL FILES IN /content***"
---


# Space-time visualisations (giddy)



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
from pysal.lib.weights.contiguity import Queen
from pysal.lib import examples
import geopandas as gpd
import pandas as pd
import numpy as np
from pysal.explore.giddy.directional import Rose
import matplotlib.pyplot as plt
from pysal.explore import esda
from pysal.viz.splot.esda import lisa_cluster

from ipywidgets import interact, fixed
import ipywidgets as widgets

%matplotlib inline
plt.style.use('ggplot')

```
</div>

</div>



## Data prepration



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
# get csv and shp and merge
shp_link = examples.get_path('us48.shp')
df = gpd.read_file(shp_link)
income_table = pd.read_csv(examples.get_path("usjoin.csv"))

```
</div>

</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
# calculate relative values
for year in range(1969, 2010):
    income_table[str(year) + '_rel'] = income_table[str(year)] / income_table[str(year)].mean()

```
</div>

</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
# merge
gdf = df.merge(income_table,left_on='STATE_NAME',right_on='Name')

```
</div>

</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
#retrieve spatial weights and data for two points in time
w = Queen.from_dataframe(gdf)
w.transform = 'r'
y1 = gdf['1969_rel'].values
y2 = gdf['2000_rel'].values

```
</div>

</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
# create rose object
Y = np.array([y1, y2]).T
rose = Rose(Y, w, k=5)

```
</div>

</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
# calculate Moran_Local
moran_loc1 = esda.moran.Moran_Local(y1, w)
moran_loc2 = esda.moran.Moran_Local(y2, w)

```
</div>

</div>



## Plotting



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
from pysal.viz.splot.giddy import (dynamic_lisa_heatmap,
                         dynamic_lisa_rose,
                         dynamic_lisa_vectors,
                         dynamic_lisa_composite,
                         dynamic_lisa_composite_explore)
from pysal.viz import splot

```
</div>

</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
fig, ax = dynamic_lisa_heatmap(rose)
ax.set_ylabel(1996)
ax.set_xlabel(2006)
plt.show()

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">

{:.output_png}
![png](../../images/viz/splot/giddy_space_time_11_0.png)

</div>
</div>
</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
fig, ax = dynamic_lisa_rose(rose, attribute=y1)
plt.show()

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">

{:.output_png}
![png](../../images/viz/splot/giddy_space_time_12_0.png)

</div>
</div>
</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
fig, ax = dynamic_lisa_vectors(rose)

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">

{:.output_png}
![png](../../images/viz/splot/giddy_space_time_13_0.png)

</div>
</div>
</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
dynamic_lisa_composite(rose, gdf)
plt.show()

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">

{:.output_png}
![png](../../images/viz/splot/giddy_space_time_14_0.png)

</div>
</div>
</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
dynamic_lisa_composite_explore(rose, gdf, pattern='rel')
plt.show()

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">
{:.output_data_text}
```
interactive(children=(Dropdown(description='start_time', options={'1969_rel': '1969_rel', '1970_rel': '1970_re…
```

</div>
</div>
</div>


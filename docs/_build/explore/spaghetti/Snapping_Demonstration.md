---
redirect_from:
  - "/explore/spaghetti/snapping-demonstration"
interact_link: content/explore/spaghetti/Snapping_Demonstration.ipynb
kernel_name: conda-env-py3_spgh_dev-py
has_widgets: false
title: 'Snapping_Demonstration'
prev_page:
  url: /explore/spaghetti/Facility_Location
  title: 'Facility_Location'
next_page:
  url: /explore/spaghetti/Network_Usage
  title: 'Network_Usage'
comment: "***PROGRAMMATICALLY GENERATED, DO NOT EDIT. SEE ORIGINAL FILES IN /content***"
---


--------------------------



# Snapping point to segments



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
import os
last_modified = None
if os.name == "posix":
    last_modified = !stat -f\
                    "# This notebook was last updated: %Sm"\
                     Snapping_Demonstration.ipynb
elif os.name == "nt":
    last_modified = !for %a in (Snapping_Demonstration.ipynb)\
                    do echo # This notebook was last updated: %~ta
    
if last_modified:
    get_ipython().set_next_input(last_modified[-1])

```
</div>

</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
# This notebook was last updated: May 13 20:04:46 2019

```
</div>

</div>



-------------------------------



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
import numpy as np
from pysal.lib import examples
import geopandas as gpd
from pysal.explore import spaghetti as spgh
from shapely.geometry import Point

%matplotlib inline

__author__ = 'James Gaboardi <jgaboardi@gmail.com>'

```
</div>

</div>



-----------------------------------------



## Segments



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
streets = examples.get_path("streets.shp")
streets = gpd.read_file(streets)

```
</div>

</div>



## Points



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
crimes = examples.get_path("crimes.shp")
crimes = gpd.read_file(crimes)
np.random.seed(1)
crimes['geometry'] = np.random.permutation(crimes['geometry'])

```
</div>

</div>



## Initial plot



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
base = streets.plot(figsize=(10,10), color='k', alpha=.35, linewidth=3)
crimes.plot(ax=base, cmap='tab20', markersize=75)

```
</div>

</div>



# Network



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
net = spgh.Network(in_data=streets)

```
</div>

</div>



## Snap point onto nearest segments



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
net.snapobservations(crimes, 'crimes')

```
</div>

</div>



## Create `geopandas.GeoDataFrame` objects of snapped points



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
snapped_gdf = spgh.element_as_gdf(net, pp_name='crimes', snapped=True)

```
</div>

</div>



## Original point coordinates, snapped point coordinates



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
original = net.pointpatterns['crimes'].points
print(original[0]['coordinates'], snapped_gdf.geometry[0].coords[:])

```
</div>

</div>



## Snapped points plot



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
base = streets.plot(figsize=(10,10), color='k', alpha=.35, linewidth=3)
crimes.plot(ax=base, cmap='tab20', markersize=75)
snapped_gdf.plot(ax=base, cmap='tab20', markersize=30)

```
</div>

</div>



---------------------------------------------


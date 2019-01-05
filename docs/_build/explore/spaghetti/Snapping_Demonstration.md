---
redirect_from:
  - "/explore/spaghetti/snapping-demonstration"
interact_link: content/explore/spaghetti/Snapping_Demonstration.ipynb
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



{:.input_area}
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




{:.input_area}
```python
# This notebook was last updated: Dec  9 13:07:52 2018
```


-------------------------------



{:.input_area}
```python
import numpy as np
from libpysal import examples
import geopandas as gpd
import spaghetti as spgh
from shapely.geometry import Point

%matplotlib inline

__author__ = 'James Gaboardi <jgaboardi@gmail.com>'
```


-----------------------------------------

## Segments



{:.input_area}
```python
streets = examples.get_path("streets.shp")
streets = gpd.read_file(streets)
```


## Points



{:.input_area}
```python
crimes = examples.get_path("crimes.shp")
crimes = gpd.read_file(crimes)
np.random.seed(1)
crimes['geometry'] = np.random.permutation(crimes['geometry'])
```


## Initial plot



{:.input_area}
```python
base = streets.plot(figsize=(10,10), color='k', alpha=.35, linewidth=3)
crimes.plot(ax=base, cmap='tab20', markersize=75)
```


# Network



{:.input_area}
```python
net = spgh.Network(in_data=streets)
```


## Snap point onto nearest segments



{:.input_area}
```python
net.snapobservations(crimes, 'crimes')
```


## Create `geopandas.GeoDataFrame` objects of snapped points



{:.input_area}
```python
snapped_gdf = spgh.element_as_gdf(net, pp_name='crimes', snapped=True)
```


## Original point coordinates, snapped point coordinates



{:.input_area}
```python
original = net.pointpatterns['crimes'].points
print(original[0]['coordinates'], snapped_gdf.geometry[0].coords[:])
```


## Snapped points plot



{:.input_area}
```python
base = streets.plot(figsize=(10,10), color='k', alpha=.35, linewidth=3)
crimes.plot(ax=base, cmap='tab20', markersize=75)
snapped_gdf.plot(ax=base, cmap='tab20', markersize=30)
```


---------------------------------------------

---
redirect_from:
  - "/explore/spaghetti/spaghetti-pointpatterns-empirical"
interact_link: content/explore/spaghetti/Spaghetti_Pointpatterns_Empirical.ipynb
kernel_name: conda-env-py3_spgh_dev-py
has_widgets: false
title: 'Spaghetti_Pointpatterns_Empirical'
prev_page:
  url: /explore/spaghetti/intro
  title: 'spaghetti'
next_page:
  url: /explore/spaghetti/Facility_Location
  title: 'Facility_Location'
comment: "***PROGRAMMATICALLY GENERATED, DO NOT EDIT. SEE ORIGINAL FILES IN /content***"
---


---------------------------------------



# $SPA$tial $G$rap$H$s: n$ET$works, $T$opology, & $I$nference

## Tutorial for `pysal.spaghetti`: Working with point patterns: empirical observations
#### James D. Gaboardi [<jgaboardi@fsu.edu>]



1. Instantiating a `pysal.spaghetti.Network`
2. Allocating observations to a network
    * snapping
3. Visualizing original and snapped locations
    * visualization with `geopandas` and `matplotlib`



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
import os
last_modified = None
if os.name == "posix":
    last_modified = !stat -f\
                    "# This notebook was last updated: %Sm"\
                     Spaghetti_Pointpatterns_Empirical.ipynb
elif os.name == "nt":
    last_modified = !for %a in (Spaghetti_Pointpatterns_Empirical.ipynb)\
                    do echo # This notebook was last updated: %~ta
    
if last_modified:
    get_ipython().set_next_input(last_modified[-1])

```
</div>

</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
# This notebook was last updated: Dec  9 14:23:58 2018

```
</div>

</div>



-----------------



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
from pysal.explore import spaghetti as spgh
from pysal.lib import examples
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from shapely.geometry import Point, LineString

%matplotlib inline

__author__ = "James Gaboardi <jgaboardi@gmail.com>"

```
</div>

</div>



# 1. Instantiating a `pysal.spaghetti.Network`
### Instantiate the network from `.shp` file



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
ntw = spgh.Network(in_data=examples.get_path('streets.shp'))

```
</div>

</div>



# 2. Allocating observations to a network
### Snap point patterns to the network



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
# Crimes with attributes
ntw.snapobservations(examples.get_path('crimes.shp'),
                     'crimes',
                     attribute=True)

# Schools without attributes
ntw.snapobservations(examples.get_path('schools.shp'),
                     'schools',
                     attribute=False)

```
</div>

</div>



# 3. Visualizing original and snapped locations



## True and snapped school locations



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
schools_df = spgh.element_as_gdf(ntw,
                                 pp_name='schools',
                                 snapped=False)

snapped_schools_df = spgh.element_as_gdf(ntw,
                                         pp_name='schools',
                                         snapped=True)

```
</div>

</div>



## True and snapped crime locations



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
crimes_df = spgh.element_as_gdf(ntw,
                                pp_name='crimes',
                                snapped=False)

snapped_crimes_df = spgh.element_as_gdf(ntw,
                                        pp_name='crimes',
                                        snapped=True)

```
</div>

</div>



## Create `geopandas.GeoDataFrame` objects of the vertices and arcs



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
# network nodes and edges
vertices_df, arcs_df = spgh.element_as_gdf(ntw,
                                           vertices=True,
                                           arcs=True)

```
</div>

</div>



## Plotting `geopandas.GeoDataFrame` objects



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
# legend patches
arcs = mlines.Line2D([], [], color='k', label='Network Arcs', alpha=.5)
vtxs = mlines.Line2D([], [], color='k', linewidth=0, markersize=2.5,
                     marker='o', label='Network Vertices', alpha=1)
schl = mlines.Line2D([], [], color='k', linewidth=0, markersize=25,
                     marker='X', label='School Locations', alpha=1)
snp_schl = mlines.Line2D([], [], color='k', linewidth=0, markersize=12,
                         marker='o', label='Snapped Schools', alpha=1)
crme = mlines.Line2D([], [], color='r', linewidth=0, markersize=7,
                     marker='x', label='Crime Locations', alpha=.75)
snp_crme = mlines.Line2D([], [], color='r', linewidth=0, markersize=3,
                         marker='o', label='Snapped Crimes', alpha=.75)

patches = [arcs, vtxs, schl, snp_schl, crme, snp_crme]

```
</div>

</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
# plot figure
base = arcs_df.plot(color='k', alpha=.25, figsize=(12,12), zorder=0)
vertices_df.plot(ax=base, color='k', markersize=5, alpha=1)

crimes_df.plot(ax=base, color='r', marker='x',
               markersize=50, alpha=.5, zorder=1)
snapped_crimes_df.plot(ax=base, color='r',
                       markersize=20, alpha=.5, zorder=1)

schools_df.plot(ax=base, cmap='tab20', column='id', marker='X',
                markersize=500, alpha=.5, zorder=2)
snapped_schools_df.plot(ax=base,cmap='tab20', column='id',
                        markersize=200, alpha=.5, zorder=2)

# add legend
plt.legend(handles=patches, fancybox=True, framealpha=0.8,
           scatterpoints=1, fontsize="xx-large", bbox_to_anchor=(1.04, .6))

```
</div>

</div>



-----------


---
redirect_from:
  - "/explore/spaghetti/network-usage"
interact_link: content/explore/spaghetti/Network_Usage.ipynb
kernel_name: conda-env-py3_spgh_dev-py
has_widgets: false
title: 'Network_Usage'
prev_page:
  url: /explore/spaghetti/Snapping_Demonstration
  title: 'Snapping_Demonstration'
next_page:
  url: /explore/segregation/intro
  title: 'segregation'
comment: "***PROGRAMMATICALLY GENERATED, DO NOT EDIT. SEE ORIGINAL FILES IN /content***"
---


-------------------



## Basic Tutorial for `pysal.spaghetti`



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
import os
last_modified = None
if os.name == "posix":
    last_modified = !stat -f\
                    "# This notebook was last updated: %Sm"\
                     Network_Usage.ipynb
elif os.name == "nt":
    last_modified = !for %a in (Network_Usage.ipynb)\
                    do echo # This notebook was last updated: %~ta
    
if last_modified:
    get_ipython().set_next_input(last_modified[-1])

```
</div>

</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
# This notebook was last updated: May 13 20:21:51 2019

```
</div>

</div>



--------------------------



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
# pysal submodule imports
from pysal.lib import examples
from pysal.explore import spaghetti as spgh
from pysal.explore import esda

import numpy as np
import matplotlib.pyplot as plt

import time

%matplotlib inline

__author__ = "James Gaboardi <jgaboardi@gmail.com>"

```
</div>

</div>



### Instantiate a network



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
ntw = spgh.Network(in_data=examples.get_path('streets.shp'))

```
</div>

</div>



### Snap point patterns to the network



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
# Crimes
ntw.snapobservations(examples.get_path('crimes.shp'),
                     'crimes',
                     attribute=True)
# Schools
ntw.snapobservations(examples.get_path('schools.shp'),
                     'schools',
                     attribute=False)

```
</div>

</div>



### A network is composed of a single topological representation of roads and $n$ point patterns which are snapped to the network.



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
ntw.pointpatterns

```
</div>

</div>



### Attributes for every point pattern



1. `dist_snapped` dict keyed by pointid with the value as snapped distance from observation to network arc
2. `dist_to_vertex` dict keyed by pointid with the value being a dict in the form 
        {node: distance to vertex, node: distance to vertex}
3. `npoints` point observations in set
4. `obs_to_arc` dict keyed by arc with the value being a dict in the form 
        {pointID:(x-coord, y-coord), pointID:(x-coord, y-coord), ... }
5. `obs_to_vertex` list of incident network vertices to snapped observation points
6. `points` geojson like representation of the point pattern.  Includes properties if read with attributes=True
7. `snapped_coordinates` dict keyed by pointid with the value being (x-coord, y-coord)



### Counts per link (arc or edge) are important, but should not be precomputed since we have different representations of the network (spatial and graph currently).  (Relatively) Uniform segmentation still needs to be done.



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
counts = ntw.count_per_link(ntw.pointpatterns['crimes'].obs_to_arc,
                            graph=False)

```
</div>

</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
sum(list(counts.values())) / float(len(counts.keys()))

```
</div>

</div>



### Network segmentation



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
n200 = ntw.split_arcs(200.0)

```
</div>

</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
counts = n200.count_per_link(n200.pointpatterns['crimes'].obs_to_arc,
                             graph=False)
sum(counts.values()) / float(len(counts.keys()))

```
</div>

</div>



### Create `geopandas.GeoDataFrame` objects of the vertices and arcs



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
# 'full' unsegmented network
vertices_df, arcs_df = spgh.element_as_gdf(ntw,
                                           vertices=ntw.vertex_coords,
                                           arcs=ntw.arcs)

# network segmented at 200-meter increments
vertices200_df, arcs200_df = spgh.element_as_gdf(n200,
                                                 vertices=n200.vertex_coords,
                                                 arcs=n200.arcs)

```
</div>

</div>



### Visualization of the shapefile derived, unsegmented network with vertices in a larger, blue, semi-opaque form and the distance segmented network with small, red, fully opaque vertices.



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
base = arcs_df.plot(color='k', alpha=.25, figsize=(12,12))
vertices_df.plot(ax=base, color='b', markersize=300, alpha=.25)
arcs200_df.plot(ax=base, color='k', alpha=.25)
vertices200_df.plot(ax=base, color='r', markersize=25, alpha=1.)

```
</div>

</div>



### Moran's I using the digitized network



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
# Binary Adjacency
w = ntw.contiguityweights(graph=False)

# Build the y vector
arcs = w.neighbors.keys()
y = np.zeros(len(arcs))

for i, a in enumerate(arcs):
    if a in counts.keys():
        y[i] = counts[a]

# Moran's I
res = esda.moran.Moran(y,
                       w,
                       permutations=99)
print(dir(res))

```
</div>

</div>



### Moran's I using the graph representation to generate the W

* Note that we have to regenerate the counts per arc, since the graph will have less edges.



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
counts = ntw.count_per_link(ntw.pointpatterns['crimes'].obs_to_arc,
                            graph=True)

# Binary Adjacency
w = ntw.contiguityweights(graph=True)

# Build the y vector
edges = w.neighbors.keys()
y = np.zeros(len(edges))

for i, e in enumerate(edges):
    if e in counts.keys():
        y[i] = counts[e]

# Moran's I
res = esda.moran.Moran(y,
                       w,
                       permutations=99)

print(dir(res))

```
</div>

</div>



### Moran's I using the segmented network and intensities instead of counts



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
# Binary Adjacency
w = n200.contiguityweights(graph=False)

# Compute the counts
counts = n200.count_per_link(n200.pointpatterns['crimes'].obs_to_arc,
                             graph=False)

# Build the y vector and convert from raw counts to intensities
arcs = w.neighbors.keys()
y = np.zeros(len(arcs))

for i, a in enumerate(edges):
    if a in counts.keys():
        length = n200.arc_lengths[a]
        y[i] = counts[a] / length

# Moran's I
res = esda.moran.Moran(y,
                       w,
                       permutations=99)

print(dir(res))

```
</div>

</div>



### Timings for distance based methods, e.g. G-function



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
t1 = time.time()
n0 = ntw.allneighbordistances(ntw.pointpatterns['crimes'])
print(time.time()-t1)

```
</div>

</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
t1 = time.time()
n1 = n200.allneighbordistances(n200.pointpatterns['crimes'])
print(time.time()-t1)

```
</div>

</div>



* Note that the first time these methods are called, the underlying vertex-to-vertex shortest path distance matrix has to be calculated. Subsequent calls will not require this, and will be much faster:



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
t1 = time.time()
n0 = ntw.allneighbordistances(ntw.pointpatterns['crimes'])
print(time.time()-t1)

```
</div>

</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
t1 = time.time()
n1 = n200.allneighbordistances(n200.pointpatterns['crimes'])
print(time.time()-t1)

```
</div>

</div>



### Simulate a point pattern on the network

* Need to supply a count of the number of points and a distirbution (default is uniform).  Generally, this will not be called by the user, since the simulation will be used for Monte Carlo permutation.



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
npts = ntw.pointpatterns['crimes'].npoints
sim = ntw.simulate_observations(npts)
sim

```
</div>

</div>



### F-function



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
fres = ntw.NetworkF(ntw.pointpatterns['crimes'],
                    permutations=99)

```
</div>

</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
plt.figure(figsize=(8,8))
plt.plot(fres.xaxis, fres.observed, 'b-', linewidth=1.5, label='Observed')
plt.plot(fres.xaxis, fres.upperenvelope, 'r--', label='Upper')
plt.plot(fres.xaxis, fres.lowerenvelope, 'k--', label='Lower')
plt.legend(loc='best', fontsize='x-large')
plt.title('Network F Function', fontsize='xx-large')
plt.show()

```
</div>

</div>



### Create a nearest neighbor matrix using the crimes point pattern

* [note from jlaura] Right now, both the G and K functions generate a full distance matrix.  This is because, I know that the full generation is correct and I believe that the truncated generated, e.g. nearest neighbor, has a bug.



### G-function



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
gres = ntw.NetworkG(ntw.pointpatterns['crimes'],
                    permutations=99)

```
</div>

</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
plt.figure(figsize=(8,8))
plt.plot(gres.xaxis, gres.observed, 'b-', linewidth=1.5, label='Observed')
plt.plot(gres.xaxis, gres.upperenvelope, 'r--', label='Upper')
plt.plot(gres.xaxis, gres.lowerenvelope, 'k--', label='Lower')
plt.legend(loc='best', fontsize='x-large')
plt.title('Network G Function', fontsize='xx-large')
plt.show()

```
</div>

</div>



### K-function



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
kres = ntw.NetworkK(ntw.pointpatterns['crimes'],
                    permutations=99)

```
</div>

</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
plt.figure(figsize=(8,8))
plt.plot(kres.xaxis, kres.observed, 'b-', linewidth=1.5, label='Observed')
plt.plot(kres.xaxis, kres.upperenvelope, 'r--', label='Upper')
plt.plot(kres.xaxis, kres.lowerenvelope, 'k--', label='Lower')
plt.legend(loc='best', fontsize='x-large')
plt.title('Network K Function', fontsize='xx-large')
plt.show()

```
</div>

</div>



-----------


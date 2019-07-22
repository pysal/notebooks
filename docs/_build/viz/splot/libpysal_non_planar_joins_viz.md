---
redirect_from:
  - "/viz/splot/libpysal-non-planar-joins-viz"
interact_link: content/viz/splot/libpysal_non_planar_joins_viz.ipynb
kernel_name: python3
has_widgets: false
title: 'libpysal_non_planar_joins_viz'
prev_page:
  url: /viz/splot/esda_moran_matrix_viz
  title: 'esda_moran_matrix_viz'
next_page:
  url: /viz/splot/esda_morans_viz
  title: 'esda_morans_viz'
comment: "***PROGRAMMATICALLY GENERATED, DO NOT EDIT. SEE ORIGINAL FILES IN /content***"
---


# splot.pysal.lib: assessing neigbors & spatial weights



In spatial analysis workflows it is often important and necessary to asses the relationships of neighbouring polygons. `pysal.lib` and `splot` can help you to inspect if two neighbouring polygons share an edge or not. 

**Content**:
* Imports
* Data Preparation
* Plotting



## Imports



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
from pysal.lib.weights.contiguity import Queen
import pysal.lib
from pysal.lib import examples
import matplotlib.pyplot as plt
import geopandas as gpd
%matplotlib inline

```
</div>

</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
from pysal.viz.splot.pysal.lib import plot_spatial_weights

```
</div>

</div>



## Data Preparation



Let's first have a look at the dataset with `pysal.lib.examples.explain`



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
examples.explain('rio_grande_do_sul')

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
{'name': 'Rio_Grande_do_Sul',
 'description': 'Cities of the Brazilian State of Rio Grande do Sul',
 'explanation': ['* 43MUE250GC_SIR.dbf: attribute data (k=2)',
  '* 43MUE250GC_SIR.shp: Polygon shapefile (n=499)',
  '* 43MUE250GC_SIR.shx: spatial index',
  '* 43MUE250GC_SIR.cpg: encoding file ',
  '* 43MUE250GC_SIR.prj: projection information ',
  '* map_RS_BR.dbf: attribute data (k=3)',
  '* map_RS_BR.shp: Polygon shapefile (no lakes) (n=497)',
  '* map_RS_BR.prj: projection information',
  '* map_RS_BR.shx: spatial index',
  'Source: Renan Xavier Cortes <renanxcortes@gmail.com>',
  'Reference: https://github.com/pysal/pysal/issues/889#issuecomment-396693495']}
```


</div>
</div>
</div>



Load data into a `geopandas` geodataframe



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
gdf = gpd.read_file(examples.get_path('map_RS_BR.shp'))
gdf.head()

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
      <th>NM_MUNICIP</th>
      <th>CD_GEOCMU</th>
      <th>geometry</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>ACEGUÁ</td>
      <td>4300034</td>
      <td>POLYGON ((-54.10940375660775 -31.4331615329298...</td>
    </tr>
    <tr>
      <th>1</th>
      <td>ÁGUA SANTA</td>
      <td>4300059</td>
      <td>POLYGON ((-51.98932089399999 -28.1294290447850...</td>
    </tr>
    <tr>
      <th>2</th>
      <td>AGUDO</td>
      <td>4300109</td>
      <td>POLYGON ((-53.13695617099998 -29.4948277498090...</td>
    </tr>
    <tr>
      <th>3</th>
      <td>AJURICABA</td>
      <td>4300208</td>
      <td>POLYGON ((-53.61993058200001 -28.1456914857853...</td>
    </tr>
    <tr>
      <th>4</th>
      <td>ALECRIM</td>
      <td>4300307</td>
      <td>POLYGON ((-54.77812739300882 -27.5837166490823...</td>
    </tr>
  </tbody>
</table>
</div>
</div>


</div>
</div>
</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
weights = Queen.from_dataframe(gdf)

```
</div>

</div>



This warning tells us that our dataset contains islands. Islands are polygons that do not share edges and nodes with adjacent polygones. This can for example be the case if polygones are truly not neighbouring, eg. when two land parcels are seperated by a river. However, these islands often stems from human error when digitizing features into polygons. 

This unwanted error can be assessed using `splot.pysal.lib` `plot_spatial_weights` functionality:



### Plotting



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
plot_spatial_weights(weights, gdf)
plt.show()

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">

{:.output_png}
![png](../../images/viz/splot/libpysal_non_planar_joins_viz_13_0.png)

</div>
</div>
</div>



This visualisation depicts the spatial weights network, a network of connections of the centroid of each polygon to the centroid of its neighbour. As we can see, there are many polygons in the south and west of this map, that are not connected to it's neighbors. This stems from digitization errors and needs to be corrected before we can start our statistical analysis. 

`pysal.lib` offers a tool to correct this error by 'snapping' incorrectly separated neighbours back together:



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
wnp = pysal.lib.weights.util.nonplanar_neighbors(weights, gdf)

```
</div>

</div>



We can now visualise if the `nonplanar_neighbors` tool adjusted all errors correctly:



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
plot_spatial_weights(wnp, gdf)
plt.show()

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">

{:.output_png}
![png](../../images/viz/splot/libpysal_non_planar_joins_viz_17_0.png)

</div>
</div>
</div>



The visualization shows that all erroneous islands are now stored as neighbors in our new weights object, depicted by the new joins displayed in orange.

We can now adapt our visualization to show all joins in the same color, by using the `nonplanar_edge_kws` argument in `plot_spatial_weights`:



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
plot_spatial_weights(wnp, gdf, nonplanar_edge_kws=dict(color='#4393c3'))
plt.show()

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">

{:.output_png}
![png](../../images/viz/splot/libpysal_non_planar_joins_viz_19_0.png)

</div>
</div>
</div>


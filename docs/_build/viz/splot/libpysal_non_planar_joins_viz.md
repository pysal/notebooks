---
redirect_from:
  - "/viz/splot/libpysal-non-planar-joins-viz"
interact_link: content/viz/splot/libpysal_non_planar_joins_viz.ipynb
title: 'libpysal_non_planar_joins_viz'
prev_page:
  url: /viz/splot/giddy_space_time
  title: 'giddy_space_time'
next_page:
  url: /viz/splot/mapping_vba
  title: 'mapping_vba'
comment: "***PROGRAMMATICALLY GENERATED, DO NOT EDIT. SEE ORIGINAL FILES IN /content***"
---

# splot.libpysal: assessing neigbors & spatial weights

### Imports



{:.input_area}
```python
from libpysal.weights.contiguity import Queen
import libpysal
from libpysal import examples
import matplotlib.pyplot as plt
import geopandas as gpd
%matplotlib inline
```




{:.input_area}
```python
from splot.libpysal import plot_spatial_weights
```


## Data Preparation



{:.input_area}
```python
examples.explain('rio_grande_do_sul')
```





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



Load data into a `geopandas` geodataframe



{:.input_area}
```python
gdf = gpd.read_file(examples.get_path('map_RS_BR.shp'))
gdf.head()
```





<div markdown="0">
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





{:.input_area}
```python
weights = Queen.from_dataframe(gdf)
```


This warning tells us that our dataset contains islands. Islands are polygons that do not share edges and nodes with adjacent polygones. This can for example be the case if polygones are truly not neighbouring, eg. when two land parcels are seperated by a river. However, these islands often stems from human error when digitizing features into polygons. 

This unwanted error can be assessed using `splot.libpysal` `plot_spatial_weights` functionality:

### Plotting



{:.input_area}
```python
plot_spatial_weights(weights, gdf)
plt.show()
```



![png](../../images/viz/splot/libpysal_non_planar_joins_viz_11_0.png)


This visualisation depicts the spatial weights network, a network of connections of the centroid of each polygon to the centroid of its neighbour. As we can see, there are many polygons in the south and west of this map, that are not connected to it's neighbors. This stems from digitization errors and needs to be corrected before we can start our statistical analysis. 

`libpysal` offers a tool to correct this error by 'snapping' incorrectly separated neighbours back together:



{:.input_area}
```python
wnp = libpysal.weights.util.nonplanar_neighbors(weights, gdf)
```


We can now visualise if the `nonplanar_neighbors` tool adjusted all errors correctly:



{:.input_area}
```python
plot_spatial_weights(wnp, gdf)
plt.show()
```



![png](../../images/viz/splot/libpysal_non_planar_joins_viz_15_0.png)


The visualization shows that all erroneous islands are now stored as neighbors in our new weights object, depicted by the new joins displayed in orange.

We can now adapt our visualization to show all joins in the same color, by using the `nonplanar_edge_kws` argument in `plot_spatial_weights`:



{:.input_area}
```python
plot_spatial_weights(wnp, gdf, nonplanar_edge_kws=dict(color='#4393c3'))
plt.show()
```



![png](../../images/viz/splot/libpysal_non_planar_joins_viz_17_0.png)


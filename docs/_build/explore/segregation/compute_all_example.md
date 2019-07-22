---
redirect_from:
  - "/explore/segregation/compute-all-example"
interact_link: content/explore/segregation/compute_all_example.ipynb
kernel_name: python3
has_widgets: false
title: 'compute_all_example'
prev_page:
  url: /explore/segregation/multigroup_aspatial_examples
  title: 'multigroup_aspatial_examples'
next_page:
  url: /explore/segregation/network_measures
  title: 'network_measures'
comment: "***PROGRAMMATICALLY GENERATED, DO NOT EDIT. SEE ORIGINAL FILES IN /content***"
---


# Example of use of computing several measures of the PySAL *segregation* module: using `ComputeAll` classes



The Compute_All classes comprises simple and quick functions to assess multiple segregation measures at once in a dataset. It uses all the default parameters and returns an object that has an attribute (.computed) of a dictionary with summary of all values fitted.

The wrappers have currently three classes: ComputeAllAspatialSegregation, ComputeAllSpatialSegregation and ComputeAllSegregation which comprises all the measures available.

Firstly, we need to import the libraries and functions to be used.



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
%matplotlib inline

import geopandas as gpd
from pysal.explore import segregation
import pysal.lib
from pysal.explore.segregation.compute_all import ComputeAllAspatialSegregation, ComputeAllSpatialSegregation, ComputeAllSegregation

```
</div>

</div>



Then it's time to load some data to estimate segregation. We use the data of 2000 Census Tract Data for the metropolitan area of Sacramento, CA, USA. 

We use a geopandas dataframe available in PySAL examples repository.

For more information about the data: https://github.com/pysal/pysal.lib/tree/master/pysal.lib/examples/sacramento2



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
s_map = gpd.read_file(pysal.lib.examples.get_path("sacramentot2.shp"))
s_map.columns

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
Index(['FIPS', 'MSA', 'TOT_POP', 'POP_16', 'POP_65', 'WHITE_', 'BLACK_',
       'ASIAN_', 'HISP_', 'MULTI_RA', 'MALES', 'FEMALES', 'MALE1664',
       'FEM1664', 'EMPL16', 'EMP_AWAY', 'EMP_HOME', 'EMP_29', 'EMP_30',
       'EMP16_2', 'EMP_MALE', 'EMP_FEM', 'OCC_MAN', 'OCC_OFF1', 'OCC_INFO',
       'HH_INC', 'POV_POP', 'POV_TOT', 'HSG_VAL', 'FIPSNO', 'POLYID',
       'geometry'],
      dtype='object')
```


</div>
</div>
</div>



The data have several demographic variables. We are going to assess the segregation of the Hispanic Population (variable 'HISP_'). For this, we only extract some columns of the geopandas dataframe.



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
gdf = s_map[['geometry', 'HISP_', 'TOT_POP']]

```
</div>

</div>



### Compute All Aspatial Measures



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
aspatial_fit = ComputeAllAspatialSegregation(gdf, 'HISP_', 'TOT_POP')
aspatial_fit.computed

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
      <th>Measure</th>
      <th>Value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Dissimilarity</td>
      <td>0.321847</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Gini</td>
      <td>0.435065</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Entropy</td>
      <td>0.094598</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Atkinson</td>
      <td>0.150793</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Exposure</td>
      <td>0.768038</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Isolation</td>
      <td>0.231962</td>
    </tr>
    <tr>
      <th>6</th>
      <td>Concentration Profile</td>
      <td>0.137687</td>
    </tr>
    <tr>
      <th>7</th>
      <td>Bias Corrected Dissimilarity</td>
      <td>0.321431</td>
    </tr>
    <tr>
      <th>8</th>
      <td>Density Corrected Dissimilarity</td>
      <td>0.295205</td>
    </tr>
    <tr>
      <th>9</th>
      <td>Correlation Ratio</td>
      <td>0.091640</td>
    </tr>
    <tr>
      <th>10</th>
      <td>Modified Dissimilarity</td>
      <td>0.310733</td>
    </tr>
    <tr>
      <th>11</th>
      <td>Modified Gini</td>
      <td>0.421795</td>
    </tr>
  </tbody>
</table>
</div>
</div>


</div>
</div>
</div>



### Compute All Spatial Measures



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
spatial_fit = ComputeAllSpatialSegregation(gdf, 'HISP_', 'TOT_POP')
spatial_fit.computed

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
      <th>Measure</th>
      <th>Value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Spatial Dissimilarity</td>
      <td>0.261197</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Absolute Centralization</td>
      <td>0.689142</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Absolute Clustering</td>
      <td>0.005189</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Absolute Concentration</td>
      <td>0.851282</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Delta</td>
      <td>0.804497</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Relative Centralization</td>
      <td>-0.111942</td>
    </tr>
    <tr>
      <th>6</th>
      <td>Relative Clustering</td>
      <td>0.009096</td>
    </tr>
    <tr>
      <th>7</th>
      <td>Relative Concentration</td>
      <td>0.127338</td>
    </tr>
    <tr>
      <th>8</th>
      <td>Distance Decay Exposure</td>
      <td>0.839658</td>
    </tr>
    <tr>
      <th>9</th>
      <td>Distance Decay Isolation</td>
      <td>0.156216</td>
    </tr>
    <tr>
      <th>10</th>
      <td>Spatial Proximity Profile</td>
      <td>0.228473</td>
    </tr>
    <tr>
      <th>11</th>
      <td>Spatial Proximity</td>
      <td>1.002662</td>
    </tr>
    <tr>
      <th>12</th>
      <td>Boundary Spatial Dissimilarity</td>
      <td>0.266763</td>
    </tr>
    <tr>
      <th>13</th>
      <td>Perimeter Area Ratio Spatial Dissimilarity</td>
      <td>0.311172</td>
    </tr>
  </tbody>
</table>
</div>
</div>


</div>
</div>
</div>



### Compute All Segregation Measures



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
segregation_fit = ComputeAllSegregation(gdf, 'HISP_', 'TOT_POP')
segregation_fit.computed

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
      <th>Measure</th>
      <th>Value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Dissimilarity</td>
      <td>0.321847</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Gini</td>
      <td>0.435065</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Entropy</td>
      <td>0.094598</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Atkinson</td>
      <td>0.150793</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Exposure</td>
      <td>0.768038</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Isolation</td>
      <td>0.231962</td>
    </tr>
    <tr>
      <th>6</th>
      <td>Concentration Profile</td>
      <td>0.137687</td>
    </tr>
    <tr>
      <th>7</th>
      <td>Bias Corrected Dissimilarity</td>
      <td>0.321369</td>
    </tr>
    <tr>
      <th>8</th>
      <td>Density Corrected Dissimilarity</td>
      <td>0.295205</td>
    </tr>
    <tr>
      <th>9</th>
      <td>Correlation Ratio</td>
      <td>0.091640</td>
    </tr>
    <tr>
      <th>10</th>
      <td>Modified Dissimilarity</td>
      <td>0.310738</td>
    </tr>
    <tr>
      <th>11</th>
      <td>Modified Gini</td>
      <td>0.421745</td>
    </tr>
    <tr>
      <th>12</th>
      <td>Spatial Dissimilarity</td>
      <td>0.261197</td>
    </tr>
    <tr>
      <th>13</th>
      <td>Absolute Centralization</td>
      <td>0.689142</td>
    </tr>
    <tr>
      <th>14</th>
      <td>Absolute Clustering</td>
      <td>0.005189</td>
    </tr>
    <tr>
      <th>15</th>
      <td>Absolute Concentration</td>
      <td>0.851282</td>
    </tr>
    <tr>
      <th>16</th>
      <td>Delta</td>
      <td>0.804497</td>
    </tr>
    <tr>
      <th>17</th>
      <td>Relative Centralization</td>
      <td>-0.111942</td>
    </tr>
    <tr>
      <th>18</th>
      <td>Relative Clustering</td>
      <td>0.009096</td>
    </tr>
    <tr>
      <th>19</th>
      <td>Relative Concentration</td>
      <td>0.127338</td>
    </tr>
    <tr>
      <th>20</th>
      <td>Distance Decay Exposure</td>
      <td>0.839658</td>
    </tr>
    <tr>
      <th>21</th>
      <td>Distance Decay Isolation</td>
      <td>0.156216</td>
    </tr>
    <tr>
      <th>22</th>
      <td>Spatial Proximity Profile</td>
      <td>0.228473</td>
    </tr>
    <tr>
      <th>23</th>
      <td>Spatial Proximity</td>
      <td>1.002662</td>
    </tr>
    <tr>
      <th>24</th>
      <td>Boundary Spatial Dissimilarity</td>
      <td>0.266763</td>
    </tr>
    <tr>
      <th>25</th>
      <td>Perimeter Area Ratio Spatial Dissimilarity</td>
      <td>0.311172</td>
    </tr>
  </tbody>
</table>
</div>
</div>


</div>
</div>
</div>


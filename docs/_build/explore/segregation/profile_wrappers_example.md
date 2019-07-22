---
redirect_from:
  - "/explore/segregation/profile-wrappers-example"
interact_link: content/explore/segregation/profile_wrappers_example.ipynb
kernel_name: python3
has_widgets: false
title: 'profile_wrappers_example'
prev_page:
  url: /explore/segregation/intro
  title: 'segregation'
next_page:
  url: /explore/segregation/decomposition_wrapper_example
  title: 'decomposition_wrapper_example'
comment: "***PROGRAMMATICALLY GENERATED, DO NOT EDIT. SEE ORIGINAL FILES IN /content***"
---


# Example of use of the Profile Wrappers of the PySAL *segregation* module



The Profile Wrappers comprises simple and quick functions to assess multiple segregation measures at once in a dataset. It uses all the default parameters and returns an object that has an attribute (.profile) of a dictionary with summary of all values fitted.

The wrappers have currently three classes: nonspatial profiles, spatial profiles and the overall profile which comprises all the measures available.

Firstly, we need to import the libraries and functions to be used.



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
%matplotlib inline

import geopandas as gpd
from pysal.explore import segregation
import pysal.lib
from pysal.explore.segregation.profile_wrappers import Profile_Non_Spatial_Segregation, Profile_Spatial_Segregation, Profile_Segregation

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



### Non-Spatial Profile



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
non_spatial_fit = Profile_Non_Spatial_Segregation(gdf, 'HISP_', 'TOT_POP')
non_spatial_fit.profile

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
{'Dissimilarity': 0.32184656076566864,
 'Gini': 0.43506510676886234,
 'Entropy': 0.09459760633014454,
 'Atkinson': 0.15079259382667654,
 'Exposure': 0.7680384513540848,
 'Isolation': 0.2319615486459151,
 'Concentration Profile': 0.1376874794741899,
 'Bias Corrected Dissimilarity': 0.321368377703044,
 'Density Corrected Dissimilarity': 0.295205155464069,
 'Correlation Ratio': 0.09164042012926693,
 'Modified Dissimilarity': 0.3107369316658255,
 'Modified Gini': 0.42176600428897665}
```


</div>
</div>
</div>



### Spatial Profile



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
spatial_fit = Profile_Spatial_Segregation(gdf, 'HISP_', 'TOT_POP')
spatial_fit.profile

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
{'Spatial Dissimilarity': 0.2611974332919437,
 'Absolute Centralization': 0.6891422368736286,
 'Absolute Concentration': 0.21496583971774408,
 'Delta': 0.8044969214141899,
 'Relative Centralization': -0.11194177550430595,
 'Relative Clustering': 0.009095632468738568,
 'Relative Concentration': 0.13102848628073688,
 'Spatial Exposure': 0.8396583368412371,
 'Spatial Isolation': 0.1562162475606278,
 'Spatial Proximity Profile': 0.22847334404621394,
 'Spatial Proximity': 1.0026623464135092,
 'Boundary Spatial Dissimilarity': 0.2667626367289605,
 'Perimeter Area Ratio Spatial Dissimilarity': 0.3165091834802075,
 'Spatial Information Theory': 0.778177518074913}
```


</div>
</div>
</div>



### Overall Segregation Profile



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
segregation_fit = Profile_Segregation(gdf, 'HISP_', 'TOT_POP')
segregation_fit.profile

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
{'Dissimilarity': 0.32184656076566864,
 'Gini': 0.43506510676886234,
 'Entropy': 0.09459760633014454,
 'Atkinson': 0.15079259382667654,
 'Exposure': 0.7680384513540848,
 'Isolation': 0.2319615486459151,
 'Concentration Profile': 0.1376874794741899,
 'Bias Corrected Dissimilarity': 0.3214362960831827,
 'Density Corrected Dissimilarity': 0.295205155464069,
 'Correlation Ratio': 0.09164042012926693,
 'Modified Dissimilarity': 0.31075359653655094,
 'Modified Gini': 0.4217841271855144,
 'Spatial Dissimilarity': 0.2611974332919437,
 'Absolute Centralization': 0.6891422368736286,
 'Absolute Concentration': 0.21496583971774408,
 'Delta': 0.8044969214141899,
 'Relative Centralization': -0.11194177550430595,
 'Relative Clustering': 0.009095632468738568,
 'Relative Concentration': 0.13102848628073688,
 'Spatial Exposure': 0.8396583368412371,
 'Spatial Isolation': 0.1562162475606278,
 'Spatial Proximity Profile': 0.22847334404621394,
 'Spatial Proximity': 1.0026623464135092,
 'Boundary Spatial Dissimilarity': 0.2667626367289605,
 'Perimeter Area Ratio Spatial Dissimilarity': 0.3165091834802075,
 'Spatial Information Theory': 0.778177518074913}
```


</div>
</div>
</div>


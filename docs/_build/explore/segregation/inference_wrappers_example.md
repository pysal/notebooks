---
redirect_from:
  - "/explore/segregation/inference-wrappers-example"
interact_link: content/explore/segregation/inference_wrappers_example.ipynb
kernel_name: python3
has_widgets: false
title: 'inference_wrappers_example'
prev_page:
  url: /explore/segregation/decomposition_wrapper_example
  title: 'decomposition_wrapper_example'
next_page:
  url: /explore/segregation/nonspatial_examples
  title: 'nonspatial_examples'
comment: "***PROGRAMMATICALLY GENERATED, DO NOT EDIT. SEE ORIGINAL FILES IN /content***"
---


# Inference Wrappers use cases



This is an example of the PySAL *segregation* framework to perform inference on a single value and comparative inference using simulations under the null hypothesis. Once the segregation classes are fitted, the user can perform inference to shed light for statistical significance in regional analysis. Currently, it is possible to make inference for a single measure or for two values of the same measure.

The summary of the inference wrappers is presented in the following Table:

| **Inference Type** | **Class/Function**   |                 **Function main Inputs**                 |         **Function Outputs**         |
| :----------------- | :------------------- | :------------------------------------------------------: | :----------------------------------: |
| Single Value       | Infer\_Segregation   |   seg\_class, iterations\_under\_null, null\_approach, two\_tailed    |    p\_value, est\_sim, statistic     |
| Two Value          | Compare\_Segregation | seg\_class\_1, seg\_class\_2, iterations\_under\_null, null\_approach | p\_value, est\_sim, est\_point\_diff |



Firstly let's import the module/functions for the use case:



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
%matplotlib inline

import geopandas as gpd
from pysal.explore import segregation
import pysal.lib
import pandas as pd
import numpy as np

from pysal.explore.segregation.inference_wrappers import Infer_Segregation, Compare_Segregation

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



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
gdf = s_map[['geometry', 'HISP_', 'TOT_POP']]

```
</div>

</div>



We also can plot the spatial distribution of the composition of the Hispanic population over the tracts of Sacramento:



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
gdf['composition'] = gdf['HISP_'] / gdf['TOT_POP']

gdf.plot(column = 'composition',
         cmap = 'OrRd', 
         figsize=(20,10),
         legend = True)

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
<matplotlib.axes._subplots.AxesSubplot at 0x2151c13b550>
```


</div>
</div>
<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">

{:.output_png}
![png](../../images/explore/segregation/inference_wrappers_example_8_1.png)

</div>
</div>
</div>



## Single Value

### Dissimilarity

The **Infer\_Segregation** function expect to receive a pre-fitted segregation class and then it uses the underlying data to iterate over the null hypothesis and comparing the results with point estimation of the index. Thus, we need to firstly estimate some measure. We can fit the classic Dissimilarity index:



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
from pysal.explore.segregation.non_spatial_indexes import Dissim
D = Dissim(gdf, 'HISP_', 'TOT_POP')
D.statistic

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
0.32184656076566864
```


</div>
</div>
</div>



The question that may rise is "Is this value of 0.32 statistically significant under some pre-specified circumstance?". To answer this, it is possible to rely on the **Infer_Segregation** function to generate several values of the same index (in this case the Dissimilarity Index) under the hypothesis and compare them with the one estimated by the dataset of Sacramento. To generate 1000 values assuming *evenness*, you can run:



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
infer_D_eve = Infer_Segregation(D, iterations_under_null = 1000, null_approach = "evenness", two_tailed = True)

```
</div>

</div>



This class has a quick plotting method to inspect the generated distribution with the estimated value from the sample (vertical red line):



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
infer_D_eve.plot()

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">

{:.output_png}
![png](../../images/explore/segregation/inference_wrappers_example_14_0.png)

</div>
</div>
</div>



It is possible to see that clearly the value of 0.3218 is far-right in the distribution indicating that the hispanic group is, indeed, significantly segregated in terms of the Dissimilarity index under evenness. You can also check the mean value of the distribution using the **est_sim** attribute which represents all the D draw from the simulations:



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
infer_D_eve.est_sim.mean()

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
0.016081626483495783
```


</div>
</div>
</div>



The two-tailed p-value of the following hypothesis test:

$$H_0: under \ evenness, \ Sacramento \ IS \ NOT \ segregated \ in \ terms \ of \ the \ Dissimilarity \ index \ (D)$$
$$H_1: under \ evenness, \ Sacramento \ IS \ segregated \ in \ terms \ of \ the \ Dissimilarity \ index \ (D)$$

can be accessed with the **p_value** attribute:



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
infer_D_eve.p_value

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
0.0
```


</div>
</div>
</div>



Therefore, we can conclude that Sacramento is statistically segregated at 5% of significance level (p.value < 5%) in terms of D.

You can also test under different approaches for the null hypothesis:



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
infer_D_sys = Infer_Segregation(D, iterations_under_null = 10000, null_approach = "systematic", two_tailed = True)

```
</div>

</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
infer_D_sys.plot()

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">

{:.output_png}
![png](../../images/explore/segregation/inference_wrappers_example_21_0.png)

</div>
</div>
</div>



The conclusions are analogous as the *evenness* approach.



### Relative Concentration



The **Infer_Segregation** wrapper can handle any class of the PySAL segregation module. It is possible to use it in the Relative Concentration (RCO) segregation index:



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
from pysal.explore.segregation.spatial_indexes import Relative_Concentration
RCO = Relative_Concentration(gdf, 'HISP_', 'TOT_POP')

```
</div>

</div>



Since RCO is an spatial index (i.e. depends on the spatial context), it makes sense to use the *permutation* null approach. This approach relies on randomly allocating the sample values over the spatial units and recalculating the chosen index to all iterations.



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
infer_RCO_per = Infer_Segregation(RCO, iterations_under_null = 1000, null_approach = "permutation", two_tailed = True)

```
</div>

</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
infer_RCO_per.plot()

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">

{:.output_png}
![png](../../images/explore/segregation/inference_wrappers_example_28_0.png)

</div>
</div>
</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
infer_RCO_per.p_value

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
0.446
```


</div>
</div>
</div>



Analogously, the conclusion for the Relative Concentration index is that Sacramento is not significantly (under 5% of significance, because p-value > 5%) concentrated for the hispanic people.



Additionaly, it is possible to combine the null approaches establishing, for example, a permutation along with evenness of the frequency of the Sacramento hispanic group. With this, the conclusion of the Relative Concentration changes.



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
infer_RCO_eve_per = Infer_Segregation(RCO, iterations_under_null = 1000, null_approach = "even_permutation", two_tailed = True)
infer_RCO_eve_per.plot()

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">

{:.output_png}
![png](../../images/explore/segregation/inference_wrappers_example_32_0.png)

</div>
</div>
</div>



### Relative Centralization



Using the same *permutation* approach for the Relative Centralization (RCE) segregation index:



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
from pysal.explore.segregation.spatial_indexes import Relative_Centralization
RCE = Relative_Centralization(gdf, 'HISP_', 'TOT_POP')
infer_RCE_per = Infer_Segregation(RCE, iterations_under_null = 1000, null_approach = "permutation", two_tailed = True)

```
</div>

</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
infer_RCE_per.plot()

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">

{:.output_png}
![png](../../images/explore/segregation/inference_wrappers_example_36_0.png)

</div>
</div>
</div>



The conclusion is that the hispanic group is negatively significantly (as the point estimation is in the left side of the distribution) in terms of centralization. This behavior can be, somehow, inspected in the map as the composition tends to be more concentraded outside of the center of the overall region.

---



## Comparative Inference



To compare two different values, the user can rely on the **Compare\_Segregation** function. Similar to the previous function, the user needs to pass two segregation SM classes to be compared, establish the number of iterations under null hypothesis with *iterations_under_null*, specify which type of null hypothesis the inference will iterate with *null_approach* argument and, also, can pass additional parameters for each segregation estimation.

Obs.: in this case, each measure has to be the same class as it would not make much sense to compare, for example, a Gini index with a Delta index



This example uses all census data that the user must provide your own copy of the external database.
A step-by-step procedure for downloading the data can be found here: https://github.com/spatialucr/geosnap/tree/master/geosnap/data.
After the user download the zip files, you must provide the path to these files.



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
import os
#os.chdir('path_to_zipfiles')

```
</div>

</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
from geosnap.data import read_ltdb

sample = "LTDB_Std_All_Sample.zip"
full = "LTDB_Std_All_fullcount.zip"

df_pre = read_ltdb(sample = sample, fullcount = full)

```
</div>

</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
df_pre.head()

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
      <th>n_asian_under_15</th>
      <th>n_black_under_15</th>
      <th>n_hispanic_under_15</th>
      <th>n_native_under_15</th>
      <th>n_white_under_15</th>
      <th>n_persons_under_18</th>
      <th>n_asian_over_60</th>
      <th>n_black_over_60</th>
      <th>n_hispanic_over_60</th>
      <th>n_native_over_60</th>
      <th>...</th>
      <th>n_widowed_divorced</th>
      <th>n_white_persons</th>
      <th>year</th>
      <th>p_nonhisp_white_persons</th>
      <th>p_white_over_60</th>
      <th>p_black_over_60</th>
      <th>p_hispanic_over_60</th>
      <th>p_native_over_60</th>
      <th>p_asian_over_60</th>
      <th>p_disabled</th>
    </tr>
    <tr>
      <th>geoid</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>01001020500</th>
      <td>NaN</td>
      <td>1.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>2.0</td>
      <td>3.0</td>
      <td>NaN</td>
      <td>0.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>...</td>
      <td>1.0</td>
      <td>6.0</td>
      <td>1970</td>
      <td>NaN</td>
      <td>6.0</td>
      <td>4.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>5.0</td>
    </tr>
    <tr>
      <th>01003010100</th>
      <td>NaN</td>
      <td>609.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>639.0</td>
      <td>1407.0</td>
      <td>NaN</td>
      <td>221.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>...</td>
      <td>324.0</td>
      <td>2004.0</td>
      <td>1970</td>
      <td>NaN</td>
      <td>8.0</td>
      <td>6.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>6.0</td>
    </tr>
    <tr>
      <th>01003010200</th>
      <td>NaN</td>
      <td>38.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>564.0</td>
      <td>687.0</td>
      <td>NaN</td>
      <td>28.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>...</td>
      <td>175.0</td>
      <td>1758.0</td>
      <td>1970</td>
      <td>NaN</td>
      <td>13.0</td>
      <td>1.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>6.0</td>
    </tr>
    <tr>
      <th>01003010300</th>
      <td>NaN</td>
      <td>375.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>982.0</td>
      <td>1524.0</td>
      <td>NaN</td>
      <td>104.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>...</td>
      <td>292.0</td>
      <td>2835.0</td>
      <td>1970</td>
      <td>NaN</td>
      <td>8.0</td>
      <td>3.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>7.0</td>
    </tr>
    <tr>
      <th>01003010400</th>
      <td>NaN</td>
      <td>113.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>797.0</td>
      <td>1030.0</td>
      <td>NaN</td>
      <td>37.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>...</td>
      <td>183.0</td>
      <td>2323.0</td>
      <td>1970</td>
      <td>NaN</td>
      <td>11.0</td>
      <td>1.0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>11.0</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 191 columns</p>
</div>
</div>


</div>
</div>
</div>



In this example, we are interested to assess the comparative segregation of the non-hispanic black people in the census tracts of the Riverside, CA, county between 2000 and 2010. Therefore, we extract the desired columns and add some auxiliary variables:



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
df = df_pre[['n_nonhisp_black_persons', 'n_total_pop', 'year']]

df['geoid'] = df.index
df['state'] = df['geoid'].str[0:2]
df['county'] = df['geoid'].str[2:5]
df.head()

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
      <th>n_nonhisp_black_persons</th>
      <th>n_total_pop</th>
      <th>year</th>
      <th>geoid</th>
      <th>state</th>
      <th>county</th>
    </tr>
    <tr>
      <th>geoid</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>01001020500</th>
      <td>NaN</td>
      <td>9.0</td>
      <td>1970</td>
      <td>01001020500</td>
      <td>01</td>
      <td>001</td>
    </tr>
    <tr>
      <th>01003010100</th>
      <td>NaN</td>
      <td>3470.0</td>
      <td>1970</td>
      <td>01003010100</td>
      <td>01</td>
      <td>003</td>
    </tr>
    <tr>
      <th>01003010200</th>
      <td>NaN</td>
      <td>1881.0</td>
      <td>1970</td>
      <td>01003010200</td>
      <td>01</td>
      <td>003</td>
    </tr>
    <tr>
      <th>01003010300</th>
      <td>NaN</td>
      <td>3724.0</td>
      <td>1970</td>
      <td>01003010300</td>
      <td>01</td>
      <td>003</td>
    </tr>
    <tr>
      <th>01003010400</th>
      <td>NaN</td>
      <td>2600.0</td>
      <td>1970</td>
      <td>01003010400</td>
      <td>01</td>
      <td>003</td>
    </tr>
  </tbody>
</table>
</div>
</div>


</div>
</div>
</div>



Filtering Riverside County and desired years of the analysis:



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
df_riv = df[(df['state'] == '06') & (df['county'] == '065') & (df['year'].isin(['2000', '2010']))]
df_riv.head()

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
      <th>n_nonhisp_black_persons</th>
      <th>n_total_pop</th>
      <th>year</th>
      <th>geoid</th>
      <th>state</th>
      <th>county</th>
    </tr>
    <tr>
      <th>geoid</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>06065030101</th>
      <td>59.0</td>
      <td>852.0</td>
      <td>2000</td>
      <td>06065030101</td>
      <td>06</td>
      <td>065</td>
    </tr>
    <tr>
      <th>06065030103</th>
      <td>120.0</td>
      <td>1740.0</td>
      <td>2000</td>
      <td>06065030103</td>
      <td>06</td>
      <td>065</td>
    </tr>
    <tr>
      <th>06065030104</th>
      <td>367.0</td>
      <td>5315.0</td>
      <td>2000</td>
      <td>06065030104</td>
      <td>06</td>
      <td>065</td>
    </tr>
    <tr>
      <th>06065030200</th>
      <td>348.0</td>
      <td>4682.0</td>
      <td>2000</td>
      <td>06065030200</td>
      <td>06</td>
      <td>065</td>
    </tr>
    <tr>
      <th>06065030300</th>
      <td>678.0</td>
      <td>4845.0</td>
      <td>2000</td>
      <td>06065030300</td>
      <td>06</td>
      <td>065</td>
    </tr>
  </tbody>
</table>
</div>
</div>


</div>
</div>
</div>



Merging it with desired map.



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
map_url = 'https://raw.githubusercontent.com/renanxcortes/inequality-segregation-supplementary-files/master/Tracts_grouped_by_County/06065.json'
map_gpd = gpd.read_file(map_url)
gdf = map_gpd.merge(df_riv, 
                    left_on = 'GEOID10', 
                    right_on = 'geoid')[['geometry', 'n_nonhisp_black_persons', 'n_total_pop', 'year']]

gdf['composition'] = np.where(gdf['n_total_pop'] == 0, 0, gdf['n_nonhisp_black_persons'] / gdf['n_total_pop'])

```
</div>

</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
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
      <th>geometry</th>
      <th>n_nonhisp_black_persons</th>
      <th>n_total_pop</th>
      <th>year</th>
      <th>composition</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>POLYGON ((-117.319414 33.902109, -117.322528 3...</td>
      <td>234.0</td>
      <td>2537.0</td>
      <td>2000</td>
      <td>0.092235</td>
    </tr>
    <tr>
      <th>1</th>
      <td>POLYGON ((-117.319414 33.902109, -117.322528 3...</td>
      <td>568.0</td>
      <td>6556.0</td>
      <td>2010</td>
      <td>0.086638</td>
    </tr>
    <tr>
      <th>2</th>
      <td>POLYGON ((-117.504056 33.800257, -117.502758 3...</td>
      <td>283.0</td>
      <td>3511.0</td>
      <td>2000</td>
      <td>0.080604</td>
    </tr>
    <tr>
      <th>3</th>
      <td>POLYGON ((-117.504056 33.800257, -117.502758 3...</td>
      <td>754.0</td>
      <td>10921.0</td>
      <td>2010</td>
      <td>0.069041</td>
    </tr>
    <tr>
      <th>4</th>
      <td>POLYGON ((-117.472451 33.762031, -117.475661 3...</td>
      <td>274.0</td>
      <td>3388.0</td>
      <td>2000</td>
      <td>0.080874</td>
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
gdf_2000 = gdf[gdf.year == 2000]
gdf_2010 = gdf[gdf.year == 2010]

```
</div>

</div>



Map of 2000:



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
gdf_2000.plot(column = 'composition',
              cmap = 'OrRd',
              figsize = (30,5),
              legend = True)

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
<matplotlib.axes._subplots.AxesSubplot at 0x21547a13780>
```


</div>
</div>
<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">

{:.output_png}
![png](../../images/explore/segregation/inference_wrappers_example_53_1.png)

</div>
</div>
</div>



Map of 2010:



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
gdf_2010.plot(column = 'composition',
              cmap = 'OrRd',
              figsize = (30,5),
              legend = True)

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
<matplotlib.axes._subplots.AxesSubplot at 0x2151fd3a7b8>
```


</div>
</div>
<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">

{:.output_png}
![png](../../images/explore/segregation/inference_wrappers_example_55_1.png)

</div>
</div>
</div>



A question that may rise is "Was it more or less segregated than 2000?". To answer this, we rely on simulations to test the following hypothesis:

$$H_0: Segregation\ Measure_{2000} - Segregation\ Measure_{2010} = 0$$



### Comparative Dissimilarity



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
D_2000 = Dissim(gdf_2000, 'n_nonhisp_black_persons', 'n_total_pop')
D_2010 = Dissim(gdf_2010, 'n_nonhisp_black_persons', 'n_total_pop')
D_2000.statistic - D_2010.statistic

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
0.02366612529047213
```


</div>
</div>
</div>



We can see that Riverside was more segregated in 2000 than in 2010. But, was this point difference statistically significant? We use the *random_label* approach which consists in random labelling the data between the two periods and recalculating the Dissimilarity statistic (D) in each iteration and comparing it to the original value.



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
compare_D_fit = Compare_Segregation(D_2000, D_2010, iterations_under_null = 1000, null_approach = "random_label")

```
</div>

</div>



The **Compare_Segregation** class also has a plotting method:



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
compare_D_fit.plot()

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">

{:.output_png}
![png](../../images/explore/segregation/inference_wrappers_example_62_0.png)

</div>
</div>
</div>



To access the two-tailed p-value of the test:



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
compare_D_fit.p_value

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
0.246
```


</div>
</div>
</div>



The conclusion is that, for the Dissimilarity index and 5% of significance, segregation in Riverside was not different between 2000 and 2010 (since p-value > 5%).



### Comparative Gini



Analogously, the same steps can be made for the Gini segregation index.



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
from pysal.explore.segregation.non_spatial_indexes import Gini_Seg
G_2000 = Gini_Seg(gdf_2000, 'n_nonhisp_black_persons', 'n_total_pop')
G_2010 = Gini_Seg(gdf_2010, 'n_nonhisp_black_persons', 'n_total_pop')
compare_G_fit = Compare_Segregation(G_2000, G_2010, iterations_under_null = 1000, null_approach = "random_label")
compare_G_fit.plot()

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">

{:.output_png}
![png](../../images/explore/segregation/inference_wrappers_example_68_0.png)

</div>
</div>
</div>



The absence of significance is also present as the point estimation of the difference (vertical red line) is located in the middle of the distribution of the null hypothesis simulated.



### Comparative Spatial Dissimilarity



As an example of a spatial index, comparative inference can be performed for the Spatial Dissimilarity Index (SD). For this, we use the *counterfactual_composition* approach as an example. 

In this framework, the population of the group of interest in each unit is randomized with a constraint that depends on both cumulative density functions (cdf) of the group of interest composition to the group of interest frequency of each unit. In each unit of each iteration, there is a probability of 50\% of keeping its original value or swapping to its corresponding value according of the other composition distribution cdf that it is been compared against.



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
from pysal.explore.segregation.spatial_indexes import Spatial_Dissim
SD_2000 = Spatial_Dissim(gdf_2000, 'n_nonhisp_black_persons', 'n_total_pop')
SD_2010 = Spatial_Dissim(gdf_2010, 'n_nonhisp_black_persons', 'n_total_pop')
compare_SD_fit = Compare_Segregation(SD_2000, SD_2010, iterations_under_null = 500, null_approach = "counterfactual_composition")
compare_SD_fit.plot()

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">

{:.output_png}
![png](../../images/explore/segregation/inference_wrappers_example_72_0.png)

</div>
</div>
</div>



The conclusion is that for the Spatial Dissimilarity index under this null approach, the year of 2000 was more segregated than 2010 for the non-hispanic black people in the region under study.


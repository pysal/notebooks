---
redirect_from:
  - "/explore/esda/spatial-autocorrelation-for-areal-unit-data"
interact_link: content/explore/esda/Spatial_Autocorrelation_for_Areal_Unit_Data.ipynb
kernel_name: python3
has_widgets: false
title: 'Spatial_Autocorrelation_for_Areal_Unit_Data'
prev_page:
  url: /explore/esda/intro
  title: 'esda'
next_page:
  url: /explore/giddy/intro
  title: 'giddy'
comment: "***PROGRAMMATICALLY GENERATED, DO NOT EDIT. SEE ORIGINAL FILES IN /content***"
---


# Exploratory Analysis of Spatial Data: Spatial Autocorrelation


In this notebook we introduce methods of _exploratory spatial data analysis_
that are intended to complement geovizualization through formal univariate and
multivariate statistical tests for spatial clustering.


## Imports



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
import sys
import os
sys.path.append(os.path.abspath('..'))
from pysal.explore import esda


```
</div>

</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
import pandas as pd
import geopandas as gpd
import pysal.lib as lps
import numpy as np
import matplotlib.pyplot as plt
%matplotlib inline

```
</div>

</div>



Our data set comes from the Berlin airbnb scrape taken in April 2018. This dataframe was constructed as part of the [GeoPython 2018 workshop](https://github.com/ljwolf/geopython) by [Levi Wolf](https://ljwolf.org) and [Serge Rey](https://sergerey.org). As part of the workshop a geopandas data frame was constructed with one of the columns reporting the median listing price of units in each neighborhood in Berlin:



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
df = gpd.read_file('data/neighborhoods.shp')
# was created in previous notebook with df.to_file('data/neighborhoods.shp')

```
</div>

</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
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
      <th>neighbourh</th>
      <th>neighbou_1</th>
      <th>price_x</th>
      <th>price_y</th>
      <th>median_pri</th>
      <th>geometry</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Blankenfelde/Niederschönhausen</td>
      <td>Pankow</td>
      <td>37.5</td>
      <td>37.5</td>
      <td>37.5</td>
      <td>POLYGON ((1493006.880445722 6912074.798336806,...</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Helmholtzplatz</td>
      <td>Pankow</td>
      <td>58.0</td>
      <td>58.0</td>
      <td>58.0</td>
      <td>POLYGON ((1493245.549433984 6900059.695978194,...</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Wiesbadener Straße</td>
      <td>Charlottenburg-Wilm.</td>
      <td>50.0</td>
      <td>50.0</td>
      <td>50.0</td>
      <td>POLYGON ((1481381.45206371 6885170.697768607, ...</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Schmöckwitz/Karolinenhof/Rauchfangswerder</td>
      <td>Treptow - Köpenick</td>
      <td>99.0</td>
      <td>99.0</td>
      <td>99.0</td>
      <td>POLYGON ((1526159.828554794 6872101.0436049, 1...</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Müggelheim</td>
      <td>Treptow - Köpenick</td>
      <td>25.0</td>
      <td>25.0</td>
      <td>25.0</td>
      <td>POLYGON ((1529265.085750472 6874326.842288786,...</td>
    </tr>
  </tbody>
</table>
</div>
</div>


</div>
</div>
</div>



We have an `nan` to first deal with:



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
pd.isnull(df['median_pri']).sum()

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
1
```


</div>
</div>
</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
df = df
df['median_pri'].fillna((df['median_pri'].mean()), inplace=True)


```
</div>

</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
df.plot(column='median_pri')

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
<matplotlib.axes._subplots.AxesSubplot at 0x7f3f1dcf0438>
```


</div>
</div>
<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">

{:.output_png}
![png](../../images/explore/esda/Spatial_Autocorrelation_for_Areal_Unit_Data_9_1.png)

</div>
</div>
</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
fig, ax = plt.subplots(figsize=(12,10), subplot_kw={'aspect':'equal'})
df.plot(column='median_pri', scheme='Quantiles', k=5, cmap='GnBu', legend=True, ax=ax)
#ax.set_xlim(150000, 160000)
#ax.set_ylim(208000, 215000)

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
<matplotlib.axes._subplots.AxesSubplot at 0x7f3f1d9b9a20>
```


</div>
</div>
<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">

{:.output_png}
![png](../../images/explore/esda/Spatial_Autocorrelation_for_Areal_Unit_Data_10_1.png)

</div>
</div>
</div>



## Spatial Autocorrelation

Visual inspection of the map pattern for the prices allows us to search for
spatial structure. If the spatial distribution of the prices was random, then we
should not see any clustering of similar values on the map. However, our visual
system is drawn to the darker clusters in the south west as well as the center,
and a concentration of the lighter hues (lower prices) in the north central and
south east.

Our brains are very powerful pattern recognition machines. However, sometimes
they can be too powerful and lead us to detect false positives, or patterns
where there are no statistical patterns. This is a particular concern when
dealing with visualization of irregular polygons of differning sizes and shapes.

The concept of *spatial
autocorrelation* relates to the combination of two types of similarity: spatial
similarity and attribute similarity. Although there are many different measures
of spatial autocorrelation, they all combine these two types of simmilarity into
a summary measure.

Let's use PySAL to generate these two types of similarity
measures.

### Spatial Similarity

We have already encountered spatial weights
in a previous notebook. In spatial autocorrelation analysis, the spatial weights
are used to formalize the notion of spatial similarity. As we have seen there
are many ways to define spatial weights, here we will use queen contiguity:



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
wq =  lps.weights.Queen.from_dataframe(df)
wq.transform = 'r'

```
</div>

</div>



### Attribute Similarity

So the spatial weight between neighborhoods $i$ and $j$ indicates if the two 
are neighbors (i.e., geographically similar). What we also need is a measure of
attribute similarity to pair up with this concept of spatial similarity. The
**spatial lag** is a derived variable that accomplishes this for us. For neighborhood
$i$ the spatial lag is defined as: $$ylag_i = \sum_j w_{i,j} y_j$$



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
y = df['median_pri']
ylag = lps.weights.lag_spatial(wq, y)

```
</div>

</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
ylag

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
array([45.2       , 52.625     , 45.75      , 32.5       , 63.5       ,
       42.        , 45.625     , 44.14285714, 43.33333333, 38.75      ,
       41.5       , 50.8       , 36.6875    , 54.36363636, 54.375     ,
       38.92857143, 38.125     , 50.9       , 35.6875    , 59.66666667,
       46.875     , 46.92857143, 49.58333333, 47.25      , 53.25      ,
       40.57142857, 37.66666667, 37.14285714, 40.75      , 41.5       ,
       45.9       , 35.3       , 47.9375    , 47.33333333, 40.        ,
       44.        , 58.3       , 53.16666667, 41.1459854 , 43.75      ,
       51.625     , 52.3       , 50.5       , 46.91666667, 47.        ,
       38.125     , 35.33333333, 48.83333333, 46.6       , 43.125     ,
       39.95498783, 41.33333333, 42.        , 44.43248175, 55.66666667,
       46.2       , 47.33333333, 49.84124088, 47.93248175, 42.92857143,
       43.4       , 40.78571429, 37.42857143, 32.75      , 45.57142857,
       51.25      , 44.        , 33.33333333, 33.25      , 42.        ,
       40.        , 34.8       , 43.57142857, 41.75      , 43.85714286,
       39.14285714, 42.25      , 47.21428571, 46.        , 51.2       ,
       36.66666667, 39.875     , 35.375     , 44.8       , 42.25      ,
       36.6       , 38.66666667, 41.11111111, 40.2       , 38.33333333,
       39.625     , 43.5       , 39.1       , 40.9       , 40.625     ,
       48.625     , 49.5       , 50.02554745, 37.42857143, 39.83333333,
       51.58333333, 48.6875    , 50.5       , 38.5       , 41.5       ,
       44.04545455, 36.33333333, 45.1875    , 40.85714286, 55.875     ,
       58.        , 47.14285714, 38.16666667, 44.7       , 44.1       ,
       45.5       , 50.83333333, 44.83333333, 40.25      , 40.        ,
       42.66666667, 44.125     , 37.6       , 39.25      , 34.25      ,
       30.33333333, 36.14285714, 38.75      , 42.16666667, 39.        ,
       38.92857143, 36.75      , 34.        , 41.375     , 36.5       ,
       38.        , 35.91666667, 36.        ])
```


</div>
</div>
</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
from pysal.viz import mapclassify as mc
ylagq5 = mc.Quantiles(ylag, k=5)

```
</div>

</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
f, ax = plt.subplots(1, figsize=(9, 9))
df.assign(cl=ylagq5.yb).plot(column='cl', categorical=True, \
        k=5, cmap='GnBu', linewidth=0.1, ax=ax, \
        edgecolor='white', legend=True)
ax.set_axis_off()
plt.title("Spatial Lag Median Price (Quintiles)")

plt.show()

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">

{:.output_png}
![png](../../images/explore/esda/Spatial_Autocorrelation_for_Areal_Unit_Data_17_0.png)

</div>
</div>
</div>



The quintile map for the spatial lag tends to enhance the impression of value
similarity in space. It is, in effect, a local smoother.



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
df['lag_median_pri'] = ylag
f,ax = plt.subplots(1,2,figsize=(2.16*4,4))
df.plot(column='median_pri', ax=ax[0], edgecolor='k',
        scheme="quantiles",  k=5, cmap='GnBu')
ax[0].axis(df.total_bounds[np.asarray([0,2,1,3])])
ax[0].set_title("Price")
df.plot(column='lag_median_pri', ax=ax[1], edgecolor='k',
        scheme='quantiles', cmap='GnBu', k=5)
ax[1].axis(df.total_bounds[np.asarray([0,2,1,3])])
ax[1].set_title("Spatial Lag Price")
ax[0].axis('off')
ax[1].axis('off')
plt.show()

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">

{:.output_png}
![png](../../images/explore/esda/Spatial_Autocorrelation_for_Areal_Unit_Data_19_0.png)

</div>
</div>
</div>



However, we still have
the challenge of visually associating the value of the prices in a neighborhod
with the value of the spatial lag of values for the focal unit. The latter is a
weighted average of homicide rates in the focal county's neighborhood.

To complement the geovisualization of these associations we can turn to formal
statistical measures of spatial autocorrelation.


## Global Spatial Autocorrelation

We begin with a simple case where the variable under consideration is binary.
This is useful to unpack the logic of spatial autocorrelation tests. So  even though
our attribute is a continuously valued one, we will convert it to a binary case
to illustrate the key concepts:

### Binary Case



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
y.median()


```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
42.0
```


</div>
</div>
</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
yb = y > y.median()
sum(yb)

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
68
```


</div>
</div>
</div>



We have 68 neighborhoods with list prices above the median and 70 below the
median (recall the issue with ties).



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
yb = y > y.median()
labels = ["0 Low", "1 High"]
yb = [labels[i] for i in 1*yb] 
df['yb'] = yb

```
</div>

</div>



The spatial distribution of the binary variable immediately raises questions
about the juxtaposition of the "black" and "white" areas.



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
fig, ax = plt.subplots(figsize=(12,10), subplot_kw={'aspect':'equal'})
df.plot(column='yb', cmap='binary', edgecolor='grey', legend=True, ax=ax)

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
<matplotlib.axes._subplots.AxesSubplot at 0x7f3f1c34f2e8>
```


</div>
</div>
<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">

{:.output_png}
![png](../../images/explore/esda/Spatial_Autocorrelation_for_Areal_Unit_Data_26_1.png)

</div>
</div>
</div>



### Join counts

One way to formalize a test for spatial autocorrelation in a binary attribute is
to consider the so-called _joins_. A join exists for each neighbor pair of
observations, and the joins are reflected in our binary spatial weights object
`wq`. 

Each unit can take on one of two values "Black" or "White", and so for a given
pair of neighboring locations there are three different types of joins that can
arise:

- Black Black (BB)
- White White (WW)
- Black White (or White Black) (BW)

Given that we have 68 Black polygons on our map, what is the number of Black
Black (BB) joins we could expect if the process were such that the Black
polygons were randomly assigned on the map? This is the logic of join count statistics.

We can use the `esda` package from PySAL to carry out join count analysis:



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
from pysal.explore import esda 
yb = 1 * (y > y.median()) # convert back to binary
wq =  lps.weights.Queen.from_dataframe(df)
wq.transform = 'b'
np.random.seed(12345)
jc = esda.join_counts.Join_Counts(yb, wq)

```
</div>

</div>



The resulting object stores the observed counts for the different types of joins:



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
jc.bb

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
121.0
```


</div>
</div>
</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
jc.ww

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
114.0
```


</div>
</div>
</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
jc.bw

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
150.0
```


</div>
</div>
</div>



Note that the three cases exhaust all possibilities:



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
jc.bb + jc.ww + jc.bw

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
385.0
```


</div>
</div>
</div>



and



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
wq.s0 / 2

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
385.0
```


</div>
</div>
</div>



which is the unique number of joins in the spatial weights object.

Our object tells us we have observed 121 BB joins:



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
jc.bb

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
121.0
```


</div>
</div>
</div>



The critical question for us, is whether this is a departure from what we would
expect if the process generating the spatial distribution of the Black polygons
were a completely random one? To answer this, PySAL uses random spatial
permutations of the observed attribute values to generate a realization under
the null of _complete spatial randomness_ (CSR). This is repeated a large number
of times (999 default) to construct a reference distribution to evaluate the
statistical significance of our observed counts.

The average number of BB joins from the synthetic realizations is:



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
jc.mean_bb

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
92.65365365365365
```


</div>
</div>
</div>



which is less than our observed count. The question is whether our observed
value is so different from the expectation that we would reject the null of CSR?



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
import seaborn as sbn
sbn.kdeplot(jc.sim_bb, shade=True)
plt.vlines(jc.bb, 0, 0.075, color='r')
plt.vlines(jc.mean_bb, 0,0.075)
plt.xlabel('BB Counts')


```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
Text(0.5,0,'BB Counts')
```


</div>
</div>
<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">

{:.output_png}
![png](../../images/explore/esda/Spatial_Autocorrelation_for_Areal_Unit_Data_42_1.png)

</div>
</div>
</div>



The density portrays the distribution of the BB counts, with the black vertical
line indicating the mean BB count from the synthetic realizations and the red
line the observed BB count for our prices. Clearly our observed value is
extremely high. A pseudo p-value summarizes this:



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
jc.p_sim_bb


```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
0.001
```


</div>
</div>
</div>



Since this is below conventional significance levels, we would reject the null
of complete spatial randomness in favor of spatial autocorrelation in market prices.


### Continuous Case

The join count analysis is based on a binary attribute, which can cover many
interesting empirical applications where one is interested in presence and
absence type phenomena. In our case, we artificially created the binary variable,
and in the process we throw away a lot of information in our originally
continuous attribute. Turning back to the original variable, we can explore
other tests for spatial autocorrelation for the continuous case.

First, we transform our weights to be row-standardized, from the current binary state:



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
wq.transform = 'r'

```
</div>

</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
y = df['median_pri']

```
</div>

</div>



Moran's I is a test for global autocorrelation for a continuous attribute:



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
np.random.seed(12345)
mi = esda.moran.Moran(y, wq)
mi.I

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
0.09715984916381672
```


</div>
</div>
</div>



Again, our value for the statistic needs to be interpreted against a reference
distribution under the null of CSR. PySAL uses a similar approach as we saw in
the join count analysis: random spatial permutations.



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
import seaborn as sbn
sbn.kdeplot(mi.sim, shade=True)
plt.vlines(mi.I, 0, 1, color='r')
plt.vlines(mi.EI, 0,1)
plt.xlabel("Moran's I")


```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
Text(0.5,0,"Moran's I")
```


</div>
</div>
<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">

{:.output_png}
![png](../../images/explore/esda/Spatial_Autocorrelation_for_Areal_Unit_Data_51_1.png)

</div>
</div>
</div>



Here our observed value is again in the upper tail, although visually it does
not look as extreme relative to the binary case. Yet, it is still statistically significant:



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
mi.p_sim

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
0.02
```


</div>
</div>
</div>



## Local Autocorrelation: Hot Spots, Cold Spots, and Spatial Outliers

In addition to the Global autocorrelation statistics, PySAL has many local
autocorrelation statistics. Let's compute a local Moran statistic for the same
d



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
np.random.seed(12345)
from pysal.explore import esda

```
</div>

</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
wq.transform = 'r'
lag_price = lps.weights.lag_spatial(wq, df['median_pri'])


```
</div>

</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
price = df['median_pri']
b, a = np.polyfit(price, lag_price, 1)
f, ax = plt.subplots(1, figsize=(9, 9))

plt.plot(price, lag_price, '.', color='firebrick')

 # dashed vert at mean of the price
plt.vlines(price.mean(), lag_price.min(), lag_price.max(), linestyle='--')
 # dashed horizontal at mean of lagged price 
plt.hlines(lag_price.mean(), price.min(), price.max(), linestyle='--')

# red line of best fit using global I as slope
plt.plot(price, a + b*price, 'r')
plt.title('Moran Scatterplot')
plt.ylabel('Spatial Lag of Price')
plt.xlabel('Price')
plt.show()


```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">

{:.output_png}
![png](../../images/explore/esda/Spatial_Autocorrelation_for_Areal_Unit_Data_57_0.png)

</div>
</div>
</div>



Now, instead of a single $I$ statistic, we have an *array* of local $I_i$
statistics, stored in the `.Is` attribute, and p-values from the simulation are
in `p_sim`.



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
li = esda.moran.Moran_Local(y, wq)

```
</div>

</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
li.q

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
array([2, 1, 1, 4, 2, 3, 2, 1, 3, 4, 3, 1, 3, 1, 1, 3, 3, 2, 3, 1, 1, 1,
       1, 2, 2, 3, 4, 4, 3, 4, 2, 3, 1, 1, 3, 1, 1, 1, 4, 1, 1, 1, 1, 1,
       2, 3, 3, 2, 2, 4, 3, 3, 3, 2, 1, 1, 1, 1, 1, 3, 3, 3, 3, 4, 2, 2,
       2, 4, 4, 3, 3, 4, 3, 4, 2, 4, 4, 1, 2, 1, 4, 3, 4, 2, 3, 3, 3, 3,
       3, 3, 4, 3, 4, 3, 4, 1, 1, 1, 3, 3, 1, 1, 1, 3, 4, 1, 4, 2, 3, 1,
       1, 2, 4, 2, 2, 2, 1, 1, 3, 3, 4, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
       3, 3, 4, 3, 3, 3])
```


</div>
</div>
</div>



We can again test for local clustering using permutations, but here we use
conditional random permutations (different distributions for each focal location)



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
(li.p_sim < 0.05).sum()

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
24
```


</div>
</div>
</div>



We can distinguish the specific type of local spatial association reflected in
the four quadrants of the Moran Scatterplot above:



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
sig = li.p_sim < 0.05
hotspot = sig * li.q==1
coldspot = sig * li.q==3
doughnut = sig * li.q==2
diamond = sig * li.q==4

```
</div>

</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
spots = ['n.sig.', 'hot spot']
labels = [spots[i] for i in hotspot*1]

```
</div>

</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
df = df
from matplotlib import colors
hmap = colors.ListedColormap(['red', 'lightgrey'])
f, ax = plt.subplots(1, figsize=(9, 9))
df.assign(cl=labels).plot(column='cl', categorical=True, \
        k=2, cmap=hmap, linewidth=0.1, ax=ax, \
        edgecolor='white', legend=True)
ax.set_axis_off()
plt.show()

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">

{:.output_png}
![png](../../images/explore/esda/Spatial_Autocorrelation_for_Areal_Unit_Data_66_0.png)

</div>
</div>
</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
spots = ['n.sig.', 'cold spot']
labels = [spots[i] for i in coldspot*1]

```
</div>

</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
df = df
from matplotlib import colors
hmap = colors.ListedColormap(['blue', 'lightgrey'])
f, ax = plt.subplots(1, figsize=(9, 9))
df.assign(cl=labels).plot(column='cl', categorical=True, \
        k=2, cmap=hmap, linewidth=0.1, ax=ax, \
        edgecolor='white', legend=True)
ax.set_axis_off()
plt.show()

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">

{:.output_png}
![png](../../images/explore/esda/Spatial_Autocorrelation_for_Areal_Unit_Data_68_0.png)

</div>
</div>
</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
spots = ['n.sig.', 'doughnut']
labels = [spots[i] for i in doughnut*1]

```
</div>

</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
df = df
from matplotlib import colors
hmap = colors.ListedColormap(['lightblue', 'lightgrey'])
f, ax = plt.subplots(1, figsize=(9, 9))
df.assign(cl=labels).plot(column='cl', categorical=True, \
        k=2, cmap=hmap, linewidth=0.1, ax=ax, \
        edgecolor='white', legend=True)
ax.set_axis_off()
plt.show()

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">

{:.output_png}
![png](../../images/explore/esda/Spatial_Autocorrelation_for_Areal_Unit_Data_70_0.png)

</div>
</div>
</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
spots = ['n.sig.', 'diamond']
labels = [spots[i] for i in diamond*1]

```
</div>

</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
df = df
from matplotlib import colors
hmap = colors.ListedColormap(['pink', 'lightgrey'])
f, ax = plt.subplots(1, figsize=(9, 9))
df.assign(cl=labels).plot(column='cl', categorical=True, \
        k=2, cmap=hmap, linewidth=0.1, ax=ax, \
        edgecolor='white', legend=True)
ax.set_axis_off()
plt.show()

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">

{:.output_png}
![png](../../images/explore/esda/Spatial_Autocorrelation_for_Areal_Unit_Data_72_0.png)

</div>
</div>
</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
sig = 1 * (li.p_sim < 0.05)
hotspot = 1 * (sig * li.q==1)
coldspot = 3 * (sig * li.q==3)
doughnut = 2 * (sig * li.q==2)
diamond = 4 * (sig * li.q==4)
spots = hotspot + coldspot + doughnut + diamond
spots

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
array([0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 3, 1, 0, 0, 0, 0, 3, 1, 0, 0,
       0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0,
       0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0,
       0, 4, 4, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0,
       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 1,
       1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 3, 3, 3, 0, 0, 0, 0, 0,
       3, 0, 0, 0, 3, 0])
```


</div>
</div>
</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
spot_labels = [ '0 ns', '1 hot spot', '2 doughnut', '3 cold spot', '4 diamond']
labels = [spot_labels[i] for i in spots]

```
</div>

</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python

from matplotlib import colors
hmap = colors.ListedColormap([ 'lightgrey', 'red', 'lightblue', 'blue', 'pink'])
f, ax = plt.subplots(1, figsize=(9, 9))
df.assign(cl=labels).plot(column='cl', categorical=True, \
        k=2, cmap=hmap, linewidth=0.1, ax=ax, \
        edgecolor='white', legend=True)
ax.set_axis_off()
plt.show()

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">

{:.output_png}
![png](../../images/explore/esda/Spatial_Autocorrelation_for_Areal_Unit_Data_75_0.png)

</div>
</div>
</div>


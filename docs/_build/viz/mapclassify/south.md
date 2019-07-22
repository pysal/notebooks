---
interact_link: content/viz/mapclassify/south.ipynb
kernel_name: python3
has_widgets: false
title: 'south'
prev_page:
  url: /viz/mapclassify/deprecate
  title: 'deprecate'
next_page:
  url: /viz/mapclassify/maximum_breaks
  title: 'maximum_breaks'
comment: "***PROGRAMMATICALLY GENERATED, DO NOT EDIT. SEE ORIGINAL FILES IN /content***"
---


<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
import sys
import os
sys.path.append(os.path.abspath('..'))
from pysal.viz import mapclassify as mc
import pysal.lib
import geopandas as gpd
import matplotlib.pyplot as plt

%matplotlib inline

```
</div>

</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
df = gpd.read_file(pysal.lib.examples.get_path('south.shp'))

```
</div>

</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
hr60_q10 = mc.Quantiles(df['HR60'], k=10)
hr60_q10

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
                Quantiles                
 
Lower            Upper              Count
=========================================
         x[i] <=  0.000               180
 0.000 < x[i] <=  2.497               103
 2.497 < x[i] <=  3.927               141
 3.927 < x[i] <=  5.104               141
 5.104 < x[i] <=  6.245               141
 6.245 < x[i] <=  7.621               141
 7.621 < x[i] <=  9.188               141
 9.188 < x[i] <= 10.981               141
10.981 < x[i] <= 14.313               141
14.313 < x[i] <= 92.937               142
```


</div>
</div>
</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
fig, ax = plt.subplots(figsize=(12,10), subplot_kw={'aspect':'equal'})
df.assign(cl=hr60_q10.yb).plot(column='cl', categorical=True, \
                              k=10, cmap='OrRd', linewidth=0.1, ax=ax, \
                              edgecolor='white', legend=True)
ax.set_axis_off()
plt.title('HR60 Deciles')
plt.savefig('hr60q10.png')

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">

{:.output_png}
![png](../../images/viz/mapclassify/south_3_0.png)

</div>
</div>
</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
import numpy as np
np.random.seed(12345)
hr60_fj10 = mc.FisherJenks(df['HR60'], k=10)
hr60_fj10

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
               FisherJenks               
 
Lower            Upper              Count
=========================================
         x[i] <=  1.707               216
 1.707 < x[i] <=  4.446               278
 4.446 < x[i] <=  7.082               287
 7.082 < x[i] <= 10.022               288
10.022 < x[i] <= 13.587               176
13.587 < x[i] <= 19.600               121
19.600 < x[i] <= 28.773                34
28.773 < x[i] <= 40.744                 8
40.744 < x[i] <= 53.305                 3
53.305 < x[i] <= 92.937                 1
```


</div>
</div>
</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
fig, ax = plt.subplots(figsize=(12,10), subplot_kw={'aspect':'equal'})
df.assign(cl=hr60_fj10.yb).plot(column='cl', categorical=True, \
                              k=10, cmap='OrRd', linewidth=0.1, ax=ax, \
                              edgecolor='white', legend=True)
ax.set_axis_off()
plt.title('HR60 Fisher-Jenks')
plt.savefig('hr60fj10.png')

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">

{:.output_png}
![png](../../images/viz/mapclassify/south_5_0.png)

</div>
</div>
</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
hr60_mb10 = mc.MaximumBreaks(df['HR60'], k=10)


fig, ax = plt.subplots(figsize=(12,10), subplot_kw={'aspect':'equal'})
df.assign(cl=hr60_mb10.yb).plot(column='cl', categorical=True, \
                              k=10, cmap='OrRd', linewidth=0.1, ax=ax, \
                              edgecolor='white', legend=True)
ax.set_axis_off()
plt.title('HR60 Maximum Breaks')
plt.savefig('hr60mb10.png')

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">

{:.output_png}
![png](../../images/viz/mapclassify/south_6_0.png)

</div>
</div>
</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
hr60_ea10 = mc.EqualInterval(df['HR60'], k=10)


fig, ax = plt.subplots(figsize=(12,10), subplot_kw={'aspect':'equal'})
df.assign(cl=hr60_ea10.yb).plot(column='cl', categorical=True, \
                              k=10, cmap='OrRd', linewidth=0.1, ax=ax, \
                              edgecolor='white', legend=True)
ax.set_axis_off()
plt.title('HR60 Equal Interval')

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
Text(0.5, 1, 'HR60 Equal Interval')
```


</div>
</div>
<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">

{:.output_png}
![png](../../images/viz/mapclassify/south_7_1.png)

</div>
</div>
</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
fig, ax = plt.subplots(figsize=(12,10), subplot_kw={'aspect':'equal'})
df.plot(column='HR60', ax=ax)

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
<matplotlib.axes._subplots.AxesSubplot at 0x7f1b25913198>
```


</div>
</div>
<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">

{:.output_png}
![png](../../images/viz/mapclassify/south_8_1.png)

</div>
</div>
</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
hr60_q5 = mc.Quantiles(df['HR60'], k=5)

```
</div>

</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
hr60_q5

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
                Quantiles                
 
Lower            Upper              Count
=========================================
         x[i] <=  2.497               283
 2.497 < x[i] <=  5.104               282
 5.104 < x[i] <=  7.621               282
 7.621 < x[i] <= 10.981               282
10.981 < x[i] <= 92.937               283
```


</div>
</div>
</div>


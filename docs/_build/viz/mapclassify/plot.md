---
interact_link: content/viz/mapclassify/plot.ipynb
kernel_name: python3
has_widgets: false
title: 'plot'
prev_page:
  url: /viz/mapclassify/intro
  title: 'mapclassify'
next_page:
  url: /viz/mapclassify/deprecate
  title: 'deprecate'
comment: "***PROGRAMMATICALLY GENERATED, DO NOT EDIT. SEE ORIGINAL FILES IN /content***"
---


<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
import pysal.lib 
import geopandas as gpd
from pysal.viz import mapclassify as mc

```
</div>

</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
columbus = gpd.read_file(pysal.lib.examples.get_path('columbus.shp'))

```
</div>

</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
q5 = mc.Quantiles(columbus.CRIME, k=5)

```
</div>

</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
q5

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
               Quantiles                
 
Lower            Upper             Count
========================================
         x[i] <= 19.023               10
19.023 < x[i] <= 29.326               10
29.326 < x[i] <= 39.025                9
39.025 < x[i] <= 53.161               10
53.161 < x[i] <= 68.892               10
```


</div>
</div>
</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
q5.plot(columbus)

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
(<Figure size 640x480 with 1 Axes>,
 <matplotlib.axes._subplots.AxesSubplot at 0x7f893be186d8>)
```


</div>
</div>
</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
q5.plot(columbus, axis_on=False)

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
(<Figure size 432x288 with 1 Axes>,
 <matplotlib.axes._subplots.AxesSubplot at 0x7f893bb0acc0>)
```


</div>
</div>
<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">

{:.output_png}
![png](../../images/viz/mapclassify/plot_5_1.png)

</div>
</div>
</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
q5.plot(columbus, axis_on=False, cmap='Blues')

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
(<Figure size 432x288 with 1 Axes>,
 <matplotlib.axes._subplots.AxesSubplot at 0x7f893ba1bb70>)
```


</div>
</div>
<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">

{:.output_png}
![png](../../images/viz/mapclassify/plot_6_1.png)

</div>
</div>
</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
f = q5.plot(columbus, axis_on=False, cmap='Blues')

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">

{:.output_png}
![png](../../images/viz/mapclassify/plot_7_0.png)

</div>
</div>
</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
f = q5.plot(columbus, axis_on=False, cmap='Blues', title='Columbus, OH')

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">

{:.output_png}
![png](../../images/viz/mapclassify/plot_8_0.png)

</div>
</div>
</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
f = q5.plot(columbus, axis_on=False, cmap='Blues', title='Columbus, OH', \
           legend=True)

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">

{:.output_png}
![png](../../images/viz/mapclassify/plot_9_0.png)

</div>
</div>
</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
f = q5.plot(columbus, axis_on=False, cmap='Blues', title='Columbus, OH', \
           legend=True, legend_kwds={'loc':'upper right'})

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">

{:.output_png}
![png](../../images/viz/mapclassify/plot_10_0.png)

</div>
</div>
</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
f = q5.plot(columbus, axis_on=False, cmap='Blues', title='Columbus, OH', \
           legend=True, legend_kwds={'loc':'upper left', 'title': 'Crime Rate'})

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">

{:.output_png}
![png](../../images/viz/mapclassify/plot_11_0.png)

</div>
</div>
</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
f = q5.plot(columbus, axis_on=False, cmap='Blues', title='Columbus, OH', \
           legend=True, legend_kwds={'loc':'upper left', 'title': 'Crime Rate'}, \
           file_name='crime.png')

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">

{:.output_png}
![png](../../images/viz/mapclassify/plot_12_0.png)

</div>
</div>
</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
f = q5.plot(columbus, axis_on=False, cmap='Blues', title='Columbus, OH', \
           legend=True, legend_kwds={'loc':'upper left', 'title': 'Crime Rate, 1988'}, \
           file_name='crime.png', border_color='green', border_width=2.0)

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">

{:.output_png}
![png](../../images/viz/mapclassify/plot_13_0.png)

</div>
</div>
</div>


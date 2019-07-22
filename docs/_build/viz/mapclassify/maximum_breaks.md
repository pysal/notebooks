---
redirect_from:
  - "/viz/mapclassify/maximum-breaks"
interact_link: content/viz/mapclassify/maximum_breaks.ipynb
kernel_name: python3
has_widgets: false
title: 'maximum_breaks'
prev_page:
  url: /viz/mapclassify/south
  title: 'south'
next_page:
  url: /viz/splot/intro
  title: 'splot'
comment: "***PROGRAMMATICALLY GENERATED, DO NOT EDIT. SEE ORIGINAL FILES IN /content***"
---


<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
import sys
import os
sys.path.append(os.path.abspath('..'))
from pysal.viz import mapclassify as mc

```
</div>

</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
y = mc.load_example()

```
</div>

</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
mc.MaximumBreaks(y, k=4)

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
               MaximumBreaks                
 
 Lower              Upper              Count
============================================
           x[i] <=  228.490               52
 228.490 < x[i] <=  546.675                4
 546.675 < x[i] <= 2417.150                1
2417.150 < x[i] <= 4111.450                1
```


</div>
</div>
</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
mc.MaximumBreaks(y, k=7)

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
               MaximumBreaks                
 
 Lower              Upper              Count
============================================
           x[i] <=  146.005               50
 146.005 < x[i] <=  228.490                2
 228.490 < x[i] <=  291.020                1
 291.020 < x[i] <=  350.210                2
 350.210 < x[i] <=  546.675                1
 546.675 < x[i] <= 2417.150                1
2417.150 < x[i] <= 4111.450                1
```


</div>
</div>
</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
mb7 = mc.MaximumBreaks(y, k=7)

```
</div>

</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
mb7.bins

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
array([ 146.005,  228.49 ,  291.02 ,  350.21 ,  546.675, 2417.15 ,
       4111.45 ])
```


</div>
</div>
</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
mb7.counts

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
array([50,  2,  1,  2,  1,  1,  1])
```


</div>
</div>
</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
mb7.yb

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
array([3, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0,
       0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 1, 0, 0, 0, 6, 0, 0, 3, 0, 2, 0,
       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
```


</div>
</div>
</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
mb7.adcm

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
727.3200000000002
```


</div>
</div>
</div>


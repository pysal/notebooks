---
interact_link: content/viz/mapclassify/deprecate.ipynb
kernel_name: python3
has_widgets: false
title: 'deprecate'
prev_page:
  url: /viz/mapclassify/plot
  title: 'plot'
next_page:
  url: /viz/mapclassify/south
  title: 'south'
comment: "***PROGRAMMATICALLY GENERATED, DO NOT EDIT. SEE ORIGINAL FILES IN /content***"
---


## Deprecations with version 2.1.0



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
mc.Equal_Interval(columbus.CRIME)

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
             Equal Interval             
 
Lower            Upper             Count
========================================
         x[i] <= 13.921                2
13.921 < x[i] <= 27.664               16
27.664 < x[i] <= 41.407               14
41.407 < x[i] <= 55.149               10
55.149 < x[i] <= 68.892                7
```


</div>
</div>
</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
qc = mc.EqualInterval(columbus.CRIME)

```
</div>

</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
mc.HeadTail_Breaks(columbus.CRIME)

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
             HeadTailBreaks             
 
Lower            Upper             Count
========================================
         x[i] <= 35.129               25
35.129 < x[i] <= 49.361               12
49.361 < x[i] <= 57.542                8
57.542 < x[i] <= 63.304                3
63.304 < x[i] <= 68.892                1
```


</div>
</div>
</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
mc.HeadTailBreaks(columbus.CRIME)

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
             HeadTailBreaks             
 
Lower            Upper             Count
========================================
         x[i] <= 35.129               25
35.129 < x[i] <= 49.361               12
49.361 < x[i] <= 57.542                8
57.542 < x[i] <= 63.304                3
63.304 < x[i] <= 68.892                1
```


</div>
</div>
</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
mc.Box_Plot(columbus.CRIME)

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
                 Box Plot                 
 
 Lower            Upper              Count
==========================================
          x[i] <= -22.757                0
-22.757 < x[i] <=  20.049               13
 20.049 < x[i] <=  34.001               12
 34.001 < x[i] <=  48.585               12
 48.585 < x[i] <=  91.391               12
```


</div>
</div>
</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
mc.BoxPlot(columbus.CRIME)

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
                 Box Plot                 
 
 Lower            Upper              Count
==========================================
          x[i] <= -22.757                0
-22.757 < x[i] <=  20.049               13
 20.049 < x[i] <=  34.001               12
 34.001 < x[i] <=  48.585               12
 48.585 < x[i] <=  91.391               12
```


</div>
</div>
</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
mc.Natural_Breaks(columbus.CRIME)

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
             NaturalBreaks              
 
Lower            Upper             Count
========================================
         x[i] <=  0.224                2
 0.224 < x[i] <= 22.541               12
22.541 < x[i] <= 34.001               11
34.001 < x[i] <= 48.585               12
48.585 < x[i] <= 68.892               12
```


</div>
</div>
</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
mc.NaturalBreaks(columbus.CRIME)

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
             NaturalBreaks              
 
Lower            Upper             Count
========================================
         x[i] <=  0.224                2
 0.224 < x[i] <= 22.541               12
22.541 < x[i] <= 34.001               11
34.001 < x[i] <= 48.585               12
48.585 < x[i] <= 68.892               12
```


</div>
</div>
</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
mc.Fisher_Jenks(columbus.CRIME)

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
              FisherJenks               
 
Lower            Upper             Count
========================================
         x[i] <=  0.224                2
 0.224 < x[i] <= 22.541               12
22.541 < x[i] <= 34.001               11
34.001 < x[i] <= 48.585               12
48.585 < x[i] <= 68.892               12
```


</div>
</div>
</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
mc.FisherJenks(columbus.CRIME)

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
              FisherJenks               
 
Lower            Upper             Count
========================================
         x[i] <=  0.224                2
 0.224 < x[i] <= 22.541               12
22.541 < x[i] <= 34.001               11
34.001 < x[i] <= 48.585               12
48.585 < x[i] <= 68.892               12
```


</div>
</div>
</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
mc.Std_Mean(columbus.CRIME)

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
                StdMean                 
 
Lower            Upper             Count
========================================
         x[i] <=  1.665                2
 1.665 < x[i] <= 18.397                6
18.397 < x[i] <= 51.861               30
51.861 < x[i] <= 68.593               10
68.593 < x[i] <= 68.892                1
```


</div>
</div>
</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
mc.StdMean(columbus.CRIME)

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
                StdMean                 
 
Lower            Upper             Count
========================================
         x[i] <=  1.665                2
 1.665 < x[i] <= 18.397                6
18.397 < x[i] <= 51.861               30
51.861 < x[i] <= 68.593               10
68.593 < x[i] <= 68.892                1
```


</div>
</div>
</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
mc.User_Defined(columbus.CRIME, bins=[51.862, 69.0])

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
              UserDefined               
 
Lower            Upper             Count
========================================
         x[i] <= 51.862               38
51.862 < x[i] <= 69.000               11
```


</div>
</div>
</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
mc.UserDefined(columbus.CRIME, bins=[51.862, 69.0])

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
              UserDefined               
 
Lower            Upper             Count
========================================
         x[i] <= 51.862               38
51.862 < x[i] <= 69.000               11
```


</div>
</div>
</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
mc.Jenks_Caspall(columbus.CRIME)

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
              JenksCaspall              
 
Lower            Upper             Count
========================================
         x[i] <= 20.049               13
20.049 < x[i] <= 29.028                7
29.028 < x[i] <= 36.869                7
36.869 < x[i] <= 48.585               10
48.585 < x[i] <= 68.892               12
```


</div>
</div>
</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
mc.JenksCaspall(columbus.CRIME)

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
              JenksCaspall              
 
Lower            Upper             Count
========================================
         x[i] <= 20.049               13
20.049 < x[i] <= 29.028                7
29.028 < x[i] <= 36.869                7
36.869 < x[i] <= 48.585               10
48.585 < x[i] <= 68.892               12
```


</div>
</div>
</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
mc.Jenks_Caspall_Sampled(columbus.CRIME)

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
          JenksCaspallSampled           
 
Lower            Upper             Count
========================================
         x[i] <= 16.492                6
16.492 < x[i] <= 41.968               27
41.968 < x[i] <= 42.445                1
42.445 < x[i] <= 61.299               13
61.299 < x[i] <= 68.892                2
```


</div>
</div>
</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
mc.Jenks_Caspall_Forced(columbus.CRIME)

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
           JenksCaspallForced           
 
Lower            Upper             Count
========================================
         x[i] <= 18.905               10
18.905 < x[i] <= 29.028               10
29.028 < x[i] <= 38.426                9
38.426 < x[i] <= 52.794               10
52.794 < x[i] <= 68.892               10
```


</div>
</div>
</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
mc.JenksCaspallForced(columbus.CRIME)

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
           JenksCaspallForced           
 
Lower            Upper             Count
========================================
         x[i] <= 18.905               10
18.905 < x[i] <= 29.028               10
29.028 < x[i] <= 38.426                9
38.426 < x[i] <= 52.794               10
52.794 < x[i] <= 68.892               10
```


</div>
</div>
</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
mc.JenksCaspallSampled(columbus.CRIME)

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
          JenksCaspallSampled           
 
Lower            Upper             Count
========================================
         x[i] <= 18.905               10
18.905 < x[i] <= 34.001               15
34.001 < x[i] <= 54.522               16
54.522 < x[i] <= 54.839                1
54.839 < x[i] <= 68.892                7
```


</div>
</div>
</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
mc.Max_P_Classifier(columbus.CRIME, k=5)

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
                  MaxP                  
 
Lower            Upper             Count
========================================
         x[i] <= 27.823               19
27.823 < x[i] <= 29.028                1
29.028 < x[i] <= 39.175               10
39.175 < x[i] <= 50.732                8
50.732 < x[i] <= 68.892               11
```


</div>
</div>
</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
mc.MaxP(columbus.CRIME, k=5)

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
                  MaxP                  
 
Lower            Upper             Count
========================================
         x[i] <= 27.823               19
27.823 < x[i] <= 29.028                1
29.028 < x[i] <= 39.175               10
39.175 < x[i] <= 50.732                8
50.732 < x[i] <= 68.892               11
```


</div>
</div>
</div>


---
redirect_from:
  - "/viz/mapclassify/maximum-breaks"
interact_link: content/viz/mapclassify/maximum_breaks.ipynb
title: 'maximum_breaks'
prev_page:
  url: /viz/mapclassify/intro
  title: 'mapclassify'
next_page:
  url: /viz/mapclassify/south
  title: 'south'
comment: "***PROGRAMMATICALLY GENERATED, DO NOT EDIT. SEE ORIGINAL FILES IN /content***"
---



{:.input_area}
```python
import sys
import os
sys.path.append(os.path.abspath('..'))
import mapclassify as mc
```




{:.input_area}
```python
y = mc.load_example()
```




{:.input_area}
```python
mc.Maximum_Breaks(y, k=4)
```





{:.output_data_text}
```
               Maximum_Breaks               
 
 Lower              Upper              Count
============================================
           x[i] <=  228.490               52
 228.490 < x[i] <=  546.675                4
 546.675 < x[i] <= 2417.150                1
2417.150 < x[i] <= 4111.450                1
```





{:.input_area}
```python
mc.Maximum_Breaks(y, k=7)
```





{:.output_data_text}
```
               Maximum_Breaks               
 
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





{:.input_area}
```python
mb7 = mc.Maximum_Breaks(y, k=7)
```




{:.input_area}
```python
mb7.bins
```





{:.output_data_text}
```
array([ 146.005,  228.49 ,  291.02 ,  350.21 ,  546.675, 2417.15 ,
       4111.45 ])
```





{:.input_area}
```python
mb7.counts
```





{:.output_data_text}
```
array([50,  2,  1,  2,  1,  1,  1])
```





{:.input_area}
```python
mb7.yb
```





{:.output_data_text}
```
array([3, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0,
       0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 1, 0, 0, 0, 6, 0, 0, 3, 0, 2, 0,
       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
```





{:.input_area}
```python
mb7.adcm
```





{:.output_data_text}
```
727.3200000000002
```



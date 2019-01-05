---
redirect_from:
  - "/model/spint/odw-example"
interact_link: content/model/spint/ODW_example.ipynb
title: 'ODW_example'
prev_page:
  url: /model/spint/sparse_categorical_speed
  title: 'sparse_categorical_speed'
next_page:
  url: /model/spint/autograd_test
  title: 'autograd_test'
comment: "***PROGRAMMATICALLY GENERATED, DO NOT EDIT. SEE ORIGINAL FILES IN /content***"
---



{:.input_area}
```python
import sys
sys.path.append('/Users/toshan/dev/pysal/pysal/weights')
from spintW import ODW
import pysal as ps
```


# With an equal number of origins and destinations (n=16)



{:.input_area}
```python
origins = ps.weights.lat2W(4,4)
dests = ps.weights.lat2W(4,4)
```




{:.input_area}
```python
origins.n
```





{:.output_data_text}
```
16
```





{:.input_area}
```python
dests.n
```





{:.output_data_text}
```
16
```





{:.input_area}
```python
ODw = ODW(origins, dests)
```




{:.input_area}
```python
print ODw.n, 16*16
```


{:.output_stream}
```
256 256

```



{:.input_area}
```python
ODw.full()[0].shape
```





{:.output_data_text}
```
(256, 256)
```



 # With non-equal number of origins (n=9) and destinations (m=25)



{:.input_area}
```python
origins = ps.weights.lat2W(3,3)
```




{:.input_area}
```python
dests = ps.weights.lat2W(5,5)
```




{:.input_area}
```python
origins.n
```





{:.output_data_text}
```
9
```





{:.input_area}
```python
dests.n
```





{:.output_data_text}
```
25
```





{:.input_area}
```python
ODw = ODW(origins, dests)
```




{:.input_area}
```python
print ODw.n, 9*25
```


{:.output_stream}
```
225 225

```



{:.input_area}
```python
ODw.full()[0].shape
```





{:.output_data_text}
```
(225, 225)
```



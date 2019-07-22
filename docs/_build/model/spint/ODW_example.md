---
redirect_from:
  - "/model/spint/odw-example"
interact_link: content/model/spint/ODW_example.ipynb
kernel_name: Python [Root]
has_widgets: false
title: 'ODW_example'
prev_page:
  url: /model/spint/sparse_categorical_speed
  title: 'sparse_categorical_speed'
next_page:
  url: /model/spint/autograd_test
  title: 'autograd_test'
comment: "***PROGRAMMATICALLY GENERATED, DO NOT EDIT. SEE ORIGINAL FILES IN /content***"
---


<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
import sys
sys.path.append('/Users/toshan/dev/pysal/pysal/weights')
from pysal.model.spintW import ODW
import pysal as ps

```
</div>

</div>



# With an equal number of origins and destinations (n=16)



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
origins = ps.weights.lat2W(4,4)
dests = ps.weights.lat2W(4,4)

```
</div>

</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
origins.n

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
16
```


</div>
</div>
</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
dests.n

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
16
```


</div>
</div>
</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
ODw = ODW(origins, dests)

```
</div>

</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
print ODw.n, 16*16

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">
{:.output_stream}
```
256 256
```
</div>
</div>
</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
ODw.full()[0].shape

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
(256, 256)
```


</div>
</div>
</div>



 # With non-equal number of origins (n=9) and destinations (m=25)



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
origins = ps.weights.lat2W(3,3)

```
</div>

</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
dests = ps.weights.lat2W(5,5)

```
</div>

</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
origins.n

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
9
```


</div>
</div>
</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
dests.n

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
25
```


</div>
</div>
</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
ODw = ODW(origins, dests)

```
</div>

</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
print ODw.n, 9*25

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">
{:.output_stream}
```
225 225
```
</div>
</div>
</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
ODw.full()[0].shape

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
(225, 225)
```


</div>
</div>
</div>


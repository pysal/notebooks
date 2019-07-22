---
redirect_from:
  - "/model/mgwr/gwr-prediction-example"
interact_link: content/model/mgwr/GWR_prediction_example.ipynb
kernel_name: python3
has_widgets: false
title: 'GWR_prediction_example'
prev_page:
  url: /model/mgwr/GWR_Georgia_example
  title: 'GWR_Georgia_example'
next_page:
  url: /model/mgwr/GWR_MGWR_example
  title: 'GWR_MGWR_example'
comment: "***PROGRAMMATICALLY GENERATED, DO NOT EDIT. SEE ORIGINAL FILES IN /content***"
---


<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
import numpy as np
import pysal.lib as ps
from pysal.model.mgwr.gwr import GWR, MGWR
from pysal.model.mgwr.sel_bw import Sel_BW
import geopandas as gp
import matplotlib.pyplot as plt
import matplotlib as mpl

```
</div>

</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
#Load Georgia dataset and generate plot of Georgia counties (figure 1)
georgia = gp.read_file(ps.examples.get_path('G_utm.shp'))
fig, ax = plt.subplots(figsize=(10,10))
georgia.plot(ax=ax, **{'edgecolor':'black', 'facecolor':'white'})
georgia.centroid.plot(ax=ax, c='black')

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
<matplotlib.axes._subplots.AxesSubplot at 0x1a2028dcc0>
```


</div>
</div>
<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">

{:.output_png}
![png](../../images/model/mgwr/GWR_prediction_example_1_1.png)

</div>
</div>
</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
#Prepare Georgia dataset inputs
y = georgia['PctBach'].values.reshape((-1,1))
X = georgia[['PctFB', 'PctBlack', 'PctRural']].values
u = georgia['X']
v = georgia['Y']
coords = np.array(list(zip(u,v)))

np.random.seed(908)
sample = np.random.choice(range(159), 10)
mask = np.ones_like(y,dtype=bool).flatten()
mask[sample] = False

cal_coords = coords[mask]
cal_y = y[mask]
cal_X = X[mask]

pred_coords = coords[~mask]
pred_y = y[~mask]
pred_X = X[~mask]

```
</div>

</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
#Calibrate GWR model

gwr_selector = Sel_BW(cal_coords, cal_y, cal_X)
gwr_bw = gwr_selector.search(bw_min=2)
print(gwr_bw)
model = GWR(cal_coords, cal_y, cal_X, gwr_bw)
gwr_results = model.fit()

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">
{:.output_stream}
```
109.0
```
</div>
</div>
</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
scale = gwr_results.scale
residuals = gwr_results.resid_response

pred_results = model.predict(pred_coords, pred_X, scale, residuals)

```
</div>

</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
pred_results.predictions

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
array([[12.17204646],
       [17.23453734],
       [10.77131683],
       [13.70057966],
       [ 4.29466558],
       [ 9.54432956],
       [ 7.57597975],
       [20.24941349],
       [10.82796502],
       [ 7.10512614]])
```


</div>
</div>
</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
pred_y

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
array([[ 9.2],
       [18.6],
       [ 9.4],
       [13.7],
       [ 6.8],
       [ 7.7],
       [ 4.6],
       [16.6],
       [ 9.5],
       [ 5.6]])
```


</div>
</div>
</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
np.corrcoef(pred_results.predictions.flatten(), pred_y.flatten())[0][1]

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
0.9142492684278577
```


</div>
</div>
</div>


---
redirect_from:
  - "/model/spint/new-distanceband"
interact_link: content/model/spint/New_DistanceBand.ipynb
kernel_name: Python [Root]
has_widgets: false
title: 'New_DistanceBand'
prev_page:
  url: /model/spint/Example_NYCBikes_AllFeatures
  title: 'Example_NYCBikes_AllFeatures'
next_page:
  url: /model/spint/sparse_scipy_optim
  title: 'sparse_scipy_optim'
comment: "***PROGRAMMATICALLY GENERATED, DO NOT EDIT. SEE ORIGINAL FILES IN /content***"
---


<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
import numpy as np
from scipy.spatial import distance
import scipy.spatial as spatial
from pysal.weights import W
from pysal.weights.util import isKDTree
from pysal.weights import Distance as Distance
from pysal.weights import WSP, WSP2W
from scipy.spatial import distance_matrix
import scipy.sparse as sp
from pysal.common import KDTree

```
</div>

</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
class DistanceBand(W):
    """
    Spatial weights based on distance band.

    Parameters
    ----------

    data        : array
                  (n,k) or KDTree where KDtree.data is array (n,k)
                  n observations on k characteristics used to measure
                  distances between the n objects
    threshold  : float
                 distance band
    p          : float
                 Minkowski p-norm distance metric parameter:
                 1<=p<=infinity
                 2: Euclidean distance
                 1: Manhattan distance
    binary     : boolean
                 If true w_{ij}=1 if d_{i,j}<=threshold, otherwise w_{i,j}=0
                 If false wij=dij^{alpha}
    alpha      : float
                 distance decay parameter for weight (default -1.0)
                 if alpha is positive the weights will not decline with
                 distance. If binary is True, alpha is ignored

    ids         : list
                  values to use for keys of the neighbors and weights dicts

    Attributes
    ----------
    weights : dict
              of neighbor weights keyed by observation id

    neighbors : dict
                of neighbors keyed by observation id



    """

    def __init__(self, data, threshold, p=2, alpha=-1.0, binary=True, ids=None, build_sp=True):
        """Casting to floats is a work around for a bug in scipy.spatial.
        See detail in pysal issue #126.

        """
        self.p = p
        self.threshold = threshold
        self.binary = binary
        self.alpha = alpha
        self.build_sp = build_sp
        
        if isKDTree(data):
            self.kd = data
            self.data = self.kd.data
        else:
            if self.build_sp:
                try:
                    data = np.asarray(data)
                    if data.dtype.kind != 'f':
                        data = data.astype(float)
                        self.data = data
                        self.kd = KDTree(self.data)
                except:
                    raise ValueError("Could not make array from data")        
            else:
                self.data = data
                self.kd = None       
               

        self._band()
        neighbors, weights = self._distance_to_W(ids)
        W.__init__(self, neighbors, weights, ids)

    def _band(self):
        """Find all pairs within threshold.

        """
        if self.build_sp:    
            self.dmat = self.kd.sparse_distance_matrix(
                    self.kd, max_distance=self.threshold)
        else:
            self.dmat = self._spdistance_matrix(self.data, self.data, self.threshold)
    
    def _distance_to_W(self, ids=None):
        if self.binary:
            self.dmat[self.dmat>0] = 1
            tempW = WSP2W(WSP(self.dmat))
            return tempW.neighbors, tempW.weights

        else:
            weighted = self.dmat.power(self.alpha)
            weighted[weighted==np.inf] = 0
            tempW = WSP2W(WSP(weighted))
            return tempW.neighbors, tempW.weights
          
    def _spdistance_matrix(self, x,y, threshold=None):
        dist = distance_matrix(x,y)
        if threshold is not None:
            zeros = dist > threshold
            dist[zeros] = 0
        return sp.csr_matrix(dist)

```
</div>

</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
x = np.random.randint(0, 1000, 1000)
y = np.random.randint(0, 1000, 1000)
w = np.random.randint(0, 1000, 1000)
z = np.random.randint(0, 1000, 1000)

data = zip(x.ravel(), y.ravel(), w.ravel(), z.ravel())
tree = KDTree(data)

```
</div>

</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
#print np.allclose(Distance.DistanceBand(tree, threshold=500, alpha=-1.5, binary=True).full()[0], DistanceBand(tree, threshold=500, alpha=-1.5, binary=True).full()[0])
#print np.allclose(Distance.DistanceBand(tree, threshold=500, alpha=-1.5, binary=False).full()[0], DistanceBand(tree, threshold=500, alpha=-1.5, binary=False).full()[0])

```
</div>

</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
%time Distance.DistanceBand(tree, threshold=500, alpha=-1.5, binary=True)
%time DistanceBand(tree, threshold=500, alpha=-1.5, binary=True, build_sp=True)


```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">
{:.output_stream}
```
CPU times: user 1.42 s, sys: 17.9 ms, total: 1.44 s
Wall time: 1.44 s
CPU times: user 366 ms, sys: 11.3 ms, total: 377 ms
Wall time: 376 ms
```
</div>
</div>
<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
<__main__.DistanceBand at 0x10c0aedd0>
```


</div>
</div>
</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
%time Distance.DistanceBand(tree, threshold=500, alpha=-1.5, binary=True)
%time DistanceBand(tree, threshold=500, alpha=-1.5, binary=True, build_sp=False)

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">
{:.output_stream}
```
CPU times: user 1.37 s, sys: 21.7 ms, total: 1.39 s
Wall time: 1.4 s
CPU times: user 69.9 ms, sys: 4.84 ms, total: 74.7 ms
Wall time: 74.7 ms
```
</div>
</div>
<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
<__main__.DistanceBand at 0x117d18c90>
```


</div>
</div>
</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
%time Distance.DistanceBand(tree, threshold=500, alpha=-1.5, binary=False)
%time DistanceBand(tree, threshold=500, alpha=-1.5, binary=False, build_sp=True)

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">
{:.output_stream}
```
CPU times: user 1.28 s, sys: 44 ms, total: 1.32 s
Wall time: 1.3 s
CPU times: user 199 ms, sys: 10.9 ms, total: 210 ms
Wall time: 210 ms
```
</div>
</div>
<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
<__main__.DistanceBand at 0x117d18a10>
```


</div>
</div>
</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
%time Distance.DistanceBand(tree, threshold=500, alpha=-1.5, binary=False)
%time DistanceBand(tree, threshold=500, alpha=-1.5, binary=False, build_sp=False)

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">
{:.output_stream}
```
CPU times: user 1.5 s, sys: 46.3 ms, total: 1.54 s
Wall time: 1.53 s
CPU times: user 67.1 ms, sys: 5.1 ms, total: 72.2 ms
Wall time: 72.2 ms
```
</div>
</div>
<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
<__main__.DistanceBand at 0x117d18e90>
```


</div>
</div>
</div>


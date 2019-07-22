---
redirect_from:
  - "/model/spint/4d-distance"
interact_link: content/model/spint/4d_distance.ipynb
kernel_name: Python [Root]
has_widgets: false
title: '4d_distance'
prev_page:
  url: /model/spint/NYC_Bike_Example
  title: 'NYC_Bike_Example'
next_page:
  url: /model/spglm/intro
  title: 'spglm'
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

```
</div>

</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
def nplinalg():
    np.linalg.norm(np.array((67, 46, 92, 67))-np.array((44, 97, 25, 50)))
    np.linalg.norm(np.array((67, 46, 92, 67))-np.array((84, 37, 66, 53)))
    np.linalg.norm(np.array((67, 46, 92, 67))-np.array((30, 46, 23, 80)))
    
    np.linalg.norm(np.array((44, 97, 25, 50))-np.array((67, 46, 92, 67)))
    np.linalg.norm(np.array((44, 97, 25, 50))-np.array((84, 37, 66, 53)))
    np.linalg.norm(np.array((44, 97, 25, 50))-np.array((30, 46, 23, 80)))
    
    np.linalg.norm(np.array((84, 37, 66, 53))-np.array((44, 97, 25, 50)))
    np.linalg.norm(np.array((84, 37, 66, 53))-np.array((30, 46, 23, 80)))
    np.linalg.norm(np.array((84, 37, 66, 53))-np.array((67, 46, 92, 67)))
    
    np.linalg.norm(np.array((30, 46, 23, 80))-np.array((67, 46, 92, 67)))
    np.linalg.norm(np.array((30, 46, 23, 80))-np.array((44, 97, 25, 50)))
    np.linalg.norm(np.array((30, 46, 23, 80))-np.array((30, 46, 23, 80)))
    
def eucdist():
    distance.euclidean(np.array((67, 46, 92, 67)),np.array((44, 97, 25, 50)))
    distance.euclidean(np.array((67, 46, 92, 67)),np.array((84, 37, 66, 53)))
    distance.euclidean(np.array((67, 46, 92, 67)),np.array((30, 46, 23, 80)))
    
    distance.euclidean(np.array((44, 97, 25, 50)),np.array((67, 46, 92, 67)))
    distance.euclidean(np.array((44, 97, 25, 50)),np.array((84, 37, 66, 53)))
    distance.euclidean(np.array((44, 97, 25, 50)),np.array((30, 46, 23, 80)))
    
    distance.euclidean(np.array((84, 37, 66, 53)),np.array((44, 97, 25, 50)))
    distance.euclidean(np.array((84, 37, 66, 53)),np.array((30, 46, 23, 80)))
    distance.euclidean(np.array((84, 37, 66, 53)),np.array((67, 46, 92, 67)))
    
    distance.euclidean(np.array((30, 46, 23, 80)),np.array((67, 46, 92, 67)))
    distance.euclidean(np.array((30, 46, 23, 80)),np.array((44, 97, 25, 50)))
    distance.euclidean(np.array((30, 46, 23, 80)),np.array((30, 46, 23, 80)))
    
def distpython():
    dist(np.array((67, 46, 92, 67)),np.array((44, 97, 25, 50)))
    dist(np.array((67, 46, 92, 67)),np.array((84, 37, 66, 53)))
    dist(np.array((67, 46, 92, 67)),np.array((30, 46, 23, 80)))
    
    dist(np.array((44, 97, 25, 50)),np.array((67, 46, 92, 67)))
    dist(np.array((44, 97, 25, 50)),np.array((84, 37, 66, 53)))
    dist(np.array((44, 97, 25, 50)),np.array((30, 46, 23, 80)))
    
    dist(np.array((84, 37, 66, 53)),np.array((44, 97, 25, 50)))
    dist(np.array((84, 37, 66, 53)),np.array((30, 46, 23, 80)))
    dist(np.array((84, 37, 66, 53)),np.array((67, 46, 92, 67)))
    
    dist(np.array((30, 46, 23, 80)),np.array((67, 46, 92, 67)))
    dist(np.array((30, 46, 23, 80)),np.array((44, 97, 25, 50)))
    dist(np.array((30, 46, 23, 80)),np.array((30, 46, 23, 80)))

def scpkdtree():
    data = zip(x.ravel(), y.ravel(), w.ravel(), z.ravel())
    tree = spatial.KDTree(data)
    W = pysal.weights.DistanceBand(tree, threshold=9999, alpha=-1.5, binary=False)


```
</div>

</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
%timeit nplinalg()
%timeit distpython()
%timeit scpkdtree()

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">
{:.output_stream}
```
The slowest run took 144.28 times longer than the fastest. This could mean that an intermediate result is being cached.
10000 loops, best of 3: 86.8 µs per loop
The slowest run took 17.86 times longer than the fastest. This could mean that an intermediate result is being cached.
10000 loops, best of 3: 82.1 µs per loop
The slowest run took 5.82 times longer than the fastest. This could mean that an intermediate result is being cached.
1 loop, best of 3: 40min 50s per loop
```
</div>
</div>
</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
x = np.random.randint(1,1000, 3000)
y = np.random.randint(1,1000, 3000)
w = np.random.randint(1,1000, 3000)
z = np.random.randint(1,1000, 3000)

data = zip(x.ravel(), y.ravel(), w.ravel(), z.ravel())
tree = spatial.KDTree(data)
W = pysal.weights.DistanceBand(tree, threshold=9999, alpha=-1.5, binary=False)

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">
{:.output_traceback_line}
```

    ---------------------------------------------------------------------------

    KeyboardInterrupt                         Traceback (most recent call last)

    <ipython-input-371-25b6bf1123d8> in <module>()
          6 data = zip(x.ravel(), y.ravel(), w.ravel(), z.ravel())
          7 tree = spatial.KDTree(data)
    ----> 8 W = pysal.weights.DistanceBand(tree, threshold=9999, alpha=-1.5, binary=False)
    

    //anaconda/lib/python2.7/site-packages/pysal/weights/Distance.pyc in __init__(self, data, threshold, p, alpha, binary, ids)
        472         self.alpha = alpha
        473         self._band()
    --> 474         neighbors, weights = self._distance_to_W(ids)
        475         W.__init__(self, neighbors, weights, ids)
        476 


    //anaconda/lib/python2.7/site-packages/pysal/weights/Distance.pyc in _distance_to_W(self, ids)
        504                 i,j = key
        505                 if i != j:
    --> 506                     if j not in neighbors[i]:
        507                         weights[i].append(weight**self.alpha)
        508                         neighbors[i].append(j)


    KeyboardInterrupt: 


```
</div>
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

    def __init__(self, data, threshold=None, p=2, alpha=-1.0, binary=True, ids=None):
        """Casting to floats is a work around for a bug in scipy.spatial.
        See detail in pysal issue #126.

        """
        if isKDTree(data):
            self.kd = data
            self.data = self.kd.data
        else:
            try:
                data = np.asarray(data)
                if data.dtype.kind != 'f':
                    data = data.astype(float)
                self.data = data
                self.kd = KDTree(self.data)
            except:
                raise ValueError("Could not make array from data")

        self.p = p
        self.threshold = threshold
        self.binary = binary
        self.alpha = alpha
        self._band()
        neighbors, weights = self._distance_to_W(ids)
        W.__init__(self, neighbors, weights, ids)

    def _band(self):
        """Find all pairs within threshold.

        """
        if self.threshold is not None:
            self.dmat = self.kd.sparse_distance_matrix(
                    self.kd, max_distance=self.threshold)
        else:
            self.dmat = np.array(distance_matrix(self.data, self.data))

    def _distance_to_W(self, ids=None):
        if ids:
            ids = np.array(ids)
        else:
            ids = np.arange(self.dmat.shape[0])
        neighbors = dict([(i,[]) for i in ids])
        weights = dict([(i,[]) for i in ids])
        if self.binary:
            for key,weight in self.dmat.items():
                i,j = key
                if i != j:
                    if j not in neighbors[i]:
                        weights[i].append(1)
                        neighbors[i].append(j)
                    if i not in neighbors[j]:
                        weights[j].append(1)
                        neighbors[j].append(i)

        else:
            weighted = np.array(map(lambda x: pow(x, -1.5), self.dmat))
            print weighted.shape
            rows, cols =self.dmat.shape
            for i in range(rows):
                for j in range(cols):
                    if i != j:
                        if j not in neighbors[i]:
                            weights[i].append(weighted[i,j])
                            neighbors[i].append(j)
                        if i not in neighbors[j]:
                            weights[j].append(weighted[i,j])
                            neighbors[j].append(i)

        return neighbors, weights


```
</div>

</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
x = np.random.randint(1,1000, 500)
y = np.random.randint(1,1000, 500)
w = np.random.randint(1,1000, 500)
z = np.random.randint(1,1000, 500)

data = zip(x.ravel(), y.ravel(), w.ravel(), z.ravel())
tree = spatial.KDTree(data)


```
</div>

</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
%timeit DistanceBand(tree, threshold=9999, alpha=-1.5, binary=False)

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">
{:.output_stream}
```
1 loop, best of 3: 7.73 s per loop
```
</div>
</div>
</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
%prun DistanceBand(tree, threshold=9999, alpha=-1.5, binary=False)

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">
{:.output_stream}
```
 ```
</div>
</div>
</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
weight = DistanceBand(tree, threshold=9999, alpha=-1.5, binary=False)

```
</div>

</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
pairs = weight.dmat.keys()

```
</div>

</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
from scipy.spatial import distance_matrix

```
</div>

</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
one = np.hstack([x.reshape((-1,1)),y.reshape((-1,1))])
two = np.hstack([w.reshape((-1,1)),z.reshape((-1,1))])
test = np.hstack([x.reshape((-1,1)),y.reshape((-1,1)), w.reshape((-1,1)),z.reshape((-1,1))])

```
</div>

</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
mat = distance_matrix(data, data)
mat = np.array(mat)
mat.shape

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
(500, 500)
```


</div>
</div>
</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
%time DistanceBand(tree, alpha=-1.5, binary=False)

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">
{:.output_stream}
```
(500, 500)
CPU times: user 1.82 s, sys: 87 ms, total: 1.91 s
Wall time: 1.85 s
```
</div>
</div>
<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
<__main__.DistanceBand at 0x123f3c450>
```


</div>
</div>
</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
%time Distance.DistanceBand(tree, threshold=9999999, alpha=-1.5, binary=False)

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">
{:.output_stream}
```
CPU times: user 8.43 s, sys: 92.3 ms, total: 8.52 s
Wall time: 8.5 s
```
</div>
</div>
<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
<pysal.weights.Distance.DistanceBand at 0x123f38250>
```


</div>
</div>
</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
W_new = DistanceBand(tree, alpha=-1.5, binary=False)

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">
{:.output_stream}
```
(500, 500)
```
</div>
</div>
</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
W_old = Distance.DistanceBand(tree, threshold=9999999, alpha=-1.5, binary=False)

```
</div>

</div>



<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
np.allclose(W_new.full()[0], W_old.full()[0])

```
</div>

<div class="output_wrapper" markdown="1">
<div class="output_subarea" markdown="1">


{:.output_data_text}
```
True
```


</div>
</div>
</div>


---
redirect_from:
  - "/model/spint/sparse-categorical-speed"
interact_link: content/model/spint/sparse_categorical_speed.ipynb
title: 'sparse_categorical_speed'
prev_page:
  url: /model/spint/sparse_categorical_bottleneck
  title: 'sparse_categorical_bottleneck'
next_page:
  url: /model/spint/sparse_grav
  title: 'sparse_grav'
comment: "***PROGRAMMATICALLY GENERATED, DO NOT EDIT. SEE ORIGINAL FILES IN /content***"
---



{:.input_area}
```python
import numpy as np
import pysal
import scipy.sparse as sp
import itertools as iter
from scipy.stats import f, chisqprob
import numpy.linalg as la
import pandas as pd
from datetime import datetime as dt
import matplotlib.pyplot as plt
%pylab inline
```


{:.output_stream}
```
Populating the interactive namespace from numpy and matplotlib

```



{:.input_area}
```python
#OLD
"""
def spcategorical2(n_cat_ids):
    '''
    Returns a dummy matrix given an array of categorical variables.
    Parameters
    ----------
    n_cat_ids    : array
                   A 1d vector of the categorical labels for n observations.

    Returns
    --------
    dummy        : array
                   A sparse matrix of dummy (indicator/binary) variables for the
                   categorical data.  

    '''
    if np.squeeze(n_cat_ids).ndim == 1:
        cat_set = np.unique(n_cat_ids)
        n = len(n_cat_ids)
        C = len(cat_set)
        row_map = dict((id, np.where(cat_set == id)[0]) for id in n_cat_ids)
        indices = np.array([row_map[row] for row in n_cat_ids]).flatten()
        indptr = np.zeros((n + 1, ), dtype=int)
        indptr[:-1] = list(np.arange(n))
        indptr[-1] = n 
        return sp.csr_matrix((np.ones(n), indices, indptr))
    else:
        raise IndexError("The index %s is not understood" % col)
"""
def spcategorical2(n_cat_ids):
    '''
    Returns a dummy matrix given an array of categorical variables.
    Parameters
    ----------
    n_cat_ids    : array
                   A 1d vector of the categorical labels for n observations.

    Returns
    --------
    dummy        : array
                   A sparse matrix of dummy (indicator/binary) variables for the
                   categorical data.  

    '''
    if np.squeeze(n_cat_ids).ndim == 1:
        cat_set = np.unique(n_cat_ids)
        n = len(n_cat_ids)
        C = len(cat_set)
        indices = n_cat_ids
        indptr = np.arange(n+1, dtype=int) 
        return sp.csr_matrix((np.ones(n), indices, indptr))
    else:
        raise IndexError("The index %s is not understood" % col)
```




{:.input_area}
```python
def spcategorical1(data):
    '''
    Returns a dummy matrix given an array of categorical variables.
    Parameters
    ----------
    data : array
        A 1d vector of the categorical variable.

    Returns
    --------
    dummy_matrix
        A sparse matrix of dummy (indicator/binary) variables for the
        categorical data.  

    '''
    if np.squeeze(data).ndim == 1:
        tmp_arr = np.unique(data)
        tmp_dummy = sp.csr_matrix((0, len(data)))
        for each in tmp_arr[:, None]:
            row = sp.csr_matrix((each == data).astype(float))
            tmp_dummy = sp.vstack([tmp_dummy, row])
        tmp_dummy = tmp_dummy.T
        return tmp_dummy
    else:
        raise IndexError("The index %s is not understood" % col)


```




{:.input_area}
```python
def spcategorical1a(data):
    '''
    Returns a dummy matrix given an array of categorical variables.
    Parameters
    ----------
    data : array
        A 1d vector of the categorical variable.

    Returns
    --------
    dummy_matrix
        A sparse matrix of dummy (indicator/binary) variables for the
        categorical data.  

    '''
    if np.squeeze(data).ndim == 1:
        tmp_arr = np.unique(data)
        n = len(data)
        C = len(tmp_arr)
        tmp_dummy = sp.dok_matrix((n, C))
        for each in tmp_arr[:, None]:
            row = (each == data).astype(float)
            tmp_dummy[:,each[0]] = row.reshape((n,1))
        return tmp_dummy.tocsr()
    else:
        raise IndexError("The index %s is not understood" % col)




```




{:.input_area}
```python
def spcategorical1b(data):
    '''
    Returns a dummy matrix given an array of categorical variables.
    Parameters
    ----------
    data : array
        A 1d vector of the categorical variable.

    Returns
    --------
    dummy_matrix
        A sparse matrix of dummy (indicator/binary) variables for the
        categorical data.  

    '''
    if np.squeeze(data).ndim == 1:
        tmp_arr = np.unique(data)
        n = len(data)
        C = len(tmp_arr)
        tmp_dummy = sp.lil_matrix((n, C))
        for each in tmp_arr[:, None]:
            row = (each == data).astype(float)
            tmp_dummy[:,each[0]] = row.reshape((n,1))
        return tmp_dummy.tocsr()
    else:
        raise IndexError("The index %s is not understood" % col)

```




{:.input_area}
```python
n = 20
o = np.tile(np.arange(n),n)
print np.allclose(spcategorical1(o).toarray(), spcategorical2(o).toarray())
print np.allclose(spcategorical1(o).toarray(), spcategorical1a(o).toarray())
print np.allclose(spcategorical1(o).toarray(), spcategorical1b(o).toarray())
```


{:.output_stream}
```
True
True
True

```



{:.input_area}
```python
spcat1 = []
for n in np.arange(25,250,25):
    o = np.tile(np.arange(n),n)
    s = dt.now()
    a = spcategorical1(np.array(o))
    e = dt.now()
    spcat1.append((e-s).total_seconds())
```




{:.input_area}
```python
spcat1a = []
for n in np.arange(25,250,25):
    o = np.tile(np.arange(n),n)
    s = dt.now()
    b = spcategorical1a(np.array(o))
    e = dt.now()
    spcat1a.append((e-s).total_seconds())
```




{:.input_area}
```python
spcat1b = []
for n in np.arange(25,250,25):
    o = np.tile(np.arange(n),n)
    s = dt.now()
    b = spcategorical1b(np.array(o))
    e = dt.now()
    spcat1b.append((e-s).total_seconds())
```




{:.input_area}
```python
spcat2 = []
for n in np.arange(25,250,25):
    o = np.tile(np.arange(n),n)
    s = dt.now()
    b = spcategorical2(np.array(o))
    e = dt.now()
    spcat2.append((e-s).total_seconds())
```




{:.input_area}
```python
spcat1
```




{:.input_area}
```python
spcat1a
```




{:.input_area}
```python
spcat1b
```




{:.input_area}
```python
spcat2
```




{:.input_area}
```python
x = np.arange(25, 250, 25)
plt.plot(x, spcat1, x, spcat1a, x, spcat1b, x, spcat2)
plt.legend(('spcat1', 'spcat1a', 'spcat1b', 'spcat2'))
plt.title('Speed of Sparse Dummy Functions')
plt.xlabel('Sample Size')
plt.ylabel('Seconds')
```


###### It is obvious that spcat1 and spcat2 are the fastest functions for creating sparse dummies. The differnece between these two functions is that spcat1 creates the dummies row by row (in sparse format) and then stacks the rows using sparse.hstack() while spcat2 builds an index for the non-zero dummy variable entries and then uses this index to instanitate the entire sparse dummy matrix, somewhat simularly to how the regimes are built in pysal. The slower functions spcat1a and spcat1b are riffs on spcat1 in that they also work row by row but they first instantiate an empty sparse matrix (either lil or dok) and then assign the rows to the empty matrix. The scipy doucmentation suggests that assignment for these two types of sparce matrices is faster than csr and csc and therefore is better for incrementally building a sparse matrix. However, it appears that avoiding assignment alother may be the best route if building a sparse matrix row by row. Therefrow csr is the best sparse data structure for row by row contruction in this context. Now lets lets row by row building (spcat1) vs entire instantiation using an non-zero-value index (spcat2) when the number of dummy variables starts to become much larger.



{:.input_area}
```python
spcat1 = []
for n in np.arange(100,1000,100):
    o = np.tile(np.arange(n),n)
    s = dt.now()
    b = spcategorical1(np.array(o))
    e = dt.now()
    spcat1.append((e-s).total_seconds())
```




{:.input_area}
```python
spcat2 = []
for n in np.arange(100,1000,100):
    o = np.tile(np.arange(n),n)
    s = dt.now()
    b = spcategorical2(np.array(o))
    e = dt.now()
    spcat2.append((e-s).total_seconds())
```




{:.input_area}
```python
spcat1
```




{:.input_area}
```python
spcat2
```




{:.input_area}
```python
x = np.arange(100, 1000, 100)
plt.plot(x, spcat1, x, spcat2)
plt.legend(('spcat1', 'spcat2'))
plt.title('Speed of Sparse Dummy Functions')
plt.xlabel('Sample Size')
plt.ylabel('Seconds')
```


###### It is clear that the spcat2 function, which uses the non-zero-value index, is more efficient than the row by row method in spcat1. However, from additional testing, it was noticed that spcat2 does use more memory and for larger n (somewhere between 10k and 20k), my notebook ran out of memory. This is likely due to to the fact that the spcat2 function requires an ($n^2$,) array ones ones, an index array of shape ($n^2$,) and an index pointer array of shape ($n^2$,). Combined these must soak up a lot of memory, which makes very large n infeasible. Then the spcat1 function still may be useful in scenarios where there is a very large sample size and no way of accessing more memory. It will be very slow in compairson, but will make analysis feasible where it would otherwise be infeasible. As a reasult,  I will keep both functions as options.



{:.input_area}
```python
def concatenate_csc_matrices_by_columns(matrix1, matrix2):
    new_data = np.concatenate((matrix1.data, matrix2.data))
    new_indices = np.concatenate((matrix1.indices, matrix2.indices))
    new_ind_ptr = matrix2.indptr + len(matrix1.data)
    new_ind_ptr = new_ind_ptr[1:]
    new_ind_ptr = np.concatenate((matrix1.indptr, new_ind_ptr))

    return csc_matrix((new_data, new_indices, new_ind_ptr))

def spcategorical2a(n_cat_ids, unique=None):
    '''
    Returns a dummy matrix given an array of categorical variables.
    Parameters
    ----------
    n_cat_ids    : array
                   A 1d vector of the categorical labels for n observations.

    Returns
    --------
    dummy        : array
                   A sparse matrix of dummy (indicator/binary) variables for the
                   categorical data.  

    '''
    if np.squeeze(n_cat_ids).ndim == 1:
        n = np.size(n_cat_ids)
        indptr = np.arange(n+1, dtype=uint32) 
        return sp.csr_matrix((np.ones(n, dtype=int8), n_cat_ids, indptr))
    else:
        raise IndexError("The index %s is not understood" % col)
```




{:.input_area}
```python
n = 3500
o = np.tile(np.arange(n, dtype=uint16),n)
s = dt.now()
b2 = spcategorical2(o)
e = dt.now()
print e-s
b2
```


{:.output_stream}
```
0:00:00.462530

```




{:.output_data_text}
```
<12250000x3500 sparse matrix of type '<type 'numpy.float64'>'
	with 12250000 stored elements in Compressed Sparse Row format>
```





{:.input_area}
```python
n = 3500
o = np.tile(np.arange(n, dtype=uint16),n)
s = dt.now()
b2a = spcategorical2a(o)
e = dt.now()
print e-s
b2a
```


{:.output_stream}
```
0:00:00.074958

```




{:.output_data_text}
```
<12250000x3500 sparse matrix of type '<type 'numpy.int8'>'
	with 12250000 stored elements in Compressed Sparse Row format>
```



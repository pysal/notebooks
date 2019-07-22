---
redirect_from:
  - "/model/spint/sparse-categorical-bottleneck"
interact_link: content/model/spint/sparse_categorical_bottleneck.ipynb
kernel_name: python2
has_widgets: false
title: 'sparse_categorical_bottleneck'
prev_page:
  url: /model/spint/sparse_grav
  title: 'sparse_grav'
next_page:
  url: /model/spint/OD_weights
  title: 'OD_weights'
comment: "***PROGRAMMATICALLY GENERATED, DO NOT EDIT. SEE ORIGINAL FILES IN /content***"
---


<div markdown="1" class="cell code_cell">
<div class="input_area" markdown="1">
```python
from scipy import sparse as sp
import numpy as np

def spcategorical(n_cat_ids):
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
        index = [np.where(cat_set == id)[0].tolist()[0] for id in n_cat_ids] #This list comprehension is likely 
        print index                                                                    #the most intense part of the algorithm
        indptr = np.arange(n+1, dtype=int) 
        return sp.csr_matrix((np.ones(n), index, indptr))
    else:
        raise IndexError("The index %s is not understood" % col)

#If the variable, n_cat_ids, is already composed of integers and the integers are the n x 1 vector of
#origins or destinations in OD pairs for which w ewant to build fixed effects then there is no need to 
#create the index variable, which probably takes the most time within this function. Instead n_cat_ids can
#passed directly to the csr matrix constructor and some speed-ups can be achieved. In the case where the
#origin/destination ids are not integers but are strings a speed-up may be possible by alterign the algorithm
#so that the index is build in chunks (say each origin/destination) rather than for each row of of the n x 1
#n_cat_ids array as is done in creating the index variable.

```
</div>

</div>


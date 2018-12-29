---
redirect_from:
  - "/model/spint/od-weights"
interact_link: content/model/spint/OD_weights.ipynb
title: 'OD_weights'
prev_page:
  url: /model/spint/ODW_example
  title: 'ODW_example'
next_page:
  url: /model/spint/sparse_categorical
  title: 'sparse_categorical'
comment: "***PROGRAMMATICALLY GENERATED, DO NOT EDIT. SEE ORIGINAL FILES IN /content***"
---



{:.input_area}
```python
import pysal as ps
from pysal import weights as w
import numpy as np
import scipy.sparse as sp
```




{:.input_area}
```python

def OD(Wo, Wd):
    Wo = Wo.sparse
    Wd = Wd.sparse
    Ww = sp.kron(Wo, Wd)
    return w.WSP2W(w.WSP(Ww))
```




{:.input_area}
```python
origins = ps.weights.lat2W(4,4)
dests = ps.weights.lat2W(4,4)
Ww = OD(origins, dests)
Ww.transform = 'r'
print Ww.full()[0].shape
```


{:.output_stream}
```
(256, 256)

```



{:.input_area}
```python
flows = np.random.randint(0,100, (4,4))
np.fill_diagonal(flows, 0)
flows = flows.reshape((16,1))
print flows
slag = ps.lag_spatial(Ww, flows)
print slag
```


{:.output_stream}
```
[[ 0]
 [38]
 [36]
 [86]
 [30]
 [ 0]
 [69]
 [19]
 [84]
 [43]
 [ 0]
 [80]
 [58]
 [ 3]
 [35]
 [ 0]]
[[ 28.  ]
 [ 53.25]
 [ 53.25]
 [ 28.  ]
 [ 28.  ]
 [ 36.  ]
 [ 36.  ]
 [ 28.  ]
 [ 28.  ]
 [ 36.  ]
 [ 36.  ]
 [ 28.  ]
 [ 28.  ]
 [ 53.25]
 [ 53.25]
 [ 28.  ]]

```



{:.input_area}
```python
origins.weights
```





{:.output_data_text}
```
{0: [1.0, 1.0], 1: [1.0, 1.0], 2: [1.0, 1.0], 3: [1.0, 1.0]}
```





{:.input_area}
```python
import os
os.chdir('/Users/toshan/dev/pysal/pysal/weights')
from spintW import ODW
```




{:.input_area}
```python
origins = ps.weights.lat2W(2,2)
dests = ps.weights.lat2W(2,2)
Ww = ODW(origins, dests)
```




{:.input_area}
```python
Ww.full()[0]
```





{:.output_data_text}
```
array([[ 0.  ,  0.  ,  0.  ,  0.  ,  0.  ,  0.25,  0.25,  0.  ,  0.  ,
         0.25,  0.25,  0.  ,  0.  ,  0.  ,  0.  ,  0.  ],
       [ 0.  ,  0.  ,  0.  ,  0.  ,  0.25,  0.  ,  0.  ,  0.25,  0.25,
         0.  ,  0.  ,  0.25,  0.  ,  0.  ,  0.  ,  0.  ],
       [ 0.  ,  0.  ,  0.  ,  0.  ,  0.25,  0.  ,  0.  ,  0.25,  0.25,
         0.  ,  0.  ,  0.25,  0.  ,  0.  ,  0.  ,  0.  ],
       [ 0.  ,  0.  ,  0.  ,  0.  ,  0.  ,  0.25,  0.25,  0.  ,  0.  ,
         0.25,  0.25,  0.  ,  0.  ,  0.  ,  0.  ,  0.  ],
       [ 0.  ,  0.25,  0.25,  0.  ,  0.  ,  0.  ,  0.  ,  0.  ,  0.  ,
         0.  ,  0.  ,  0.  ,  0.  ,  0.25,  0.25,  0.  ],
       [ 0.25,  0.  ,  0.  ,  0.25,  0.  ,  0.  ,  0.  ,  0.  ,  0.  ,
         0.  ,  0.  ,  0.  ,  0.25,  0.  ,  0.  ,  0.25],
       [ 0.25,  0.  ,  0.  ,  0.25,  0.  ,  0.  ,  0.  ,  0.  ,  0.  ,
         0.  ,  0.  ,  0.  ,  0.25,  0.  ,  0.  ,  0.25],
       [ 0.  ,  0.25,  0.25,  0.  ,  0.  ,  0.  ,  0.  ,  0.  ,  0.  ,
         0.  ,  0.  ,  0.  ,  0.  ,  0.25,  0.25,  0.  ],
       [ 0.  ,  0.25,  0.25,  0.  ,  0.  ,  0.  ,  0.  ,  0.  ,  0.  ,
         0.  ,  0.  ,  0.  ,  0.  ,  0.25,  0.25,  0.  ],
       [ 0.25,  0.  ,  0.  ,  0.25,  0.  ,  0.  ,  0.  ,  0.  ,  0.  ,
         0.  ,  0.  ,  0.  ,  0.25,  0.  ,  0.  ,  0.25],
       [ 0.25,  0.  ,  0.  ,  0.25,  0.  ,  0.  ,  0.  ,  0.  ,  0.  ,
         0.  ,  0.  ,  0.  ,  0.25,  0.  ,  0.  ,  0.25],
       [ 0.  ,  0.25,  0.25,  0.  ,  0.  ,  0.  ,  0.  ,  0.  ,  0.  ,
         0.  ,  0.  ,  0.  ,  0.  ,  0.25,  0.25,  0.  ],
       [ 0.  ,  0.  ,  0.  ,  0.  ,  0.  ,  0.25,  0.25,  0.  ,  0.  ,
         0.25,  0.25,  0.  ,  0.  ,  0.  ,  0.  ,  0.  ],
       [ 0.  ,  0.  ,  0.  ,  0.  ,  0.25,  0.  ,  0.  ,  0.25,  0.25,
         0.  ,  0.  ,  0.25,  0.  ,  0.  ,  0.  ,  0.  ],
       [ 0.  ,  0.  ,  0.  ,  0.  ,  0.25,  0.  ,  0.  ,  0.25,  0.25,
         0.  ,  0.  ,  0.25,  0.  ,  0.  ,  0.  ,  0.  ],
       [ 0.  ,  0.  ,  0.  ,  0.  ,  0.  ,  0.25,  0.25,  0.  ,  0.  ,
         0.25,  0.25,  0.  ,  0.  ,  0.  ,  0.  ,  0.  ]])
```



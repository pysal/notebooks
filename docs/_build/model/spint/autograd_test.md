---
redirect_from:
  - "/model/spint/autograd-test"
interact_link: content/model/spint/autograd_test.ipynb
title: 'autograd_test'
prev_page:
  url: /model/spint/ODW_example
  title: 'ODW_example'
next_page:
  url: /model/spint/NYC_Bike_Example
  title: 'NYC_Bike_Example'
comment: "***PROGRAMMATICALLY GENERATED, DO NOT EDIT. SEE ORIGINAL FILES IN /content***"
---



{:.input_area}
```python
import pandas as pd
import scipy.optimize as sc
import autograd.numpy as np
import autograd
from autograd.convenience_wrappers import multigrad
import scipy.sparse
```




{:.input_area}
```python
austria = pd.read_csv('http://dl.dropbox.com/u/8649795/AT_Austria.csv')
austria = austria[austria['Origin'] != austria['Destination']]
f = np.reshape(austria['Data'].values, (-1,1))
o = austria['Origin'].values
d = austria['Destination'].values
dij = np.reshape(austria['Dij'].values, (-1,1))
o_vars = np.reshape(austria['Oi2007'].values, (-1,1))
d_vars = np.reshape(austria['Dj2007'].values, (-1,1))
dij = np.reshape(austria['Dij'].values, (-1,1))
o_vars = np.reshape(austria['Oi2007'].values, (-1,1))
d_vars = np.reshape(austria['Dj2007'].values, (-1,1))
```




{:.input_area}
```python
def newton(f, x0):
    # wrap scipy.optimize.newton with our automatic derivatives
    params = sc.fsolve(f, x0)
    return params

def poiss_loglike(mu, sig, ep, x, inputs):
    a,b,c = inputs[:,0], inputs[:,1], inputs[:,2]
    predict = sig*a + ep*b + mu*c
    predict = np.reshape(predict, (-1,1))
    return -np.sum(x*np.log(predict)-predict)

#def loglike(mu, k, x, inputs):
    #return np.sum(poiss_loglike(mu, k, x, inputs))


def fit_maxlike(x, inputs, mu_guess, o_guess, d_guess):
    prime = lambda p: multigrad(poiss_loglike, argnums=[0,1,2])(p[0], p[1], p[2], x, inputs)
    params = newton(prime, (mu_guess, o_guess, d_guess))
    return params
```




{:.input_area}
```python
if __name__ == "__main__":
    
    x=np.log(f)
    inputs = np.hstack((np.log(o_vars), np.log(d_vars), np.log(dij)))
    params = fit_maxlike(x, inputs, mu_guess=0.0, o_guess=1.0, d_guess=1.0)
    print(params)
    
    prime = lambda p: multigrad(poiss_loglike, argnums=[0,1,2])(p[0], p[1], p[2], x, inputs)
    print(prime(params))
```


{:.output_stream}
```
[-1.14993102  0.69084953  0.68523832]
(-2.7430635540781623e-10, -2.5915536383536164e-10, -4.730811298259141e-10)

```

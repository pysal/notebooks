---
redirect_from:
  - "/dynamics/giddy/mobility-measures"
interact_link: content/dynamics/giddy/Mobility_measures.ipynb
title: 'Mobility_measures'
prev_page:
  url: /dynamics/giddy/Rank_Markov
  title: 'Rank_Markov'
next_page:
  url: /dynamics/giddy/Markov_Based_Methods
  title: 'Markov_Based_Methods'
comment: "***PROGRAMMATICALLY GENERATED, DO NOT EDIT. SEE ORIGINAL FILES IN /content***"
---

# Measures of Income Mobility

**Author: Wei Kang <weikang9009@gmail.com>, Serge Rey <sjsrey@gmail.com>**

Income mobility could be viewed as a reranking pheonomenon where regions switch income positions while it could also be considered to be happening as long as regions move away from the previous income levels. The former is named absolute mobility and the latter relative mobility.

This notebook introduces how to estimate income mobility measures from longitudinal income data using methods in **giddy**. Currently, five summary mobility estimators are implemented in **giddy.mobility**. All of them are Markov-based, meaning that they are closely related to the discrete Markov Chains methods introduced in [Markov Based Methods notebook](Markov Based Methods.ipynb). More specifically, each of them is derived from a transition probability matrix $P$. Whether the final estimate is absolute or reletive mobility depends on how the original continuous income data are discretized.

The five Markov-based summary measures of mobility (Formby et al., 2004) are listed below:

| Num| Measures        |      Symbol      | 
|-------------| :-------------: |:-------------:|
|1| $M_P(P) = \frac{m-\sum_{i=1}^m p_{ii}}{m-1} $ | P |
|2| $M_D(P) = 1-|det(P)|$   |D   |   
|3| $M_{L2}(P)=1-|\lambda_2|$| L2| 
|4| $M_{B1}(P) = \frac{m-m \sum_{i=1}^m \pi_i P_{ii}}{m-1} $  |   B1      |   
|5| $M_{B2}(P)=\frac{1}{m-1} \sum_{i=1}^m \sum_{j=1}^m \pi_i P_{ij} |i-j|$| B2| 

$\pi$ is the inital income distribution. For any transition probability matrix with a quasi-maximal diagonal, all of these mobility measures take values on $[0,1]$. $0$ means immobility and $1$ perfect mobility. If the transition probability matrix takes the form of the identity matrix, every region is stuck in its current state implying complete immobility. On the contrary, when each row of $P$ is identical, current state is irrelevant to the probability of moving away to any class. Thus, the transition matrix with identical rows is considered perfect mobile. The larger the mobility estimate, the more mobile the regional income system is. However, it should be noted that these measures try to reveal mobility pattern from different aspects and are thus not comparable to each other. Actually the mean and variance of these measures are different. 

We implemented all the above five summary mobility measures in a single method $markov\_mobility$. A parameter $measure$ could be specified to select which measure to calculate. By default, the mobility measure 'P' will be estimated.

```python
def markov_mobility(p, measure = "P",ini=None)
```



{:.input_area}
```python
from giddy import markov,mobility
mobility.markov_mobility?
```


### US income mobility example
Similar to [Markov Based Methods notebook](Markov Based Methods.ipynb), we will demonstrate the usage of the mobility methods by an application to data on per capita incomes observed annually from 1929 to 2009 for the lower 48 US states.



{:.input_area}
```python
import libpysal
import numpy as np
import mapclassify as mc
```




{:.input_area}
```python
income_path = libpysal.examples.get_path("usjoin.csv")
f = libpysal.io.open(income_path)
pci = np.array([f.by_col[str(y)] for y in range(1929, 2010)]) #each column represents an state's income time series 1929-2010
q5 = np.array([mc.Quantiles(y).yb for y in pci]).transpose() #each row represents an state's income time series 1929-2010
m = markov.Markov(q5)
m.p
```





{:.output_data_text}
```
array([[0.91011236, 0.0886392 , 0.00124844, 0.        , 0.        ],
       [0.09972299, 0.78531856, 0.11080332, 0.00415512, 0.        ],
       [0.        , 0.10125   , 0.78875   , 0.1075    , 0.0025    ],
       [0.        , 0.00417827, 0.11977716, 0.79805014, 0.07799443],
       [0.        , 0.        , 0.00125156, 0.07133917, 0.92740926]])
```



After acquiring the estimate of transition probability matrix, we could call the method $markov\_mobility$ to estimate any of the five Markov-based summary mobility indice. 

### 1. Shorrock1's mobility measure

$$M_{P} = \frac{m-\sum_{i=1}^m P_{ii}}{m-1}$$

```python
measure = "P"```



{:.input_area}
```python
mobility.markov_mobility(m.p, measure="P")
```





{:.output_data_text}
```
0.19758992000997844
```



### 2. Shorroks2's mobility measure

$$M_{D} = 1 - |\det(P)|$$
```python
measure = "D"```



{:.input_area}
```python
mobility.markov_mobility(m.p, measure="D")
```





{:.output_data_text}
```
0.6068485462369559
```



### 3. Sommers and Conlisk's mobility measure
$$M_{L2} = 1  - |\lambda_2|$$

```python
measure = "L2"```



{:.input_area}
```python
mobility.markov_mobility(m.p, measure = "L2")
```





{:.output_data_text}
```
0.03978200230815965
```



### 4. Bartholomew1's mobility measure

$$M_{B1} = \frac{m-m \sum_{i=1}^m \pi_i P_{ii}}{m-1}$$

$\pi$: the inital income distribution

```python
measure = "B1"```



{:.input_area}
```python
pi = np.array([0.1,0.2,0.2,0.4,0.1])
mobility.markov_mobility(m.p, measure = "B1", ini=pi)
```





{:.output_data_text}
```
0.2277675878319787
```



### 5. Bartholomew2's mobility measure

$$M_{B2} = \frac{1}{m-1} \sum_{i=1}^m \sum_{j=1}^m \pi_i P_{ij} |i-j|$$

$\pi$: the inital income distribution

```python
measure = "B1"```



{:.input_area}
```python
pi = np.array([0.1,0.2,0.2,0.4,0.1])
mobility.markov_mobility(m.p, measure = "B2", ini=pi)
```





{:.output_data_text}
```
0.04636660119478926
```



## Next steps

* Markov-based partial mobility measures
* Other mobility measures:
    * Inequality reduction mobility measures (Trede, 1999)
* Statistical inference for mobility measures

## References

* Formby, J. P., W. J. Smith, and B. Zheng. 2004. “[Mobility Measurement, Transition Matrices and Statistical Inference](http://www.sciencedirect.com/science/article/pii/S0304407603002112).” Journal of Econometrics 120 (1). Elsevier: 181–205.
* Trede, Mark. 1999. “[Statistical Inference for Measures of Income Mobility / Statistische Inferenz Zur Messung Der Einkommensmobilität](https://www.jstor.org/stable/23812388).” Jahrbücher Für Nationalökonomie Und Statistik / Journal of Economics and Statistics 218 (3/4). Lucius & Lucius Verlagsgesellschaft mbH: 473–90.

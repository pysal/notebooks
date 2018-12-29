---
redirect_from:
  - "/explore/pointpats/quadrat-statistics"
interact_link: content/explore/pointpats/Quadrat_statistics.ipynb
title: 'Quadrat_statistics'
prev_page:
  url: /explore/pointpats/process
  title: 'process'
next_page:
  url: /explore/pointpats/window
  title: 'window'
comment: "***PROGRAMMATICALLY GENERATED, DO NOT EDIT. SEE ORIGINAL FILES IN /content***"
---

# Quadrat Based Statistical Method for Planar Point Patterns

**Authors: Serge Rey <sjsrey@gmail.com>, Wei Kang <weikang9009@gmail.com> and Hu Shao <shaohutiger@gmail.com>**

## Introduction

In this notebook, we are going to introduce how to apply quadrat statistics to a point pattern to infer whether it comes from a CSR process.

1. In [Quadrat Statistic](#Quadrat-Statistic) we introduce the concept of quadrat based method.
2. We illustrate how to use the module **quadrat_statistics.py** through an example dataset **juvenile** in [Juvenile Example](#Juvenile-Example)

##  Quadrat Statistic

In the previous notebooks, we introduced the concept of Complete Spatial Randomness (CSR) process which serves as the benchmark process. Utilizing CSR properties, we can discriminate those that are not from a CSR process. Quadrat statistic is one such method. Since a CSR process has two major characteristics:
1. Uniform: each location has equal probability of getting a point (where an event happens).
2. Independent: location of event points are independent.

We can imagine that for any point pattern, if the underlying process is a CSR process, the expected point counts inside any cell of area $|A|$ should be $\lambda |A|$ ($\lambda$ is the intensity which is uniform across the study area for a CSR). Thus, if we impose a $m \times k$ rectangular tessellation over the study area (window), we can easily calculate the expected number of points inside each cell under the null of CSR. By comparing the observed point counts against the expected counts and calculate a $\chi^2$ test statistic, we can decide whether to reject the null based on the position of the $\chi^2$ test statistic in the sampling distribution. 

$$\chi^2 = \sum^m_{i=1} \sum^k_{j=1} \frac{[x_{i,j}-E(x_{i,j})]^2}{\lambda |A_{i,j}|}$$

There are two ways to construct the sampling distribution and acquire a p-value:
1. Analytical sampling distribution: a $\chi^2$ distribution of $m \times k -1$ degree of freedom. We can refer to the $\chi^2$ distribution table to acquire the p-value. If it is smaller than $0.05$, we will reject the null at the $95\%$ confidence level.
2. Empirical sampling distribution: a distribution constructed from a large number of $\chi^2$ test statistics for  simulations under the null of CSR. If the $\chi^2$ test statistic for the observed point pattern is among the largest $5%$ test statistics, we would say that it is very unlikely that it is the outcome of a CSR process at the $95\%$ confidence level. Then, the null is rejected. A pseudo p-value can be calculated based on which we can use the same rule as p-value to make the decision:
$$p(\chi^2) = \frac{1+\sum^{nsim}_{i=1}\phi_i}{nsim+1}$$
where 
$$ 
\phi_i =
 \begin{cases}
    1       & \quad \text{if } \psi_i^2 \geq \chi^2 \\
    0       & \quad \text{otherwise } \\
  \end{cases}
$$

$nsim$ is the number of simulations, $\psi_i^2$ is the $\chi^2$ test statistic calculated for each simulated point pattern, $\chi^2$ is the $\chi^2$ test statistic calculated for the observed point pattern, $\phi_i$ is an indicator variable.

We are going to introduce how to use the **quadrat_statistics.py** module to perform quadrat based method using either of the above two approaches to constructing the sampling distribution and acquire a p-value.


## Juvenile Example



{:.input_area}
```python
import libpysal as ps
import numpy as np
from pointpats import PointPattern, as_window
from pointpats import PoissonPointProcess as csr
%matplotlib inline
import matplotlib.pyplot as plt
```


Import the quadrat_statistics module to conduct quadrat-based method. 

Among the three major classes in the module, **RectangleM, HexagonM, QStatistic**, the first two are aimed at imposing a tessellation (rectangular or hexagonal shape) over the minimum bounding rectangle of the point pattern and calculate the number of points falling in each cell; **QStatistic** is the main class with which we can calculate a p-value, as well as a pseudo p-value to help us make the decision of rejecting the null or not.



{:.input_area}
```python
import pointpats.quadrat_statistics as qs
```




{:.input_area}
```python
dir(qs)
```





{:.output_data_text}
```
['HexagonM',
 'QStatistic',
 'RectangleM',
 '__all__',
 '__author__',
 '__builtins__',
 '__cached__',
 '__doc__',
 '__file__',
 '__loader__',
 '__name__',
 '__package__',
 '__spec__',
 'math',
 'np',
 'plt',
 'scipy']
```



Open the point shapefile "juvenile.shp".



{:.input_area}
```python
juv = ps.io.open(ps.examples.get_path("juvenile.shp"))
```




{:.input_area}
```python
len(juv) # 168 point events in total
```





{:.output_data_text}
```
168
```





{:.input_area}
```python
juv_points = np.array([event for event in juv]) # get x,y coordinates for all the points
juv_points
```





{:.output_data_text}
```
array([[94., 93.],
       [80., 95.],
       [79., 90.],
       [78., 92.],
       [76., 92.],
       [66., 93.],
       [64., 90.],
       [27., 70.],
       [58., 88.],
       [57., 92.],
       [53., 92.],
       [50., 90.],
       [49., 90.],
       [32., 90.],
       [31., 87.],
       [22., 87.],
       [21., 87.],
       [21., 86.],
       [22., 81.],
       [23., 83.],
       [27., 85.],
       [27., 84.],
       [27., 83.],
       [27., 82.],
       [30., 84.],
       [31., 84.],
       [31., 84.],
       [32., 83.],
       [33., 81.],
       [32., 79.],
       [32., 76.],
       [33., 77.],
       [34., 86.],
       [34., 84.],
       [38., 82.],
       [39., 81.],
       [40., 80.],
       [41., 83.],
       [43., 75.],
       [44., 81.],
       [46., 81.],
       [47., 82.],
       [47., 81.],
       [48., 80.],
       [48., 81.],
       [50., 85.],
       [51., 84.],
       [52., 83.],
       [55., 85.],
       [57., 88.],
       [57., 81.],
       [60., 87.],
       [69., 80.],
       [71., 82.],
       [72., 81.],
       [74., 82.],
       [75., 81.],
       [77., 88.],
       [80., 88.],
       [82., 77.],
       [66., 62.],
       [64., 71.],
       [59., 63.],
       [55., 64.],
       [53., 68.],
       [52., 59.],
       [51., 61.],
       [50., 75.],
       [50., 74.],
       [45., 61.],
       [44., 60.],
       [43., 59.],
       [42., 61.],
       [39., 71.],
       [37., 67.],
       [35., 70.],
       [31., 68.],
       [30., 71.],
       [29., 61.],
       [26., 69.],
       [24., 68.],
       [ 7., 52.],
       [11., 53.],
       [34., 50.],
       [36., 47.],
       [37., 45.],
       [37., 56.],
       [38., 55.],
       [38., 50.],
       [39., 52.],
       [41., 52.],
       [47., 49.],
       [50., 57.],
       [52., 56.],
       [53., 55.],
       [56., 57.],
       [69., 52.],
       [69., 50.],
       [71., 51.],
       [71., 51.],
       [73., 48.],
       [74., 48.],
       [75., 46.],
       [75., 46.],
       [86., 51.],
       [87., 51.],
       [87., 52.],
       [90., 52.],
       [91., 51.],
       [87., 42.],
       [81., 39.],
       [80., 43.],
       [79., 37.],
       [78., 38.],
       [75., 44.],
       [73., 41.],
       [71., 44.],
       [68., 29.],
       [62., 33.],
       [61., 35.],
       [60., 34.],
       [58., 36.],
       [54., 30.],
       [52., 38.],
       [52., 36.],
       [47., 37.],
       [46., 36.],
       [45., 33.],
       [36., 32.],
       [22., 39.],
       [21., 38.],
       [22., 35.],
       [21., 36.],
       [22., 30.],
       [19., 29.],
       [17., 40.],
       [14., 41.],
       [13., 36.],
       [10., 34.],
       [ 7., 37.],
       [ 2., 39.],
       [21., 16.],
       [22., 14.],
       [29., 17.],
       [30., 25.],
       [32., 26.],
       [39., 28.],
       [40., 26.],
       [40., 26.],
       [42., 25.],
       [43., 24.],
       [43., 16.],
       [48., 16.],
       [51., 25.],
       [52., 26.],
       [57., 27.],
       [60., 22.],
       [63., 24.],
       [64., 23.],
       [64., 27.],
       [71., 25.],
       [50., 10.],
       [48., 12.],
       [45., 14.],
       [33.,  8.],
       [31.,  7.],
       [32.,  6.],
       [31.,  8.]])
```



Construct a point pattern from numpy array **juv_points**.



{:.input_area}
```python
pp_juv = PointPattern(juv_points)
pp_juv
```





{:.output_data_text}
```
<pointpats.pointpattern.PointPattern at 0x1b18b92cf8>
```





{:.input_area}
```python
pp_juv.summary()
```


{:.output_stream}
```
Point Pattern
168 points
Bounding rectangle [(2.0,6.0), (94.0,95.0)]
Area of window: 8188.0
Intensity estimate for window: 0.02051783097215437
      x     y
0  94.0  93.0
1  80.0  95.0
2  79.0  90.0
3  78.0  92.0
4  76.0  92.0

```



{:.input_area}
```python
pp_juv.plot(window= True, title= "Point pattern")
```



![png](../../images/explore/pointpats/Quadrat_statistics_14_0.png)


### Rectangle quadrats & analytical sampling distribution

We can impose rectangle tessellation over mbb of the point pattern by specifying **shape** as "rectangle". We can also specify the number of rectangles in each row and column. For the current analysis, we use the $3 \times 3$ rectangle grids.



{:.input_area}
```python
q_r = qs.QStatistic(pp_juv,shape= "rectangle",nx = 3, ny = 3)
```


Use the plot method to plot the quadrats as well as the number of points falling in each quadrat.



{:.input_area}
```python
q_r.plot()
```



![png](../../images/explore/pointpats/Quadrat_statistics_18_0.png)




{:.input_area}
```python
q_r.chi2 #chi-squared test statistic for the observed point pattern
```





{:.output_data_text}
```
33.107142857142854
```





{:.input_area}
```python
q_r.df #degree of freedom
```





{:.output_data_text}
```
8
```





{:.input_area}
```python
q_r.chi2_pvalue # analytical pvalue
```





{:.output_data_text}
```
5.890978545159614e-05
```



Since the p-value based on the analytical $\chi^2$ distribution (degree of freedom = 8) is 0.0000589, much smaller than 0.05. We might determine that the underlying process is not CSR. We can also turn to empirical sampling distribution to ascertain our decision.

### Rectangle quadrats & empirical sampling distribution

To construct a empirical sampling distribution, we need to simulate CSR within the window of the observed point pattern a lot of times. Here, we generate 999 point patterns under the null of CSR.



{:.input_area}
```python
csr_process = csr(pp_juv.window, pp_juv.n, 999, asPP=True)
```


We specify parameter **realizations** as the point process instance which contains 999 CSR realizations.



{:.input_area}
```python
q_r_e = qs.QStatistic(pp_juv,shape= "rectangle",nx = 3, ny = 3, realizations = csr_process)
```




{:.input_area}
```python
q_r_e.chi2_r_pvalue
```





{:.output_data_text}
```
0.001
```



The pseudo p-value is 0.002, which is smaller than 0.05. Thus, we reject the null at the $95\%$ confidence level.

### Hexagon quadrats & analytical sampling distribution

We can also impose hexagon tessellation over mbb of the point pattern by specifying **shape** as "hexagon". We can also specify the length of the hexagon edge. For the current analysis, we specify it as 15.



{:.input_area}
```python
q_h = qs.QStatistic(pp_juv,shape= "hexagon",lh = 15)
```




{:.input_area}
```python
q_h.plot()
```



![png](../../images/explore/pointpats/Quadrat_statistics_31_0.png)




{:.input_area}
```python
q_h.chi2 #chi-squared test statistic for the observed point pattern
```





{:.output_data_text}
```
129.38095238095238
```





{:.input_area}
```python
q_h.df #degree of freedom
```





{:.output_data_text}
```
19
```





{:.input_area}
```python
q_h.chi2_pvalue  # analytical pvalue
```





{:.output_data_text}
```
1.909272893094198e-18
```



Similar to the inference of rectangle tessellation, since the analytical p-value is much smaller than 0.05, we reject the null of CSR. The point pattern is not random.

### Hexagon quadrats & empirical sampling distribution



{:.input_area}
```python
q_h_e = qs.QStatistic(pp_juv,shape= "hexagon",lh = 15, realizations = csr_process)
```




{:.input_area}
```python
q_h_e.chi2_r_pvalue
```





{:.output_data_text}
```
0.001
```



Because 0.001 is smaller than 0.05, we reject the null.

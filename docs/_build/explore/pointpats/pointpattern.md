---
redirect_from:
  - "/explore/pointpats/pointpattern"
interact_link: content/explore/pointpats/pointpattern.ipynb
title: 'pointpattern'
prev_page:
  url: /explore/pointpats/marks
  title: 'marks'
next_page:
  url: /explore/pointpats/process
  title: 'process'
comment: "***PROGRAMMATICALLY GENERATED, DO NOT EDIT. SEE ORIGINAL FILES IN /content***"
---

# Planar Point Patterns in PySAL

**Author: Serge Rey <sjsrey@gmail.com> and Wei Kang <weikang9009@gmail.com>**

## Introduction
This notebook introduces the basic PointPattern class in PySAL and covers the following:

* [What is a point pattern?](#What-is-a-point-pattern?)
* [Creating Point Patterns](#Creating-Point-Patterns)
* [Atributes of Point Patterns](#Attributes-of-PySAL-Point-Patterns)
* [Intensity Estimates](#Intensity-Estimates)
* [Next steps](#Next-steps)

## What is a point pattern?

We introduce basic terminology here and point the interested reader to more [detailed references](#References) on the underlying theory of the statistical analysis of point patterns.

### Points and Event Points

To start we consider a series of *point locations*, $(s_1, s_2, \ldots, s_n)$ in a study region $\Re$. We limit our focus here to a two-dimensional space so that $s_j = (x_j, y_j)$ is the spatial coordinate pair for point location $j$.

We will be interested in two different types of points.

#### Event Points

*Event Points* are locations where something of interest has occurred. The term *event* is very general here and could be used to represent a wide variety of phenomena. Some examples include:

* [locations of individual plants of a certain species](http://link.springer.com/chapter/10.1007/978-3-642-01976-0_7#page-1)
* [archeological sites](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=1&cad=rja&uact=8&ved=0ahUKEwjA46Si2oTKAhUU1GMKHZUBCBEQFgghMAA&url=http%3A%2F%2Fdiscovery.ucl.ac.uk%2F11345%2F&usg=AFQjCNG5dKBcsVJQZ9M20U5AOMTt3P6AWQ&sig2=Nt8ViSs8Q2G_-q1BSnNvKg&bvm=bv.110151844,d.cGc)
* [addresses of disease cases](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=1&cad=rja&uact=8&ved=0ahUKEwiy7NSE2oTKAhUOyWMKHb7cDA4QFgghMAA&url=http%3A%2F%2Fwww.jstor.org%2Fstable%2F622936&usg=AFQjCNExfettAsU3i-Hs7twmB6_iVkghUA&sig2=tPROSM6wMtbZT0qlg_N6Hw&bvm=bv.110151844,d.cGc)
* [locations of crimes](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=2&cad=rja&uact=8&ved=0ahUKEwiogfbl2YTKAhVT42MKHfTFCdUQFggqMAE&url=https%3A%2F%2Fgeodacenter.asu.edu%2Fsystem%2Ffiles%2Fpoints.pdf&usg=AFQjCNFase8ykAPuopayUDHQRvgj8S4Vsw&sig2=Ezzx45MLZIFaepvcOjV-aw)
* the [distribution of neurons](http://www.ncbi.nlm.nih.gov/pmc/articles/PMC2889688/)

among [many others](https://en.wikipedia.org/wiki/Point_process).

It is important to recognize that in the statistical analysis of point patterns the interest extends beyond the observed point pattern at hand.
The observed patterns are viewed as realizations from some underlying spatial stochastic process.


#### Arbitrary Points

The second type of point we consider are those locations where the phenomena  of interest has not been observed. These go by various names such as "empty space" or "regular" points, and at first glance might seem less interesting to a spatial analayst. However, these types of points play a central role in a class of point pattern methods that we explore below.


### Point Pattern Analysis

The analysis of event points focuses on a number of different characteristics of the collective spatial pattern that is observed. Often the pattern is jugded against the hypothesis of complete spatial randomness (CSR). That is, one assumes that the point events arise independently of one another and with constant probability across $\Re$, loosely speaking.

Of course, many of the empirical point patterns we encounter do not appear to be generated from such a simple stochastic process. The depatures from CSR can be due to two types of effects.

#### First order effects

For a point process, the first-order properties pertain to the intensity of the process across space. Whether and how the intensity of the point pattern varies within our study region are questions that assume center stage. Such variation in the itensity of the pattern of, say, addresses of individuals with a certain type of non-infectious disease may reflect the underlying population density. In other words, although the point pattern of disease cases may display variation in intensity in our study region, and thus violate the constant probability of an event condition, that spatial drift in the pattern intensity could be driven by an underlying covariate. 



#### Second order effects

The second channel by which departures from CSR can arise is through interaction and dependence between events in space. The canonical example being contagious diseases whereby the presence of an infected individual increases the probability of subsequent additional cases nearby.


When a pattern departs from expectation under CSR, this is suggestive that the underlying process may have some spatial structure that merits further investigation. Thus methods for detection of deviations from CSR and testing for alternative processes have given rise to a large literature in point pattern statistics.


### Methods of Point Pattern Analysis in PySAL

The points module in PySAL implements basic methods of point pattern analysis organized into the following groups:

* Point Processing
* Centrography and Visualization
* Quadrat Based Methods
* Distance Based Methods

In the remainder of this notebook we shall focus on point processing.



{:.input_area}
```python
import libpysal as ps
import numpy as np
from pointpats import PointPattern
```


## Creating Point Patterns

### From lists

We can build a point pattern by using Python lists of coordinate pairs $(s_0, s_1,\ldots, s_m)$ as follows:



{:.input_area}
```python
points = [[66.22, 32.54], [22.52, 22.39], [31.01, 81.21],
          [9.47, 31.02],  [30.78, 60.10], [75.21, 58.93],
          [79.26,  7.68], [8.23, 39.93],  [98.73, 77.17],
          [89.78, 42.53], [65.19, 92.08], [54.46, 8.48]]
p1 = PointPattern(points)
```




{:.input_area}
```python
p1.mbb
```





{:.output_data_text}
```
array([ 8.23,  7.68, 98.73, 92.08])
```



Thus $s_0 = (66.22, 32.54), \ s_{11}=(54.46, 8.48)$.



{:.input_area}
```python
p1.summary()
```


{:.output_stream}
```
Point Pattern
12 points
Bounding rectangle [(8.23,7.68), (98.73,92.08)]
Area of window: 7638.200000000002
Intensity estimate for window: 0.0015710507711240865
       x      y
0  66.22  32.54
1  22.52  22.39
2  31.01  81.21
3   9.47  31.02
4  30.78  60.10

```



{:.input_area}
```python
type(p1.points)
```





{:.output_data_text}
```
pandas.core.frame.DataFrame
```





{:.input_area}
```python
np.asarray(p1.points)
```





{:.output_data_text}
```
array([[66.22, 32.54],
       [22.52, 22.39],
       [31.01, 81.21],
       [ 9.47, 31.02],
       [30.78, 60.1 ],
       [75.21, 58.93],
       [79.26,  7.68],
       [ 8.23, 39.93],
       [98.73, 77.17],
       [89.78, 42.53],
       [65.19, 92.08],
       [54.46,  8.48]])
```





{:.input_area}
```python
p1.mbb
```





{:.output_data_text}
```
array([ 8.23,  7.68, 98.73, 92.08])
```



### From numpy arrays



{:.input_area}
```python
points = np.asarray(points)
points
```





{:.output_data_text}
```
array([[66.22, 32.54],
       [22.52, 22.39],
       [31.01, 81.21],
       [ 9.47, 31.02],
       [30.78, 60.1 ],
       [75.21, 58.93],
       [79.26,  7.68],
       [ 8.23, 39.93],
       [98.73, 77.17],
       [89.78, 42.53],
       [65.19, 92.08],
       [54.46,  8.48]])
```





{:.input_area}
```python
p1_np = PointPattern(points)
p1_np.summary()
```


{:.output_stream}
```
Point Pattern
12 points
Bounding rectangle [(8.23,7.68), (98.73,92.08)]
Area of window: 7638.200000000002
Intensity estimate for window: 0.0015710507711240865
       x      y
0  66.22  32.54
1  22.52  22.39
2  31.01  81.21
3   9.47  31.02
4  30.78  60.10

```

### From shapefiles

This example uses 200 randomly distributed points within the counties of Virginia. Coordinates are for UTM zone 17 N.



{:.input_area}
```python
f = ps.examples.get_path('vautm17n_points.shp')
fo = ps.io.open(f)
pp_va = PointPattern(np.asarray([pnt for pnt in fo]))
fo.close()
pp_va.summary()
```


{:.output_stream}
```
Point Pattern
200 points
Bounding rectangle [(273959.664381352,4049220.903414295), (972595.9895779632,4359604.85977962)]
Area of window: 216845506675.0557
Intensity estimate for window: 9.223156295311261e-10
               x             y
0  865322.486181  4.150317e+06
1  774479.213103  4.258993e+06
2  308048.692232  4.054700e+06
3  670711.529980  4.258864e+06
4  666254.475614  4.256514e+06

```

## Attributes of PySAL Point Patterns



{:.input_area}
```python
pp_va.summary()
```


{:.output_stream}
```
Point Pattern
200 points
Bounding rectangle [(273959.664381352,4049220.903414295), (972595.9895779632,4359604.85977962)]
Area of window: 216845506675.0557
Intensity estimate for window: 9.223156295311261e-10
               x             y
0  865322.486181  4.150317e+06
1  774479.213103  4.258993e+06
2  308048.692232  4.054700e+06
3  670711.529980  4.258864e+06
4  666254.475614  4.256514e+06

```



{:.input_area}
```python
pp_va.points
```





<div markdown="0">
<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>x</th>
      <th>y</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>865322.486181</td>
      <td>4.150317e+06</td>
    </tr>
    <tr>
      <th>1</th>
      <td>774479.213103</td>
      <td>4.258993e+06</td>
    </tr>
    <tr>
      <th>2</th>
      <td>308048.692232</td>
      <td>4.054700e+06</td>
    </tr>
    <tr>
      <th>3</th>
      <td>670711.529980</td>
      <td>4.258864e+06</td>
    </tr>
    <tr>
      <th>4</th>
      <td>666254.475614</td>
      <td>4.256514e+06</td>
    </tr>
    <tr>
      <th>5</th>
      <td>664464.571678</td>
      <td>4.061242e+06</td>
    </tr>
    <tr>
      <th>6</th>
      <td>784718.209785</td>
      <td>4.076109e+06</td>
    </tr>
    <tr>
      <th>7</th>
      <td>972595.989578</td>
      <td>4.183781e+06</td>
    </tr>
    <tr>
      <th>8</th>
      <td>657798.357403</td>
      <td>4.253278e+06</td>
    </tr>
    <tr>
      <th>9</th>
      <td>682259.020242</td>
      <td>4.282441e+06</td>
    </tr>
    <tr>
      <th>10</th>
      <td>727004.821077</td>
      <td>4.068344e+06</td>
    </tr>
    <tr>
      <th>11</th>
      <td>705895.874812</td>
      <td>4.266602e+06</td>
    </tr>
    <tr>
      <th>12</th>
      <td>828584.046576</td>
      <td>4.065666e+06</td>
    </tr>
    <tr>
      <th>13</th>
      <td>713905.086059</td>
      <td>4.316151e+06</td>
    </tr>
    <tr>
      <th>14</th>
      <td>881552.803340</td>
      <td>4.091455e+06</td>
    </tr>
    <tr>
      <th>15</th>
      <td>469051.359337</td>
      <td>4.117702e+06</td>
    </tr>
    <tr>
      <th>16</th>
      <td>316765.769715</td>
      <td>4.074300e+06</td>
    </tr>
    <tr>
      <th>17</th>
      <td>697788.542435</td>
      <td>4.060254e+06</td>
    </tr>
    <tr>
      <th>18</th>
      <td>735806.711384</td>
      <td>4.169688e+06</td>
    </tr>
    <tr>
      <th>19</th>
      <td>857188.061626</td>
      <td>4.069335e+06</td>
    </tr>
    <tr>
      <th>20</th>
      <td>840068.036835</td>
      <td>4.157035e+06</td>
    </tr>
    <tr>
      <th>21</th>
      <td>554658.507423</td>
      <td>4.056777e+06</td>
    </tr>
    <tr>
      <th>22</th>
      <td>273959.664381</td>
      <td>4.057244e+06</td>
    </tr>
    <tr>
      <th>23</th>
      <td>751755.354691</td>
      <td>4.212530e+06</td>
    </tr>
    <tr>
      <th>24</th>
      <td>862508.493456</td>
      <td>4.068196e+06</td>
    </tr>
    <tr>
      <th>25</th>
      <td>608082.366460</td>
      <td>4.137227e+06</td>
    </tr>
    <tr>
      <th>26</th>
      <td>783720.206483</td>
      <td>4.131364e+06</td>
    </tr>
    <tr>
      <th>27</th>
      <td>648766.829060</td>
      <td>4.193105e+06</td>
    </tr>
    <tr>
      <th>28</th>
      <td>560753.141222</td>
      <td>4.059971e+06</td>
    </tr>
    <tr>
      <th>29</th>
      <td>659157.093262</td>
      <td>4.157386e+06</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>170</th>
      <td>693186.966524</td>
      <td>4.139941e+06</td>
    </tr>
    <tr>
      <th>171</th>
      <td>845699.719699</td>
      <td>4.231892e+06</td>
    </tr>
    <tr>
      <th>172</th>
      <td>796797.110375</td>
      <td>4.313534e+06</td>
    </tr>
    <tr>
      <th>173</th>
      <td>691583.213674</td>
      <td>4.074581e+06</td>
    </tr>
    <tr>
      <th>174</th>
      <td>752905.895923</td>
      <td>4.166523e+06</td>
    </tr>
    <tr>
      <th>175</th>
      <td>963207.941343</td>
      <td>4.165624e+06</td>
    </tr>
    <tr>
      <th>176</th>
      <td>611691.334171</td>
      <td>4.049221e+06</td>
    </tr>
    <tr>
      <th>177</th>
      <td>777399.041143</td>
      <td>4.170244e+06</td>
    </tr>
    <tr>
      <th>178</th>
      <td>781453.204801</td>
      <td>4.124116e+06</td>
    </tr>
    <tr>
      <th>179</th>
      <td>675900.040876</td>
      <td>4.059235e+06</td>
    </tr>
    <tr>
      <th>180</th>
      <td>530691.417350</td>
      <td>4.087626e+06</td>
    </tr>
    <tr>
      <th>181</th>
      <td>555641.288115</td>
      <td>4.122360e+06</td>
    </tr>
    <tr>
      <th>182</th>
      <td>532600.970765</td>
      <td>4.051876e+06</td>
    </tr>
    <tr>
      <th>183</th>
      <td>800528.454702</td>
      <td>4.335969e+06</td>
    </tr>
    <tr>
      <th>184</th>
      <td>516747.058864</td>
      <td>4.104977e+06</td>
    </tr>
    <tr>
      <th>185</th>
      <td>647291.961412</td>
      <td>4.223991e+06</td>
    </tr>
    <tr>
      <th>186</th>
      <td>673236.038854</td>
      <td>4.292326e+06</td>
    </tr>
    <tr>
      <th>187</th>
      <td>534897.641241</td>
      <td>4.129232e+06</td>
    </tr>
    <tr>
      <th>188</th>
      <td>789507.980935</td>
      <td>4.240825e+06</td>
    </tr>
    <tr>
      <th>189</th>
      <td>701276.258284</td>
      <td>4.199411e+06</td>
    </tr>
    <tr>
      <th>190</th>
      <td>669424.422196</td>
      <td>4.276723e+06</td>
    </tr>
    <tr>
      <th>191</th>
      <td>602477.348747</td>
      <td>4.146360e+06</td>
    </tr>
    <tr>
      <th>192</th>
      <td>872333.052082</td>
      <td>4.156737e+06</td>
    </tr>
    <tr>
      <th>193</th>
      <td>773967.535489</td>
      <td>4.145192e+06</td>
    </tr>
    <tr>
      <th>194</th>
      <td>803387.940279</td>
      <td>4.173642e+06</td>
    </tr>
    <tr>
      <th>195</th>
      <td>876485.065262</td>
      <td>4.148120e+06</td>
    </tr>
    <tr>
      <th>196</th>
      <td>621600.111400</td>
      <td>4.177462e+06</td>
    </tr>
    <tr>
      <th>197</th>
      <td>450246.610116</td>
      <td>4.106031e+06</td>
    </tr>
    <tr>
      <th>198</th>
      <td>740919.375814</td>
      <td>4.359605e+06</td>
    </tr>
    <tr>
      <th>199</th>
      <td>797522.610898</td>
      <td>4.208606e+06</td>
    </tr>
  </tbody>
</table>
<p>200 rows × 2 columns</p>
</div>
</div>





{:.input_area}
```python
pp_va.head()
```





<div markdown="0">
<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>x</th>
      <th>y</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>865322.486181</td>
      <td>4.150317e+06</td>
    </tr>
    <tr>
      <th>1</th>
      <td>774479.213103</td>
      <td>4.258993e+06</td>
    </tr>
    <tr>
      <th>2</th>
      <td>308048.692232</td>
      <td>4.054700e+06</td>
    </tr>
    <tr>
      <th>3</th>
      <td>670711.529980</td>
      <td>4.258864e+06</td>
    </tr>
    <tr>
      <th>4</th>
      <td>666254.475614</td>
      <td>4.256514e+06</td>
    </tr>
  </tbody>
</table>
</div>
</div>





{:.input_area}
```python
pp_va.tail()
```





<div markdown="0">
<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>x</th>
      <th>y</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>195</th>
      <td>876485.065262</td>
      <td>4.148120e+06</td>
    </tr>
    <tr>
      <th>196</th>
      <td>621600.111400</td>
      <td>4.177462e+06</td>
    </tr>
    <tr>
      <th>197</th>
      <td>450246.610116</td>
      <td>4.106031e+06</td>
    </tr>
    <tr>
      <th>198</th>
      <td>740919.375814</td>
      <td>4.359605e+06</td>
    </tr>
    <tr>
      <th>199</th>
      <td>797522.610898</td>
      <td>4.208606e+06</td>
    </tr>
  </tbody>
</table>
</div>
</div>



### Intensity Estimates

The intensity of a point process at point $s_i$ can be defined as:

$$\lambda(s_j) = \lim \limits_{|\mathbf{A}s_j| \to 0} \left \{ \frac{E(Y(\mathbf{A}s_j)}{|\mathbf{A}s_j|} \right \}   $$

where $\mathbf{A}s_j$ is a small region surrounding location $s_j$ with area $|\mathbf{A}s_j|$, and $E(Y(\mathbf{A}s_j)$ is the expected number of event points in $\mathbf{A}s_j$. 

The intensity is the mean number of event points per unit of area at point $s_j$. 



Recall that one of the implications of CSR is that the intensity of the point process is constant in our study area $\Re$. In other words $\lambda(s_j) = \lambda(s_{j+1}) = \ldots = \lambda(s_n) = \lambda \ \forall s_j \in \Re$. Thus, if the area of $\Re$ = $|\Re|$ the expected number of event points in the study region is: $E(Y(\Re)) = \lambda |\Re|.$

In PySAL, the intensity is estimated by using a geometric object to encode the study region. We refer to this as the window, $W$. The reason for distinguishing between $\Re$ and $W$ is that the latter permits alternative definitions of the bounding object.

**Intensity estimates are based on the following:**
$$\hat{\lambda} = \frac{n}{|W|}$$

where $n$ is the number of points in the *window* $W$, and $|W|$ is the area of $W$.

**Intensity based on minimum bounding box:**
$$\hat{\lambda}_{mbb} = \frac{n}{|W_{mbb}|}$$

where $W_{mbb}$ is the minimum bounding box for the point pattern.



{:.input_area}
```python
pp_va.lambda_mbb
```





{:.output_data_text}
```
9.223156295311263e-10
```



**Intensity based on convex hull:**
$$\hat{\lambda}_{hull} = \frac{n}{|W_{hull}|}$$

where $W_{hull}$ is the convex hull for the point pattern.



{:.input_area}
```python
pp_va.lambda_hull
```





{:.output_data_text}
```
1.5973789098179388e-09
```



## Next steps


There is more to learn about point patterns in PySAL. 

The [centrographic notebook](centrography.ipynb) illustrates a number of spatial descriptive statistics and visualization of point patterns.

Clearly the window chosen will impact the intensity estimate. For more on **windows** see the [window notebook](window.ipynb).

To test if your point pattern departs from complete spatial randomness see the [distance statistics notebook](distance_statistics.ipynb) and  [quadrat statistics notebook](Quadrat_statistics.ipynb).


To simulate different types of point processes in various windows see [process notebook](process.ipynb).

If you have point pattern data with additional attributes associated with each point see how to handle this in the [marks notebook](marks.ipynb).



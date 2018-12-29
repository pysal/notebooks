---
redirect_from:
  - "/dynamics/giddy/rank-markov"
interact_link: content/dynamics/giddy/Rank_Markov.ipynb
title: 'Rank_Markov'
prev_page:
  url: /dynamics/giddy/Rank_based_Methods
  title: 'Rank_based_Methods'
next_page:
  url: /explore/esda/intro
  title: 'esda'
comment: "***PROGRAMMATICALLY GENERATED, DO NOT EDIT. SEE ORIGINAL FILES IN /content***"
---

# Full Rank Markov and Geographic Rank Markov

**Author: Wei Kang <weikang9009@gmail.com>**



{:.input_area}
```python
import libpysal as ps
import numpy as np
import matplotlib.pyplot as plt
%matplotlib inline
import seaborn as sns
import pandas as pd
import geopandas as gpd
```


## Full Rank Markov



{:.input_area}
```python
from giddy.markov import FullRank_Markov
```




{:.input_area}
```python
income_table = pd.read_csv(ps.examples.get_path("usjoin.csv"))
income_table.head()
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
      <th>Name</th>
      <th>STATE_FIPS</th>
      <th>1929</th>
      <th>1930</th>
      <th>1931</th>
      <th>1932</th>
      <th>1933</th>
      <th>1934</th>
      <th>1935</th>
      <th>1936</th>
      <th>...</th>
      <th>2000</th>
      <th>2001</th>
      <th>2002</th>
      <th>2003</th>
      <th>2004</th>
      <th>2005</th>
      <th>2006</th>
      <th>2007</th>
      <th>2008</th>
      <th>2009</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Alabama</td>
      <td>1</td>
      <td>323</td>
      <td>267</td>
      <td>224</td>
      <td>162</td>
      <td>166</td>
      <td>211</td>
      <td>217</td>
      <td>251</td>
      <td>...</td>
      <td>23471</td>
      <td>24467</td>
      <td>25161</td>
      <td>26065</td>
      <td>27665</td>
      <td>29097</td>
      <td>30634</td>
      <td>31988</td>
      <td>32819</td>
      <td>32274</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Arizona</td>
      <td>4</td>
      <td>600</td>
      <td>520</td>
      <td>429</td>
      <td>321</td>
      <td>308</td>
      <td>362</td>
      <td>416</td>
      <td>462</td>
      <td>...</td>
      <td>25578</td>
      <td>26232</td>
      <td>26469</td>
      <td>27106</td>
      <td>28753</td>
      <td>30671</td>
      <td>32552</td>
      <td>33470</td>
      <td>33445</td>
      <td>32077</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Arkansas</td>
      <td>5</td>
      <td>310</td>
      <td>228</td>
      <td>215</td>
      <td>157</td>
      <td>157</td>
      <td>187</td>
      <td>207</td>
      <td>247</td>
      <td>...</td>
      <td>22257</td>
      <td>23532</td>
      <td>23929</td>
      <td>25074</td>
      <td>26465</td>
      <td>27512</td>
      <td>29041</td>
      <td>31070</td>
      <td>31800</td>
      <td>31493</td>
    </tr>
    <tr>
      <th>3</th>
      <td>California</td>
      <td>6</td>
      <td>991</td>
      <td>887</td>
      <td>749</td>
      <td>580</td>
      <td>546</td>
      <td>603</td>
      <td>660</td>
      <td>771</td>
      <td>...</td>
      <td>32275</td>
      <td>32750</td>
      <td>32900</td>
      <td>33801</td>
      <td>35663</td>
      <td>37463</td>
      <td>40169</td>
      <td>41943</td>
      <td>42377</td>
      <td>40902</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Colorado</td>
      <td>8</td>
      <td>634</td>
      <td>578</td>
      <td>471</td>
      <td>354</td>
      <td>353</td>
      <td>368</td>
      <td>444</td>
      <td>542</td>
      <td>...</td>
      <td>32949</td>
      <td>34228</td>
      <td>33963</td>
      <td>34092</td>
      <td>35543</td>
      <td>37388</td>
      <td>39662</td>
      <td>41165</td>
      <td>41719</td>
      <td>40093</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 83 columns</p>
</div>
</div>





{:.input_area}
```python
pci = income_table[list(map(str,range(1929,2010)))].values
pci
```





{:.output_data_text}
```
array([[  323,   267,   224, ..., 31988, 32819, 32274],
       [  600,   520,   429, ..., 33470, 33445, 32077],
       [  310,   228,   215, ..., 31070, 31800, 31493],
       ...,
       [  460,   408,   356, ..., 29769, 31265, 31843],
       [  673,   588,   469, ..., 35839, 36594, 35676],
       [  675,   585,   476, ..., 43453, 45177, 42504]])
```





{:.input_area}
```python
m = FullRank_Markov(pci)
m.ranks
```





{:.output_data_text}
```
array([[45, 45, 44, ..., 41, 40, 39],
       [24, 25, 25, ..., 36, 38, 41],
       [46, 47, 45, ..., 43, 43, 43],
       ...,
       [34, 34, 34, ..., 47, 46, 42],
       [17, 17, 22, ..., 25, 26, 25],
       [16, 18, 19, ...,  6,  6,  7]])
```





{:.input_area}
```python
m.transitions
```





{:.output_data_text}
```
array([[66.,  5.,  5., ...,  0.,  0.,  0.],
       [ 8., 51.,  9., ...,  0.,  0.,  0.],
       [ 2., 13., 44., ...,  0.,  0.,  0.],
       ...,
       [ 0.,  0.,  0., ..., 40., 17.,  0.],
       [ 0.,  0.,  0., ..., 15., 54.,  2.],
       [ 0.,  0.,  0., ...,  2.,  1., 77.]])
```



Full rank Markov transition probability matrix



{:.input_area}
```python
m.p
```





{:.output_data_text}
```
array([[0.825 , 0.0625, 0.0625, ..., 0.    , 0.    , 0.    ],
       [0.1   , 0.6375, 0.1125, ..., 0.    , 0.    , 0.    ],
       [0.025 , 0.1625, 0.55  , ..., 0.    , 0.    , 0.    ],
       ...,
       [0.    , 0.    , 0.    , ..., 0.5   , 0.2125, 0.    ],
       [0.    , 0.    , 0.    , ..., 0.1875, 0.675 , 0.025 ],
       [0.    , 0.    , 0.    , ..., 0.025 , 0.0125, 0.9625]])
```



Full rank first mean passage times



{:.input_area}
```python
m.fmpt
```





{:.output_data_text}
```
array([[  48.        ,   87.96280048,   68.1089084 , ...,  443.76689275,
         518.31000749, 1628.59025557],
       [ 225.92564594,   48.        ,   78.75804364, ...,  440.0173313 ,
         514.56045127, 1624.84070661],
       [ 271.55443692,  102.484092  ,   48.        , ...,  438.93288204,
         513.47599512, 1623.75624059],
       ...,
       [ 727.11189921,  570.15910508,  546.61934646, ...,   48.        ,
         117.41906375, 1278.96860316],
       [ 730.40467469,  573.45179415,  549.91216045, ...,   49.70722573,
          48.        , 1202.06279368],
       [ 754.8761577 ,  597.92333477,  574.38361779, ...,   43.23574191,
         104.9460425 ,   48.        ]])
```





{:.input_area}
```python
m.sojourn_time
```





{:.output_data_text}
```
array([ 5.71428571,  2.75862069,  2.22222222,  1.77777778,  1.66666667,
        1.73913043,  1.53846154,  1.53846154,  1.53846154,  1.42857143,
        1.42857143,  1.56862745,  1.53846154,  1.40350877,  1.29032258,
        1.21212121,  1.31147541,  1.37931034,  1.29032258,  1.25      ,
        1.15942029,  1.12676056,  1.25      ,  1.17647059,  1.19402985,
        1.08108108,  1.19402985,  1.25      ,  1.25      ,  1.14285714,
        1.33333333,  1.26984127,  1.25      ,  1.37931034,  1.42857143,
        1.31147541,  1.26984127,  1.25      ,  1.31147541,  1.25      ,
        1.19402985,  1.25      ,  1.53846154,  1.6       ,  1.86046512,
        2.        ,  3.07692308, 26.66666667])
```





{:.input_area}
```python
df_fullrank = pd.DataFrame(np.c_[m.p.diagonal(),m.sojourn_time], columns=["Staying Probability","Sojourn Time"], index = np.arange(m.p.shape[0])+1)
df_fullrank.head()
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
      <th>Staying Probability</th>
      <th>Sojourn Time</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>1</th>
      <td>0.8250</td>
      <td>5.714286</td>
    </tr>
    <tr>
      <th>2</th>
      <td>0.6375</td>
      <td>2.758621</td>
    </tr>
    <tr>
      <th>3</th>
      <td>0.5500</td>
      <td>2.222222</td>
    </tr>
    <tr>
      <th>4</th>
      <td>0.4375</td>
      <td>1.777778</td>
    </tr>
    <tr>
      <th>5</th>
      <td>0.4000</td>
      <td>1.666667</td>
    </tr>
  </tbody>
</table>
</div>
</div>





{:.input_area}
```python
df_fullrank.plot(subplots=True, layout=(1,2), figsize=(15,5))
```





{:.output_data_text}
```
array([[<matplotlib.axes._subplots.AxesSubplot object at 0x1a2ad213c8>,
        <matplotlib.axes._subplots.AxesSubplot object at 0x1a2ad64668>]],
      dtype=object)
```




![png](../../images/dynamics/giddy/Rank_Markov_14_1.png)




{:.input_area}
```python
sns.distplot(m.fmpt.flatten(),kde=False)
```





{:.output_data_text}
```
<matplotlib.axes._subplots.AxesSubplot at 0x1a2ae70908>
```




![png](../../images/dynamics/giddy/Rank_Markov_15_1.png)


## Geographic Rank Markov



{:.input_area}
```python
from giddy.markov import GeoRank_Markov, Markov, sojourn_time
gm = GeoRank_Markov(pci)
```




{:.input_area}
```python
gm.transitions
```





{:.output_data_text}
```
array([[38.,  0.,  8., ...,  0.,  0.,  0.],
       [ 0., 15.,  0., ...,  0.,  1.,  0.],
       [ 6.,  0., 44., ...,  5.,  0.,  0.],
       ...,
       [ 2.,  0.,  5., ..., 34.,  0.,  0.],
       [ 0.,  0.,  0., ...,  0., 18.,  2.],
       [ 0.,  0.,  0., ...,  0.,  3., 14.]])
```





{:.input_area}
```python
gm.p
```





{:.output_data_text}
```
array([[0.475 , 0.    , 0.1   , ..., 0.    , 0.    , 0.    ],
       [0.    , 0.1875, 0.    , ..., 0.    , 0.0125, 0.    ],
       [0.075 , 0.    , 0.55  , ..., 0.0625, 0.    , 0.    ],
       ...,
       [0.025 , 0.    , 0.0625, ..., 0.425 , 0.    , 0.    ],
       [0.    , 0.    , 0.    , ..., 0.    , 0.225 , 0.025 ],
       [0.    , 0.    , 0.    , ..., 0.    , 0.0375, 0.175 ]])
```





{:.input_area}
```python
gm.sojourn_time[:10]
```





{:.output_data_text}
```
array([1.9047619 , 1.23076923, 2.22222222, 1.73913043, 1.15942029,
       3.80952381, 1.70212766, 1.25      , 1.31147541, 1.11111111])
```





{:.input_area}
```python
gm.sojourn_time
```





{:.output_data_text}
```
array([ 1.9047619 ,  1.23076923,  2.22222222,  1.73913043,  1.15942029,
        3.80952381,  1.70212766,  1.25      ,  1.31147541,  1.11111111,
        1.73913043,  1.37931034,  1.17647059,  1.21212121,  1.33333333,
        1.37931034,  1.09589041,  2.10526316,  2.        ,  1.45454545,
        1.26984127, 26.66666667,  1.19402985,  1.23076923,  1.09589041,
        1.56862745,  1.26984127,  2.42424242,  1.50943396,  2.        ,
        1.29032258,  1.09589041,  1.6       ,  1.42857143,  1.25      ,
        1.45454545,  1.29032258,  1.6       ,  1.17647059,  1.56862745,
        1.25      ,  1.37931034,  1.45454545,  1.42857143,  1.29032258,
        1.73913043,  1.29032258,  1.21212121])
```





{:.input_area}
```python
gm.fmpt
```





{:.output_data_text}
```
array([[ 48.        ,  63.35532038,  92.75274652, ...,  82.47515731,
         71.01114491,  68.65737127],
       [108.25928005,  48.        , 127.99032986, ...,  92.03098299,
         63.36652935,  61.82733039],
       [ 76.96801786,  64.7713783 ,  48.        , ...,  73.84595169,
         72.24682723,  69.77497173],
       ...,
       [ 93.3107474 ,  62.47670463, 105.80634118, ...,  48.        ,
         69.30121319,  67.08838421],
       [113.65278078,  61.1987031 , 133.57991745, ...,  96.0103924 ,
         48.        ,  56.74165107],
       [114.71894813,  63.4019776 , 134.73381719, ...,  97.287895  ,
         61.45565054,  48.        ]])
```





{:.input_area}
```python
income_table["geo_sojourn_time"] = gm.sojourn_time
i = 0
for state in income_table["Name"]:
    income_table["geo_fmpt_to_" + state] = gm.fmpt[:,i]
    income_table["geo_fmpt_from_" + state] = gm.fmpt[i,:]
    i = i + 1
income_table.head()
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
      <th>Name</th>
      <th>STATE_FIPS</th>
      <th>1929</th>
      <th>1930</th>
      <th>1931</th>
      <th>1932</th>
      <th>1933</th>
      <th>1934</th>
      <th>1935</th>
      <th>1936</th>
      <th>...</th>
      <th>geo_fmpt_to_Virginia</th>
      <th>geo_fmpt_from_Virginia</th>
      <th>geo_fmpt_to_Washington</th>
      <th>geo_fmpt_from_Washington</th>
      <th>geo_fmpt_to_West Virginia</th>
      <th>geo_fmpt_from_West Virginia</th>
      <th>geo_fmpt_to_Wisconsin</th>
      <th>geo_fmpt_from_Wisconsin</th>
      <th>geo_fmpt_to_Wyoming</th>
      <th>geo_fmpt_from_Wyoming</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Alabama</td>
      <td>1</td>
      <td>323</td>
      <td>267</td>
      <td>224</td>
      <td>162</td>
      <td>166</td>
      <td>211</td>
      <td>217</td>
      <td>251</td>
      <td>...</td>
      <td>72.186055</td>
      <td>109.828532</td>
      <td>82.994754</td>
      <td>118.769984</td>
      <td>82.475157</td>
      <td>93.310747</td>
      <td>71.011145</td>
      <td>113.652781</td>
      <td>68.657371</td>
      <td>114.718948</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Arizona</td>
      <td>4</td>
      <td>600</td>
      <td>520</td>
      <td>429</td>
      <td>321</td>
      <td>308</td>
      <td>362</td>
      <td>416</td>
      <td>462</td>
      <td>...</td>
      <td>67.544447</td>
      <td>60.838807</td>
      <td>76.090895</td>
      <td>66.729262</td>
      <td>92.030983</td>
      <td>62.476705</td>
      <td>63.366529</td>
      <td>61.198703</td>
      <td>61.827330</td>
      <td>63.401978</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Arkansas</td>
      <td>5</td>
      <td>310</td>
      <td>228</td>
      <td>215</td>
      <td>157</td>
      <td>157</td>
      <td>187</td>
      <td>207</td>
      <td>247</td>
      <td>...</td>
      <td>73.650943</td>
      <td>129.533691</td>
      <td>84.071211</td>
      <td>138.692513</td>
      <td>73.845952</td>
      <td>105.806341</td>
      <td>72.246827</td>
      <td>133.579917</td>
      <td>69.774972</td>
      <td>134.733817</td>
    </tr>
    <tr>
      <th>3</th>
      <td>California</td>
      <td>6</td>
      <td>991</td>
      <td>887</td>
      <td>749</td>
      <td>580</td>
      <td>546</td>
      <td>603</td>
      <td>660</td>
      <td>771</td>
      <td>...</td>
      <td>71.377700</td>
      <td>111.644884</td>
      <td>62.230417</td>
      <td>97.908341</td>
      <td>104.922271</td>
      <td>121.670243</td>
      <td>69.368408</td>
      <td>110.668388</td>
      <td>59.998457</td>
      <td>105.965215</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Colorado</td>
      <td>8</td>
      <td>634</td>
      <td>578</td>
      <td>471</td>
      <td>354</td>
      <td>353</td>
      <td>368</td>
      <td>444</td>
      <td>542</td>
      <td>...</td>
      <td>69.627179</td>
      <td>57.106339</td>
      <td>66.353930</td>
      <td>52.229230</td>
      <td>98.797636</td>
      <td>66.464398</td>
      <td>60.762589</td>
      <td>52.324565</td>
      <td>55.559020</td>
      <td>53.872702</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 180 columns</p>
</div>
</div>





{:.input_area}
```python
geo_table = gpd.read_file(ps.examples.get_path('us48.shp'))
# income_table = pd.read_csv(libpysal.examples.get_path("usjoin.csv"))
complete_table = geo_table.merge(income_table,left_on='STATE_NAME',right_on='Name')
complete_table.head()
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
      <th>AREA</th>
      <th>PERIMETER</th>
      <th>STATE_</th>
      <th>STATE_ID</th>
      <th>STATE_NAME</th>
      <th>STATE_FIPS_x</th>
      <th>SUB_REGION</th>
      <th>STATE_ABBR</th>
      <th>geometry</th>
      <th>Name</th>
      <th>...</th>
      <th>geo_fmpt_to_Virginia</th>
      <th>geo_fmpt_from_Virginia</th>
      <th>geo_fmpt_to_Washington</th>
      <th>geo_fmpt_from_Washington</th>
      <th>geo_fmpt_to_West Virginia</th>
      <th>geo_fmpt_from_West Virginia</th>
      <th>geo_fmpt_to_Wisconsin</th>
      <th>geo_fmpt_from_Wisconsin</th>
      <th>geo_fmpt_to_Wyoming</th>
      <th>geo_fmpt_from_Wyoming</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>20.750</td>
      <td>34.956</td>
      <td>1</td>
      <td>1</td>
      <td>Washington</td>
      <td>53</td>
      <td>Pacific</td>
      <td>WA</td>
      <td>(POLYGON ((-122.400749206543 48.22539520263672...</td>
      <td>Washington</td>
      <td>...</td>
      <td>71.663055</td>
      <td>73.756804</td>
      <td>48.000000</td>
      <td>48.000000</td>
      <td>101.592400</td>
      <td>81.692586</td>
      <td>65.219124</td>
      <td>70.701226</td>
      <td>53.126177</td>
      <td>64.476985</td>
    </tr>
    <tr>
      <th>1</th>
      <td>45.132</td>
      <td>34.527</td>
      <td>2</td>
      <td>2</td>
      <td>Montana</td>
      <td>30</td>
      <td>Mtn</td>
      <td>MT</td>
      <td>POLYGON ((-111.4746322631836 44.70223999023438...</td>
      <td>Montana</td>
      <td>...</td>
      <td>69.918931</td>
      <td>59.067897</td>
      <td>76.184088</td>
      <td>64.710823</td>
      <td>90.781850</td>
      <td>58.795201</td>
      <td>63.455248</td>
      <td>58.975522</td>
      <td>60.881954</td>
      <td>60.553000</td>
    </tr>
    <tr>
      <th>2</th>
      <td>9.571</td>
      <td>18.899</td>
      <td>3</td>
      <td>3</td>
      <td>Maine</td>
      <td>23</td>
      <td>N Eng</td>
      <td>ME</td>
      <td>(POLYGON ((-69.77778625488281 44.0740737915039...</td>
      <td>Maine</td>
      <td>...</td>
      <td>69.431862</td>
      <td>53.872836</td>
      <td>77.512381</td>
      <td>62.862378</td>
      <td>87.734760</td>
      <td>54.244823</td>
      <td>66.257807</td>
      <td>56.905741</td>
      <td>61.978506</td>
      <td>58.336426</td>
    </tr>
    <tr>
      <th>3</th>
      <td>21.874</td>
      <td>21.353</td>
      <td>4</td>
      <td>4</td>
      <td>North Dakota</td>
      <td>38</td>
      <td>W N Cen</td>
      <td>ND</td>
      <td>POLYGON ((-98.73005676269531 45.93829727172852...</td>
      <td>North Dakota</td>
      <td>...</td>
      <td>69.441690</td>
      <td>56.526347</td>
      <td>76.659646</td>
      <td>62.823668</td>
      <td>85.031218</td>
      <td>49.511240</td>
      <td>67.362718</td>
      <td>58.717458</td>
      <td>64.386382</td>
      <td>59.728719</td>
    </tr>
    <tr>
      <th>4</th>
      <td>22.598</td>
      <td>22.746</td>
      <td>5</td>
      <td>5</td>
      <td>South Dakota</td>
      <td>46</td>
      <td>W N Cen</td>
      <td>SD</td>
      <td>POLYGON ((-102.7879333496094 42.99532318115234...</td>
      <td>South Dakota</td>
      <td>...</td>
      <td>68.229894</td>
      <td>61.548209</td>
      <td>78.886304</td>
      <td>68.794083</td>
      <td>88.192659</td>
      <td>55.754109</td>
      <td>66.187694</td>
      <td>63.802359</td>
      <td>64.336311</td>
      <td>65.070022</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 189 columns</p>
</div>
</div>





{:.input_area}
```python
complete_table.columns
```





{:.output_data_text}
```
Index(['AREA', 'PERIMETER', 'STATE_', 'STATE_ID', 'STATE_NAME', 'STATE_FIPS_x',
       'SUB_REGION', 'STATE_ABBR', 'geometry', 'Name',
       ...
       'geo_fmpt_to_Virginia', 'geo_fmpt_from_Virginia',
       'geo_fmpt_to_Washington', 'geo_fmpt_from_Washington',
       'geo_fmpt_to_West Virginia', 'geo_fmpt_from_West Virginia',
       'geo_fmpt_to_Wisconsin', 'geo_fmpt_from_Wisconsin',
       'geo_fmpt_to_Wyoming', 'geo_fmpt_from_Wyoming'],
      dtype='object', length=189)
```



Visualizing first mean passage time from/to California/Mississippi:



{:.input_area}
```python
fig, axes = plt.subplots(nrows=2, ncols=2,figsize = (15,7))
target_states = ["California","Mississippi"]
directions = ["from","to"]
for i, direction in enumerate(directions):
    for j, target in enumerate(target_states):
        ax = axes[i,j]
        col = direction+"_"+target
        complete_table.plot(ax=ax,column = "geo_fmpt_"+ col,cmap='OrRd', 
                    scheme='quantiles', legend=True)
        ax.set_title("First Mean Passage Time "+direction+" "+target)
        ax.axis('off')
        leg = ax.get_legend()
        leg.set_bbox_to_anchor((0.8, 0.15, 0.16, 0.2))
plt.tight_layout()
```



![png](../../images/dynamics/giddy/Rank_Markov_27_0.png)


Visualizing sojourn time for each US state:



{:.input_area}
```python
fig, axes = plt.subplots(nrows=1, ncols=2,figsize = (15,7))
schemes = ["Quantiles","Equal_Interval"]
for i, scheme in enumerate(schemes):
    ax = axes[i]
    complete_table.plot(ax=ax,column = "geo_sojourn_time",cmap='OrRd', 
                scheme=scheme, legend=True)
    ax.set_title("Rank Sojourn Time ("+scheme+")")
    ax.axis('off')
    leg = ax.get_legend()
    leg.set_bbox_to_anchor((0.8, 0.15, 0.16, 0.2))
plt.tight_layout()
```



![png](../../images/dynamics/giddy/Rank_Markov_29_0.png)


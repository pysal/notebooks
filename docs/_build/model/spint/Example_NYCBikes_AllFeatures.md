---
redirect_from:
  - "/model/spint/example-nycbikes-allfeatures"
interact_link: content/model/spint/Example_NYCBikes_AllFeatures.ipynb
title: 'Example_NYCBikes_AllFeatures'
prev_page:
  url: /model/spint/dispersion_test
  title: 'dispersion_test'
next_page:
  url: /model/spint/local_SI
  title: 'local_SI'
comment: "***PROGRAMMATICALLY GENERATED, DO NOT EDIT. SEE ORIGINAL FILES IN /content***"
---



{:.input_area}
```python
from pysal.contrib.spint.gravity import  BaseGravity, Gravity, Production, Attraction, Doubly
from pysal.contrib.spint.dispersion import phi_disp
from pysal.contrib.spint.vec_SA import VecMoran
import pysal as ps
import pandas as pd
import geopandas as gp
import numpy as np
import seaborn as sb
import matplotlib.pylab as plt
%pylab inline
from descartes import PolygonPatch
import matplotlib as mpl
from mpl_toolkits.basemap import Basemap
import pyproj as pj
from shapely.geometry import Polygon, Point
```


{:.output_stream}
```
Populating the interactive namespace from numpy and matplotlib

```



{:.input_area}
```python
#Load NYC bike data - trips between census tract centroids
bikes = pd.read_csv(ps.examples.get_path('nyc_bikes_ct.csv'))
bikes.head()
```





<div markdown="0">
<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Unnamed: 0</th>
      <th>index</th>
      <th>count</th>
      <th>d_cap</th>
      <th>d_tract</th>
      <th>distance</th>
      <th>end station latitude</th>
      <th>end station longitude</th>
      <th>o_cap</th>
      <th>o_tract</th>
      <th>...</th>
      <th>weighted</th>
      <th>total_out</th>
      <th>total_in</th>
      <th>o_hub</th>
      <th>d_hub</th>
      <th>od_hub</th>
      <th>SX</th>
      <th>SY</th>
      <th>EX</th>
      <th>EY</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0</td>
      <td>0</td>
      <td>5709</td>
      <td>255.0</td>
      <td>600</td>
      <td>NaN</td>
      <td>40.712899</td>
      <td>-73.989865</td>
      <td>162.0</td>
      <td>202</td>
      <td>...</td>
      <td>0.0</td>
      <td>56352</td>
      <td>69165</td>
      <td>hub</td>
      <td>hub</td>
      <td>hub</td>
      <td>585995.353038</td>
      <td>4.507417e+06</td>
      <td>585322.159723</td>
      <td>4.507378e+06</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1</td>
      <td>1</td>
      <td>4010</td>
      <td>595.0</td>
      <td>600</td>
      <td>NaN</td>
      <td>40.712899</td>
      <td>-73.989865</td>
      <td>774.0</td>
      <td>700</td>
      <td>...</td>
      <td>0.0</td>
      <td>160040</td>
      <td>69165</td>
      <td>hub</td>
      <td>hub</td>
      <td>hub</td>
      <td>583785.918305</td>
      <td>4.506573e+06</td>
      <td>585322.159723</td>
      <td>4.507378e+06</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2</td>
      <td>2</td>
      <td>1906</td>
      <td>170.0</td>
      <td>600</td>
      <td>NaN</td>
      <td>40.712899</td>
      <td>-73.989865</td>
      <td>141.0</td>
      <td>800</td>
      <td>...</td>
      <td>0.0</td>
      <td>34254</td>
      <td>69165</td>
      <td>hub</td>
      <td>hub</td>
      <td>non_hub</td>
      <td>585018.109713</td>
      <td>4.507320e+06</td>
      <td>585322.159723</td>
      <td>4.507378e+06</td>
    </tr>
    <tr>
      <th>3</th>
      <td>3</td>
      <td>3</td>
      <td>1192</td>
      <td>255.0</td>
      <td>600</td>
      <td>NaN</td>
      <td>40.712899</td>
      <td>-73.989865</td>
      <td>291.0</td>
      <td>900</td>
      <td>...</td>
      <td>0.0</td>
      <td>46446</td>
      <td>69165</td>
      <td>hub</td>
      <td>hub</td>
      <td>non_hub</td>
      <td>583444.520998</td>
      <td>4.506199e+06</td>
      <td>585322.159723</td>
      <td>4.507378e+06</td>
    </tr>
    <tr>
      <th>4</th>
      <td>4</td>
      <td>4</td>
      <td>484</td>
      <td>85.0</td>
      <td>600</td>
      <td>NaN</td>
      <td>40.712899</td>
      <td>-73.989865</td>
      <td>57.0</td>
      <td>1002</td>
      <td>...</td>
      <td>0.0</td>
      <td>15916</td>
      <td>69165</td>
      <td>hub</td>
      <td>hub</td>
      <td>non_hub</td>
      <td>586462.456350</td>
      <td>4.507937e+06</td>
      <td>585322.159723</td>
      <td>4.507378e+06</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 35 columns</p>
</div>
</div>





{:.input_area}
```python
#Process data

#Remove intrazonal flows
bikes = bikes[bikes['o_tract'] != bikes['d_tract']]

#Set zero attirbute values to a small constant
bikes.ix[bikes.o_sq_foot == 0, 'o_sq_foot'] = 1
bikes.ix[bikes.d_sq_foot == 0, 'd_sq_foot'] = 1
bikes.ix[bikes.o_cap == 0, 'o_cap'] = 1
bikes.ix[bikes.d_cap == 0, 'd_cap'] = 1
bikes.ix[bikes.o_housing == 0, 'o_housing'] = 1
bikes.ix[bikes.d_housing == 0, 'd_housing'] = 1

#Flows between tracts
flows = bikes['count'].values.reshape((-1,1))

#Origin variables: square footage of buildings, housing units, total station capacity
o_vars = np.hstack([bikes['o_sq_foot'].values.reshape((-1,1)),
                    bikes['o_housing'].values.reshape((-1,1)),
                    bikes['o_cap'].values.reshape((-1,1))])

#Destination variables: square footage of buildings, housing units, total station capacity
d_vars = np.hstack([bikes['d_sq_foot'].values.reshape((-1,1)),
                    bikes['d_housing'].values.reshape((-1,1)),
                    bikes['d_cap'].values.reshape((-1,1))])

#Trip "cost" in time (seconds)
cost = bikes['tripduration'].values.reshape((-1,1))

#Origin ids
o = bikes['o_tract'].astype(str).values.reshape((-1,1))

#destination ids
d = bikes['d_tract'].astype(str).values.reshape((-1,1))

print len(bikes), ' OD pairs between census tracts after filtering out intrazonal flows'
```


{:.output_stream}
```
14042  OD pairs between census tracts after filtering out intrazonal flows

```



{:.input_area}
```python
#First we fit a basic gravity model and examine the parameters and model fit

grav= Gravity(flows, o_vars, d_vars, cost, 'exp')

print grav.params

print 'Adjusted psuedo R2: ', grav.adj_pseudoR2
print 'Adjusted D2: ', grav.adj_D2
print 'SRMSE: ', grav.SRMSE
print 'Sorensen similarity index: ', grav.SSI
```


{:.output_stream}
```
[ 0.09898099  0.05748786  0.50319944  0.06920194  0.06408526  0.39371417
 -0.00226671]
Adjusted psuedo R2:  0.772607968896
Adjusted D2:  0.77684235847
SRMSE:  0.924994119459
Sorensen similarity index:  0.746131903798

```



{:.input_area}
```python
#Next we fit a production-constrained model

prod = Production(flows, o, d_vars, cost, 'exp')

print prod.params[-4:] #truncate to exclude balancing factors/fixed effects

print 'Adjusted psuedo R2: ', prod.adj_pseudoR2
print 'Adjusted D2: ', prod.adj_D2
print 'SRMSE: ', prod.SRMSE
print 'Sorensen similarity index: ', prod.SSI
```


{:.output_stream}
```
[ 0.00437122  0.06794379  0.85720958 -0.00227555]
Adjusted psuedo R2:  0.832399632692
Adjusted D2:  0.836963213893
SRMSE:  0.794147843751
Sorensen similarity index:  0.777965361121

```



{:.input_area}
```python
#Next we fit an attraction-constrained model

att = Attraction(flows, d, o_vars, cost, 'exp')

print att.params[-4:] #truncate to exclude balancing factors/fixed effects

print 'Adjusted psuedo R2: ', att.adj_pseudoR2
print 'Adjusted D2: ', att.adj_D2
print 'SRMSE: ', att.SRMSE
print 'Sorensen similarity index: ', att.SSI
```


{:.output_stream}
```
[ 0.05281568  0.05689814  0.85161213 -0.00229343]
Adjusted psuedo R2:  0.83252844463
Adjusted D2:  0.83709408585
SRMSE:  0.792604389867
Sorensen similarity index:  0.777557481635

```



{:.input_area}
```python
#Finally, we fit the doubly constrained model

doub = Doubly(flows, o, d, cost, 'exp')

print doub.params[-1:] #truncate to exclude balancing factors/fixed effects

print 'Adjusted psuedo R2: ', doub.adj_pseudoR2
print 'Adjusted D2: ', doub.adj_D2
print 'SRMSE: ', doub.SRMSE
print 'Sorensen similarity index: ', doub.SSI
```


{:.output_stream}
```
[-0.00232112]
Adjusted psuedo R2:  0.895575966583
Adjusted D2:  0.900342219279
SRMSE:  0.627981455879
Sorensen similarity index:  0.818294076455

```



{:.input_area}
```python
#Next, we can test the models for violations of the equidispersion assumption of Poisson models

#test the hypotehsis of equidispersion (var[mu] = mu) against that of QuasiPoisson (var[mu] = phi * mu)
#Results = [phi, tvalue, pvalue]
print phi_disp(grav)
print phi_disp(prod)
print phi_disp(att)
print phi_disp(doub)

#We can see for all four models there is overdispersion (phi >> 0), 
#which are statistically significant according the tvalues (large)
#and pvalues (essentially zero). It does however decrease as more 
#constraints are introduced and model fit increases
```


{:.output_stream}
```
[  2.99777896e+002   2.38580701e+001   4.17517731e-126]
[  2.06092255e+002   2.60328203e+001   1.05289599e-149]
[  2.07645243e+002   2.64229678e+001   3.73180682e-154]
[  1.18261248e+002   2.96580921e+001   1.33362721e-193]

```



{:.input_area}
```python
#As a result we can compare our standard errors and tvalues for a Poisson model to a QuasiPoisson

print 'Production-constrained Poisson model standard errors and tvalues'
print prod.params[-4:]
print prod.std_err[-4:]
print prod.tvalues[-4:]

#Fit the same model using QuasiPoisson framework
Quasi = Production(flows, o, d_vars, cost, 'exp', Quasi=True)

print 'Production-constrained QuasiPoisson model standard errors and tvalues'
print Quasi.params[-4:]
print Quasi.std_err[-4:]
print Quasi.tvalues[-4:]

#As we can see both models result in the same parameters (first line)
#We also see the QuasiPoisson results in larger standard errors (middle line)
#Which then results in smaller t-values (bottom line)
#We would even consdier rejecting the statistical significant of of the 
#parameter estimate on destination building square footage because its abolsute 
# value is less than 1.96 (96% confidence level) 
```


{:.output_stream}
```
Production-constrained Poisson model standard errors and tvalues
[ 0.00437122  0.06794379  0.85720958 -0.00227555]
[  5.00039382e-04   3.52444295e-04   6.85493176e-04   1.00141356e-06]
[    8.74174692   192.77880405  1250.5005361  -2272.33530432]
Production-constrained QuasiPoisson model standard errors and tvalues
[ 0.00437122  0.06794379  0.85720958 -0.00227555]
[  7.21095039e-03   5.08251633e-03   9.88533597e-03   1.44411496e-05]
[   0.60619162   13.36813995   86.71527071 -157.57383972]

```



{:.input_area}
```python
#We can also estimate a local model which subsets the data
#For a production constrained model this means each local model
#is from one origin to all destinations. Since we get a set of 
#parameter estimates for each origin, we can then map them.

local_prod = prod.local()
```




{:.input_area}
```python
#There is a set of local parameter estimates, tvalues, and pvalues for each covariate
#And there is a set of local values for each diagnostic

local_prod.keys()
```





{:.output_data_text}
```
['pvalue3',
 'pvalue2',
 'SRMSE',
 'pvalue0',
 'deviance',
 'adj_pseudoR2',
 'pvalue1',
 'tvalue0',
 'tvalue2',
 'tvalue3',
 'adj_D2',
 'tvalue1',
 'SSI',
 'aic',
 'param1',
 'param0',
 'param3',
 'D2',
 'pseudoR2',
 'param2']
```





{:.input_area}
```python
#Prep geometry for plotting

#Read in census tracts for NYC
crs = {'datum':'WGS84', 'proj':'longlat'}
tracts = ps.examples.get_path('nyct2010.shp')
tracts = gp.read_file(tracts)
tracts = tracts.to_crs(crs=crs)

#subset manhattan tracts
man_tracts = tracts[tracts['BoroCode'] == '1'].copy()
man_tracts['CT2010S'] = man_tracts['CT2010'].astype(int).astype(str)

#Get tracts for which there are no onbservations
mt = set(man_tracts.CT2010S.unique())
lt = set(np.unique(o))
nt = list(mt.difference(lt))
no_tracts = pd.DataFrame({'no_tract':nt})
no_tracts = man_tracts[man_tracts.CT2010S.isin(nt)].copy()

#Join local values to census tracts
local_vals = pd.DataFrame({'betas': local_prod['param3'], 'tract':np.unique(o)})
local_vals = pd.merge(local_vals, man_tracts[['CT2010S', 'geometry']], left_on='tract', right_on='CT2010S')
local_vals = gp.GeoDataFrame(local_vals)


```




{:.input_area}
```python
#Plot local "cost" values: darker blue is stronger distance decay; grey is no data

fig = plt.figure(figsize=(12,12))
ax = fig.add_subplot(111)
local_vals['inv_betas'] = (local_vals['betas']*-1)
no_tracts['test'] = 0
no_tracts.plot('test', cmap='copper', ax=ax)
local_vals.plot('inv_betas', cmap='Blues', ax=ax)
plt.xlim(-74.02, -73.95)
plt.ylim(40.7, 40.78)
```





{:.output_data_text}
```
(40.7, 40.78)
```




![png](../../images/model/spint/Example_NYCBikes_AllFeatures_12_1.png)




{:.input_area}
```python
#Plot local estimates for destination capacity: darker red is larger effect; grey is no data

fig = plt.figure(figsize=(12,12))
ax = fig.add_subplot(111)
local_vals['cap'] = local_prod['param3']
no_tracts['test'] = 0
no_tracts.plot('test', cmap='copper', ax=ax)
local_vals.plot('cap', cmap='Reds', ax=ax)
plt.legend()
plt.xlim(-74.02, -73.95)
plt.ylim(40.7, 40.78)
```





{:.output_data_text}
```
(40.7, 40.78)
```




![png](../../images/model/spint/Example_NYCBikes_AllFeatures_13_1.png)




{:.input_area}
```python
#Plot local estimates for # of housing units: darker red is larger effect; grey is no data

fig = plt.figure(figsize=(12,12))
ax = fig.add_subplot(111)
local_vals['house'] = local_prod['param2']
no_tracts['test'] = 0
no_tracts.plot('test', cmap='copper', ax=ax)
local_vals.plot('house', cmap='Reds', ax=ax)
plt.legend()
plt.xlim(-74.02, -73.95)
plt.ylim(40.7, 40.78)
```





{:.output_data_text}
```
(40.7, 40.78)
```




![png](../../images/model/spint/Example_NYCBikes_AllFeatures_14_1.png)




{:.input_area}
```python
#Plot local estimates for destination building sq footage: darker red is larger effect; grey is no data

fig = plt.figure(figsize=(12,12))
ax = fig.add_subplot(111)
local_vals['foot'] = local_prod['param1']
no_tracts['test'] = 0
no_tracts.plot('test', cmap='copper', ax=ax)
local_vals.plot('foot', cmap='Reds', ax=ax)
plt.legend()
plt.xlim(-74.02, -73.95)
plt.ylim(40.7, 40.78)
```





{:.output_data_text}
```
(40.7, 40.78)
```




![png](../../images/model/spint/Example_NYCBikes_AllFeatures_15_1.png)




{:.input_area}
```python
#Drop NA values
labels = ['start station longitude', 'start station latitude', 'end station longitude', 'end station latitude']
bikes = bikes.dropna(subset=labels)
```




{:.input_area}
```python
#Prep OD data as vectors and then compute origin or destination focused distance-based weights

ids = bikes['index'].reshape((-1,1))
origin_x = bikes['SX'].reshape((-1,1))
origin_y = bikes['SY'].reshape((-1,1))
dest_x = bikes['EX'].reshape((-1,1))
dest_y = bikes['EY'].reshape((-1,1))


vecs = np.hstack([ids, origin_x, origin_y, dest_x, dest_y])
origins = vecs[:,1:3]
wo = ps.weights.DistanceBand(origins, 999, alpha=-1.5, binary=False, build_sp=False, silent=True)
dests = vecs[:,3:5]
wd = ps.weights.DistanceBand(dests, 999, alpha=-1.5, binary=False, build_sp=False, silent=True)

```




{:.input_area}
```python
#Origin focused Moran's I of OD pairs as vectors in space
vmo = VecMoran(vecs, wo, permutations=1)
vmo.I
```





{:.output_data_text}
```
0.15734115508365823
```





{:.input_area}
```python
#Destination focused Moran's I of OD pairs as vectors in space
vmd = VecMoran(vecs, wd, permutations=1)
vmd.I
```





{:.output_data_text}
```
0.21322002653342809
```





{:.input_area}
```python
#No substantial examples to show for spatial interaction weights
#Will add them once there is a working SAR Lag spatial interaction
#model implementation avaialble
#from pysal.weights.spintW import vecW, netW, ODW
```


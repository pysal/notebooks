---
redirect_from:
  - "/explore/pointpats/minimum-bounding-circle"
interact_link: content/explore/pointpats/Minimum_bounding_circle.ipynb
title: 'Minimum_bounding_circle'
prev_page:
  url: /explore/pointpats/marks
  title: 'marks'
next_page:
  url: /explore/pointpats/pointpattern
  title: 'pointpattern'
comment: "***PROGRAMMATICALLY GENERATED, DO NOT EDIT. SEE ORIGINAL FILES IN /content***"
---



{:.input_area}
```python
import matplotlib.pyplot as plt
import matplotlib.collections as mplc
import libpysal as ps
from shapely import geometry as sgeom
import descartes as des
import pointpats 
%matplotlib inline
```




{:.input_area}
```python
data = ps.io.open(ps.examples.get_path('columbus.shp')).read()
chains = [chain.parts[0] for chain in data]
```




{:.input_area}
```python
points = chains[0]
points
```





{:.output_data_text}
```
[(8.624129295349121, 14.236980438232422),
 (8.559700012207031, 14.742449760437012),
 (8.809452056884766, 14.734430313110352),
 (8.808412551879883, 14.636520385742188),
 (8.919304847717285, 14.638500213623047),
 (9.087138175964355, 14.63049030303955),
 (9.09996509552002, 14.244830131530762),
 (9.015047073364258, 14.241840362548828),
 (9.008951187133789, 13.995059967041016),
 (8.818140029907227, 14.002050399780273),
 (8.653305053710938, 14.008090019226074),
 (8.642902374267578, 14.089710235595703),
 (8.63259220123291, 14.1705904006958),
 (8.625825881958008, 14.22367000579834),
 (8.624129295349121, 14.236980438232422)]
```



Let's plot that polygon by interpreting it in Shapely and using its draw behavior.



{:.input_area}
```python
poly = sgeom.Polygon(points)
poly
```





![svg](../../images/explore/pointpats/Minimum_bounding_circle_4_0.svg)



Nifty. Now, I've implemented Skyum's method for finding the Minimum Bounding Circle for a set of points in `centrography`. 

Right now, there's some extra printing. Essentially, if you have sufficiently straight lines on the boundary, the equations for the circumcenter of the tuple $(p,q,r)$ explodes. Thus, I test if $\angle (p,q,r)$ identifies a circle whose diameter is $(p,r)$ or $(p,q)$. There are two triplets of straight enough lines, so their circle equations are modified, and I retain printing for bug diagnostics.



{:.input_area}
```python
(radius, center), inset, removed, constraints = pointpats.skyum(points)
#p,q,r = cent.skyum(points)
#mbc = cent._circle(points[p], points[q], points[r])
#mbc = cent._circle()
mbc_poly = sgeom.Point(*center).buffer(radius)
```




{:.input_area}
```python
fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(111)
ax.set_xlim(8, 10)
ax.set_ylim(13,16)
ax.plot([p[0] for p in points], [p[-1] for p in points], 'r')
ax.add_patch(des.PolygonPatch(mbc_poly, fc='white', ec='black'))
chull = pointpats.hull(points)
ax.plot([p[0] for p in chull], [p[-1] for p in chull], 'm')
ax.plot([p[0] for p in constraints], [p[-1] for p in constraints], '^b')
ax.plot([p[0] for p in inset], [p[-1] for p in inset], 'ob')
ax.plot([p[0] for p in removed], [p[-1] for p in removed], 'xb')
plt.show()
```



![png](../../images/explore/pointpats/Minimum_bounding_circle_8_0.png)


### Cool. How fast is this?



{:.input_area}
```python
import time
```




{:.input_area}
```python
def demo_mbc(chains):
    for cidx, chain in enumerate(chains):
        points = chain
        start = time.time()
        (radius, center), inset, removed, constraints = pointpats.skyum(chain)
        elapsed = time.time() - start
        mbc_poly = sgeom.Point(*center).buffer(radius)
        fig = plt.figure(figsize=(8,8))
        ax = fig.add_subplot(111)
        parray = ps.common.np.array(points)
        ax.set_xlim(parray[:,0].min()*.98, parray[:,0].max()*1.02)
        ax.set_ylim(parray[:,1].min()*.98, parray[:,1].max()*1.02)
        ax.plot([p[0] for p in points], [p[-1] for p in points], 'r')
        ax.add_patch(des.PolygonPatch(mbc_poly, fc='white', ec='black'))
        chull = pointpats.hull(points)
        #ax.plot([p[0] for p in chull], [p[-1] for p in chull], '--m')
        ax.plot([p[0] for p in constraints], [p[-1] for p in constraints], '^b')
        #ax.plot([p[0] for p in inset], [p[-1] for p in inset], 'ob')
        ax.plot([p[0][0] for p in removed[:-1]], [p[0][1] for p in removed[:-1]], 'xc')
        ax.plot(removed[-1][0][0], removed[-1][0][1], '*k')
        plt.title('Shape #{}, Elapsed Time: {}'.format(cidx, elapsed))
        #print(removed)
        nonboundary = [p for p in chull.tolist() if p not in constraints]
        succeeded = [mbc_poly.contains(sgeom.Point(p)) for p in nonboundary]
        for i,v in enumerate(succeeded):
            print("Point {i}: {tf}".format(i=i, tf=v))
            if not v:
                ax.plot(chull.tolist()[i][0], chull.tolist()[i][1], 'gH')
        plt.show()
        plt.clf()
```




{:.input_area}
```python
demo_mbc(chains)
```


{:.output_stream}
```
Point 0: True
Point 1: True
Point 2: True
Point 3: True
Point 4: True
Point 5: True

```


![png](../../images/explore/pointpats/Minimum_bounding_circle_12_1.png)


{:.output_stream}
```
Point 0: True
Point 1: True
Point 2: True
Point 3: True
Point 4: True
Point 5: True
Point 6: True
Point 7: True
Point 8: True

```


{:.output_data_text}
```
<Figure size 432x288 with 0 Axes>
```



![png](../../images/explore/pointpats/Minimum_bounding_circle_12_4.png)


{:.output_stream}
```
Point 0: False
Point 1: True
Point 2: True
Point 3: True
Point 4: True

```


{:.output_data_text}
```
<Figure size 432x288 with 0 Axes>
```



![png](../../images/explore/pointpats/Minimum_bounding_circle_12_7.png)


{:.output_stream}
```
Point 0: True
Point 1: True
Point 2: True
Point 3: True
Point 4: True
Point 5: True
Point 6: True
Point 7: True

```


{:.output_data_text}
```
<Figure size 432x288 with 0 Axes>
```



![png](../../images/explore/pointpats/Minimum_bounding_circle_12_10.png)


{:.output_stream}
```
Point 0: False
Point 1: True
Point 2: True
Point 3: True
Point 4: True

```


{:.output_data_text}
```
<Figure size 432x288 with 0 Axes>
```



![png](../../images/explore/pointpats/Minimum_bounding_circle_12_13.png)


{:.output_stream}
```
Point 0: True
Point 1: True
Point 2: True
Point 3: True
Point 4: True
Point 5: True
Point 6: True
Point 7: True

```


{:.output_data_text}
```
<Figure size 432x288 with 0 Axes>
```



![png](../../images/explore/pointpats/Minimum_bounding_circle_12_16.png)


{:.output_stream}
```
Point 0: True
Point 1: True
Point 2: True
Point 3: True
Point 4: True
Point 5: True
Point 6: True
Point 7: True

```


{:.output_data_text}
```
<Figure size 432x288 with 0 Axes>
```



![png](../../images/explore/pointpats/Minimum_bounding_circle_12_19.png)


{:.output_stream}
```
Point 0: True
Point 1: True
Point 2: True
Point 3: True
Point 4: True
Point 5: True
Point 6: True
Point 7: True

```


{:.output_data_text}
```
<Figure size 432x288 with 0 Axes>
```



![png](../../images/explore/pointpats/Minimum_bounding_circle_12_22.png)


{:.output_stream}
```
Point 0: True
Point 1: True
Point 2: True
Point 3: True
Point 4: True
Point 5: True
Point 6: True
Point 7: True
Point 8: True
Point 9: True

```


{:.output_data_text}
```
<Figure size 432x288 with 0 Axes>
```



![png](../../images/explore/pointpats/Minimum_bounding_circle_12_25.png)


{:.output_stream}
```
Point 0: True
Point 1: True
Point 2: True
Point 3: True
Point 4: True
Point 5: True
Point 6: True
Point 7: True
Point 8: True
Point 9: True

```


{:.output_data_text}
```
<Figure size 432x288 with 0 Axes>
```



![png](../../images/explore/pointpats/Minimum_bounding_circle_12_28.png)


{:.output_stream}
```
Point 0: True
Point 1: True
Point 2: True
Point 3: True

```


{:.output_data_text}
```
<Figure size 432x288 with 0 Axes>
```



![png](../../images/explore/pointpats/Minimum_bounding_circle_12_31.png)


{:.output_stream}
```
Point 0: True
Point 1: True
Point 2: True
Point 3: True
Point 4: True

```


{:.output_data_text}
```
<Figure size 432x288 with 0 Axes>
```



![png](../../images/explore/pointpats/Minimum_bounding_circle_12_34.png)


{:.output_stream}
```
Point 0: True
Point 1: True

```


{:.output_data_text}
```
<Figure size 432x288 with 0 Axes>
```



![png](../../images/explore/pointpats/Minimum_bounding_circle_12_37.png)


{:.output_stream}
```
Point 0: True
Point 1: True
Point 2: True
Point 3: True
Point 4: True

```


{:.output_data_text}
```
<Figure size 432x288 with 0 Axes>
```



![png](../../images/explore/pointpats/Minimum_bounding_circle_12_40.png)


{:.output_stream}
```
Point 0: True
Point 1: True
Point 2: True
Point 3: True
Point 4: True
Point 5: True

```


{:.output_data_text}
```
<Figure size 432x288 with 0 Axes>
```



![png](../../images/explore/pointpats/Minimum_bounding_circle_12_43.png)


{:.output_stream}
```
Point 0: True
Point 1: True
Point 2: True
Point 3: True
Point 4: True
Point 5: True
Point 6: True
Point 7: True

```


{:.output_data_text}
```
<Figure size 432x288 with 0 Axes>
```



![png](../../images/explore/pointpats/Minimum_bounding_circle_12_46.png)


{:.output_stream}
```
Point 0: True
Point 1: True
Point 2: True
Point 3: True
Point 4: True
Point 5: True

```


{:.output_data_text}
```
<Figure size 432x288 with 0 Axes>
```



![png](../../images/explore/pointpats/Minimum_bounding_circle_12_49.png)


{:.output_stream}
```
Point 0: False
Point 1: False
Point 2: False
Point 3: False
Point 4: False
Point 5: False
Point 6: True
Point 7: False
Point 8: False

```


{:.output_data_text}
```
<Figure size 432x288 with 0 Axes>
```



![png](../../images/explore/pointpats/Minimum_bounding_circle_12_52.png)


{:.output_stream}
```
Point 0: True
Point 1: True
Point 2: True

```


{:.output_data_text}
```
<Figure size 432x288 with 0 Axes>
```



![png](../../images/explore/pointpats/Minimum_bounding_circle_12_55.png)


{:.output_stream}
```
Point 0: True
Point 1: True
Point 2: True
Point 3: True
Point 4: True
Point 5: True

```


{:.output_data_text}
```
<Figure size 432x288 with 0 Axes>
```



![png](../../images/explore/pointpats/Minimum_bounding_circle_12_58.png)


{:.output_stream}
```
Point 0: True
Point 1: True
Point 2: True
Point 3: True
Point 4: True
Point 5: True
Point 6: True
Point 7: True
Point 8: False
Point 9: False
Point 10: False
Point 11: True
Point 12: True
Point 13: True
Point 14: True
Point 15: True
Point 16: True

```


{:.output_data_text}
```
<Figure size 432x288 with 0 Axes>
```



![png](../../images/explore/pointpats/Minimum_bounding_circle_12_61.png)


{:.output_stream}
```
Point 0: True
Point 1: True
Point 2: True
Point 3: True
Point 4: True
Point 5: True
Point 6: True
Point 7: True

```


{:.output_data_text}
```
<Figure size 432x288 with 0 Axes>
```



![png](../../images/explore/pointpats/Minimum_bounding_circle_12_64.png)


{:.output_stream}
```
Point 0: True
Point 1: True
Point 2: True
Point 3: True
Point 4: True
Point 5: True

```


{:.output_data_text}
```
<Figure size 432x288 with 0 Axes>
```



![png](../../images/explore/pointpats/Minimum_bounding_circle_12_67.png)


{:.output_stream}
```
Point 0: True
Point 1: True
Point 2: True
Point 3: True
Point 4: True
Point 5: True
Point 6: True
Point 7: True
Point 8: True
Point 9: True
Point 10: True
Point 11: True

```


{:.output_data_text}
```
<Figure size 432x288 with 0 Axes>
```



![png](../../images/explore/pointpats/Minimum_bounding_circle_12_70.png)


{:.output_stream}
```
Point 0: True
Point 1: True
Point 2: True
Point 3: True
Point 4: True
Point 5: True
Point 6: True
Point 7: True
Point 8: True
Point 9: True

```


{:.output_data_text}
```
<Figure size 432x288 with 0 Axes>
```



![png](../../images/explore/pointpats/Minimum_bounding_circle_12_73.png)


{:.output_stream}
```
Point 0: True
Point 1: True
Point 2: True
Point 3: True

```


{:.output_data_text}
```
<Figure size 432x288 with 0 Axes>
```



![png](../../images/explore/pointpats/Minimum_bounding_circle_12_76.png)


{:.output_stream}
```
Point 0: True
Point 1: True
Point 2: True
Point 3: True

```


{:.output_data_text}
```
<Figure size 432x288 with 0 Axes>
```



![png](../../images/explore/pointpats/Minimum_bounding_circle_12_79.png)


{:.output_stream}
```
Point 0: True
Point 1: True
Point 2: True
Point 3: True
Point 4: True
Point 5: True
Point 6: True
Point 7: True
Point 8: True
Point 9: True

```


{:.output_data_text}
```
<Figure size 432x288 with 0 Axes>
```



![png](../../images/explore/pointpats/Minimum_bounding_circle_12_82.png)


{:.output_stream}
```
Point 0: True
Point 1: True
Point 2: True

```


{:.output_data_text}
```
<Figure size 432x288 with 0 Axes>
```



![png](../../images/explore/pointpats/Minimum_bounding_circle_12_85.png)


{:.output_stream}
```
Point 0: True
Point 1: True
Point 2: True

```


{:.output_data_text}
```
<Figure size 432x288 with 0 Axes>
```



![png](../../images/explore/pointpats/Minimum_bounding_circle_12_88.png)


{:.output_stream}
```
Point 0: True
Point 1: True
Point 2: True
Point 3: True
Point 4: True
Point 5: True
Point 6: True

```


{:.output_data_text}
```
<Figure size 432x288 with 0 Axes>
```



![png](../../images/explore/pointpats/Minimum_bounding_circle_12_91.png)


{:.output_stream}
```
Point 0: True
Point 1: True
Point 2: True
Point 3: True
Point 4: True

```


{:.output_data_text}
```
<Figure size 432x288 with 0 Axes>
```



![png](../../images/explore/pointpats/Minimum_bounding_circle_12_94.png)


{:.output_stream}
```
Point 0: True
Point 1: True
Point 2: True
Point 3: True
Point 4: True
Point 5: True
Point 6: True
Point 7: True

```


{:.output_data_text}
```
<Figure size 432x288 with 0 Axes>
```



![png](../../images/explore/pointpats/Minimum_bounding_circle_12_97.png)


{:.output_stream}
```
Point 0: True
Point 1: True
Point 2: True
Point 3: True
Point 4: True
Point 5: True
Point 6: True
Point 7: True
Point 8: True

```


{:.output_data_text}
```
<Figure size 432x288 with 0 Axes>
```



![png](../../images/explore/pointpats/Minimum_bounding_circle_12_100.png)


{:.output_stream}
```
Point 0: True
Point 1: True
Point 2: True
Point 3: True
Point 4: True
Point 5: True
Point 6: True
Point 7: True
Point 8: True

```


{:.output_data_text}
```
<Figure size 432x288 with 0 Axes>
```



![png](../../images/explore/pointpats/Minimum_bounding_circle_12_103.png)


{:.output_stream}
```
Point 0: True
Point 1: True
Point 2: True
Point 3: True
Point 4: True

```


{:.output_data_text}
```
<Figure size 432x288 with 0 Axes>
```



![png](../../images/explore/pointpats/Minimum_bounding_circle_12_106.png)


{:.output_stream}
```
Point 0: True
Point 1: True
Point 2: True
Point 3: True
Point 4: True

```


{:.output_data_text}
```
<Figure size 432x288 with 0 Axes>
```



![png](../../images/explore/pointpats/Minimum_bounding_circle_12_109.png)


{:.output_stream}
```
Point 0: True
Point 1: True
Point 2: True
Point 3: True

```


{:.output_data_text}
```
<Figure size 432x288 with 0 Axes>
```



![png](../../images/explore/pointpats/Minimum_bounding_circle_12_112.png)


{:.output_stream}
```
Point 0: True
Point 1: True

```


{:.output_data_text}
```
<Figure size 432x288 with 0 Axes>
```



![png](../../images/explore/pointpats/Minimum_bounding_circle_12_115.png)


{:.output_stream}
```
Point 0: True
Point 1: True
Point 2: True
Point 3: True
Point 4: True
Point 5: True
Point 6: True
Point 7: True
Point 8: True
Point 9: True

```


{:.output_data_text}
```
<Figure size 432x288 with 0 Axes>
```



![png](../../images/explore/pointpats/Minimum_bounding_circle_12_118.png)


{:.output_stream}
```
Point 0: True
Point 1: True
Point 2: True
Point 3: True
Point 4: True
Point 5: True
Point 6: True
Point 7: True
Point 8: True
Point 9: True
Point 10: True

```


{:.output_data_text}
```
<Figure size 432x288 with 0 Axes>
```



![png](../../images/explore/pointpats/Minimum_bounding_circle_12_121.png)


{:.output_stream}
```
Point 0: True
Point 1: True
Point 2: True
Point 3: True
Point 4: True
Point 5: True
Point 6: True

```


{:.output_data_text}
```
<Figure size 432x288 with 0 Axes>
```



![png](../../images/explore/pointpats/Minimum_bounding_circle_12_124.png)


{:.output_stream}
```
Point 0: True
Point 1: True
Point 2: True

```


{:.output_data_text}
```
<Figure size 432x288 with 0 Axes>
```



![png](../../images/explore/pointpats/Minimum_bounding_circle_12_127.png)


{:.output_stream}
```
Point 0: True
Point 1: True
Point 2: True
Point 3: True

```


{:.output_data_text}
```
<Figure size 432x288 with 0 Axes>
```



![png](../../images/explore/pointpats/Minimum_bounding_circle_12_130.png)


{:.output_stream}
```
Point 0: True
Point 1: True
Point 2: True
Point 3: True
Point 4: True
Point 5: True
Point 6: True
Point 7: True

```


{:.output_data_text}
```
<Figure size 432x288 with 0 Axes>
```



![png](../../images/explore/pointpats/Minimum_bounding_circle_12_133.png)


{:.output_stream}
```
Point 0: False
Point 1: True
Point 2: True
Point 3: True
Point 4: False

```


{:.output_data_text}
```
<Figure size 432x288 with 0 Axes>
```



![png](../../images/explore/pointpats/Minimum_bounding_circle_12_136.png)


{:.output_stream}
```
Point 0: True
Point 1: True
Point 2: True
Point 3: True
Point 4: True
Point 5: True
Point 6: True
Point 7: True

```


{:.output_data_text}
```
<Figure size 432x288 with 0 Axes>
```



![png](../../images/explore/pointpats/Minimum_bounding_circle_12_139.png)


{:.output_stream}
```
Point 0: True
Point 1: True
Point 2: True
Point 3: True
Point 4: True
Point 5: True
Point 6: True
Point 7: True
Point 8: True
Point 9: True

```


{:.output_data_text}
```
<Figure size 432x288 with 0 Axes>
```



![png](../../images/explore/pointpats/Minimum_bounding_circle_12_142.png)


{:.output_stream}
```
Point 0: True
Point 1: True
Point 2: True
Point 3: True
Point 4: True
Point 5: True

```


{:.output_data_text}
```
<Figure size 432x288 with 0 Axes>
```



![png](../../images/explore/pointpats/Minimum_bounding_circle_12_145.png)



{:.output_data_text}
```
<Figure size 432x288 with 0 Axes>
```




{:.input_area}
```python
pointpats.hull(chains[8])
```





{:.output_data_text}
```
array([[ 9.33329678, 13.27241993],
       [ 9.12427711, 12.63424015],
       [ 9.3860054 , 12.59624004],
       [ 9.47149754, 12.5957098 ],
       [ 9.55582809, 12.59519005],
       [ 9.72367477, 12.59519958],
       [10.01543999, 12.72404957],
       [10.09543037, 12.87689972],
       [10.09350967, 12.90021992],
       [10.08250999, 13.03376961],
       [10.02766991, 13.29854012],
       [ 9.67700958, 13.29658985]])
```





{:.input_area}
```python
plt.plot(*pointpats.hull(chains[8]).T.tolist())
plt.plot(*pointpats.hull(chains[8])[5].T.tolist(), markerfacecolor='k', marker='o')
plt.plot(*pointpats.hull(chains[8])[6].T.tolist(), markerfacecolor='k', marker='o')
plt.plot(*pointpats.hull(chains[8])[7].T.tolist(), markerfacecolor='k', marker='o')
```





{:.output_data_text}
```
[<matplotlib.lines.Line2D at 0x1b2456d710>]
```




![png](../../images/explore/pointpats/Minimum_bounding_circle_14_1.png)




{:.input_area}
```python
pointpats._circle(chains[8][-5], chains[8][-4], chains[8][-3])
```





{:.output_data_text}
```
(0.914822771306765, (8.333136366132898, 13.026633376705332))
```



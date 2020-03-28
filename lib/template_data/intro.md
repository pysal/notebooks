# `PySAL` Notebooks Book

This is a compilation of official notebooks demonstrating the functionality of `PySAL`, the
Python Spatial Analysis library.

* * *

# Introduction

The PySAL project began began life a decade ago as a collaboration between Serge Rey and
Luc Anslin as a way to coalesce their research efforts on spatial econometrics and
spatio-temporal dynamics.
Over the last 10 years, the library has grown considerably, welcoming new developers to
the team, supporting several doctoral dissertations, and including functions to facilitate
a much broader set of spatial data science applications than envisioned originally at the
outset. For that reason, PySAL has taken a new form and grown into a new modular structure
as it has matured, permitting greater flexibility for both users and developers.
Unfortunately, that flexibility comes at a cost, since it can be difficult to discover and
understand all the capabilities that exists within the PySAL ecosystem, and for that
reason we’ve decided to collect a wide variety of example notebooks, drawn from each of
the modules in the PySAL ecosystem, and combined them into this jupyterbook.
We hope this decision will help elucidate everything PySAL can do—and maybe even inspire
some new developments we have yet to discover.
This is an ongoing project, and it will evolve both on its own, and with the constituent
packages and notebooks that form its substance.
We hope you will find it useful.

# PySAL

The original design of PySAL was to have a single monolithic library with subcomponents
that addressed different types of spatial analysis.
This facilitated the easy installation of the package for end-users.
Another guiding principle to minimize the complications of the install was the fairly
restrictive use of dependencies.
Over time we have come to recognize that the single monolithic architecture of the
library, while easing installation, had a number of unintended side effects on the
developers. Many of the features in the library were buried deep in lower level packages
and the monolithic structure hindered the discoverability of those packages.
This meant that the developers of those packages were not getting the recognition they
deserved, which is particularly important in an academic environment where the time
dedicated to making these contributions was essentially ignored in tenure and promotion
cases. Moreover, the limited discoverability also impacted end users who were not aware of
the functionality.

We recently decided to re-factor the library to address these two limitations.
The refactoring is recasting PySAL as a meta-package that brings together a federation of
spatial analytical modules, and carries along several advantages.
Users who may want to focus on, say, spatial econometrics may have no need for all of
PySAL, so now they can install `spreg` as its own package.
The refactoring also increases discoverability as `spreg` is its own active stand-alone package,
and is no longer buried deep inside PySAL. With this increased visibility, adoption
increases, leading to greater recognition for the developers as well as more feedback from
users and, ultimately, improvements to the package.
From a development perspective, the refactoring also increases the speed at which we are
able to release new functionality in the individual packages.
The other benefit of this model is that end users who still want everything in the PySAL
federation can install the meta-package and should notice no difference from their use of
the monolithic PySAL package.
In other words, we support two different ways for users to interface with the library:
users can get everything in one shot through the meta-package, or they could go the a la
carte route and pick specific packages in mix and match them to support a specialized
workflow. 

# Organization

The reorganization of PySAL is along four groups of packages that address the certain type
of spatial analysis:

1. lib
2. explore
3. viz 
4. model

## Core Data Structures

`libpysal` is the core package and it is here where we handle file-io, spatial weights, and
geoprocessing.
All the other packages in the PySAL ecosystem import where they are dependent upon lib.

## Exploration

Under the explore family of packages we have `esda`, which supports exploratory spatial data
analysis in the form of global and local tests for spatial autocorrelation as well as
rates smoothing. `giddy`
for geospatial distribution dynamics implements classic Markov and spatial Markov models
for longitudinal spatial data along with measures for spatial income mobility and other
types of intra-distributional change.
In addition, explore includes `spaghetti`, which is for spatial analysis on networks, and `pointpats`, which
supports spatial analysis of planar point patterns.
The newest additon to the explore family is `segregation`, which facilitates the spatial and temporal
analysis of urban segregation patterns and includes inferential and decompositional
frameworks.

## Visualization

The viz group of packages includes `splot`, a new package providing common a common application
programming interface (API) for lightweight visualization functionality on top of the
other PySAL packages. `mapclassify`
is a second component of the visualization layer that implements a large number of
classification schemes for choropleth mapping, and also supports updating and streaming
type data. Rounding out the viz group is `legendgram`, a novel approach to developing and
representing the classification underlying a choropleth map.

## Modeling

The third cluster of packages fall under the model layer.
The workhorse here is `spreg`, which implements modern methods of spatial econometrics and has
been a key part of PySAL from day one.
As part of the refactoring we have seen much growth in the model space, as new packages
that have been added include `mgwr` implementing multiscale geographically weighted regression;
`spint` for estimating spatial interaction models, such as the production- or
consumption-constrained gravity models; `spvcm`
for spatially correlated multilevel models;
and `spglm`, a package for fitting sparse general linear models (GLM).

* * *

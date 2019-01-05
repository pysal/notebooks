---
redirect_from:
  - "/model/spvcm/intro"
title: 'spvcm'
prev_page:
  url: /viz/splot/mapping_vba
  title: 'mapping_vba'
next_page:
  url: /model/spvcm/spatially-varying-coefficients
  title: 'spatially-varying-coefficients'
comment: "***PROGRAMMATICALLY GENERATED, DO NOT EDIT. SEE ORIGINAL FILES IN /content***"
---
---
title: '`spvcm`: Gibbs sampling for spatially-correlated variance-components'
---

[![image](https://travis-ci.org/pysal/spvcm.svg?branch=master)](https://travis-ci.org/pysal/spvcm)

[![image](https://zenodo.org/badge/79168765.svg)](https://zenodo.org/badge/latestdoi/79168765)

This is a package to estimate spatially-correlated variance components
models/varying intercept models. In addition to a general toolkit to
conduct Gibbs sampling in Python, the package also provides an interface
to PyMC3 and CODA. For a complete overview, consult the
[walkthrough](https://github.com/ljwolf/spvcm/blob/master/spvcm/examples/using_the_sampler.ipynb).

*author*: Levi John Wolf

*email*: `levi.john.wolf@gmail.com`

*institution*: University of Bristol & University of Chicago Center for
Spatial Data Science

*preprint*: on the [Open Science Framework](https://osf.io/ks6t3/)

Installation
============

This package works best in Python 3.5, but unittests pass in Python 2.7
as well. Only Python 3.5+ is officially supported.

To install, first install the Anaconda Python
[Distribution](https://https://www.continuum.io/downloads) from
Continuum [Analytics](https://continuum.io). Installation of the package
has been tested in Windows (10, 8, 7) Mac OSX (10.8+) and Linux using
Anaconda 4.2.0, with Python version 3.5.

Once Anaconda is installed, `spvcm` can be installed using `pip`, the
Python Package Manager.

`pip install spvcm`

To install this from source, one can also navigate to the source
directory and use:

`pip install ./`

which will install the package from the target source directory.

Usage
=====

To use the package, start up a Python interpreter and run:
`import spvcm.api as spvcm`

Then, many differnet variance components model specificaions are
available in:

`spvcm.both` `spvcm.upper` `spvcm.lower`

For more thorough directions, consult the Jupyter Notebook,
`using the sampler.ipynb`, which is provided in the `spvcm/examples`
directory.

Citation
========

Levi John Wolf. (2016). [Gibbs Sampling for a class of
spatially-correlated variance components models]{.title-ref}. University
of Chicago Center for Spatial Data Science Technical Report.

[![Latest Version](https://pypip.in/version/boadata/badge.svg)](https://pypi.python.org/pypi/boadata/)

boadata
=======

(B)rowser (O)f (A)rbitrary Data - a Python browser of data. 
The goal is to create a simple tool for scientists / data miners
to browse and plot various data sources in one simple environment.

Requirements
------------
* PyQt4
* pandas
* six
* blinker
* h5py (optional)
* sqlalchemy (optional)
* pyqtgraph (optional)
* matplotlib (optional)
* xlrd (optional, for reading Excel files)
* bokeh (optional)

None of these but PyQt4 should be required in the future.
But honestly, a full distribution is highly recommended.

* Python 2.7 / 3.4+

Status
------
* in (slow) development
* version 0.2.9 is (perhaps) the last in 0.2 series
* version 0.3 will see a major API redesign

Supported formats and sources
-----------------------------
* File system tree
* HDF5
* CSV (basic)
* XLS (very basic)
* SQL based on SqlAlchemy (very basic)
* TSV-like field data

Supported views
---------
* Table
* Line plot
* Properties
* Text view
* Field view (very basic)


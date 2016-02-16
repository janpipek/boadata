boadata
=======

(B)rowser (O)f (A)rbitrary Data - a Python browser of data. 
The goal is to create a simple tool for scientists / data miners
to browse and plot various data sources in one simple environment.

Requirements
------------
* PyQt4
* odo
* pandas
* numpy
* six
* blinker
* h5py (optional)
* sqlalchemy (optional)
* pyqtgraph (optional - table support)
* matplotlib (optional)
* pandas_profiling (optional - dataframe summaries)

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
* In principle many odo sources.

Supported views
---------
* Table
* Line plot
* Properties
* Text view
* Field view (very basic)


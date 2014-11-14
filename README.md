boadata
=======

(B)rowser (O)f (A)rbitrary Data - a Python browser of data. 
The goal is to create a simple tool for scientists / data miners
to browse and plot various data sources in one simple environment.

Requirements
------------
* PyQt4
* pandas
* blinker
* h5py (optional)
* sqlalchemy (optional)
* pyqtgraph (optional)
* matplotlib (optional)
* xlrd (optional, for reading Excel files)

None of these but PyQt4 should be required in the future.
But honestly, a full distribution is highly recommended.

* Python 2.7 (Python 3 planned)

Status
------
* in (slow) development

Supported formats and sources
-----------------------------
* File system tree
* HDF5
* CSV (basic)
* XLS (very basic)
* SQL based on SqlAlchemy (very basic)

Supported views
---------
* Table
* Line plot


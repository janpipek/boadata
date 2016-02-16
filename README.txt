boadata
=======

(B)rowser (O)f (A)rbitrary Data - a Python browser of data. 
The goal is to create a simple tool for scientists / data miners
to browse and plot various data sources in one simple environment.

It's a library, as well as a set of tools.

Concepts
--------
* uri - boadata tries to support odo URIs
* data object - wrapper around basic data types (a.k.a odo.resource but with wrapper)
* data tree - browseable that can contain nodes (some of the nodes can be data objects)
* data conversion - between different object types
* view - visual representation of a data objects

Executables
------------
* `boadescribe <uri>` - show basic info about a data object (in command-line)
* `boatree <uri>` - list nodes in a data tree
* `boaplot <uri> <colx> <coly>` - scatter plot of two columns
* `boahist <uri> <col>` - histogram of a column
* `boadata [<uri>]` - full gui with a tree
* `boatable <uri>` - show tabular representation of a dataobject

Status
------
* in (slow) development

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

Supported formats and sources
-----------------------------
* File system tree
* HDF5
* CSV
* SQL based on SqlAlchemy (sqlite supported)
* pydataset datasets

Supported views
---------
* Table
* Histogram
* Scatter plot
* Text view
* Summary (from pandas_profiling)


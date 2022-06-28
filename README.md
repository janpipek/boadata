boadata
=======

(B)rowser (O)f (A)rbitrary Data - a Python browser of data. 
The goal is to create a simple tool for scientists / data miners
to browse and plot various data sources in one simple environment.

It's a library, as well as a set of tools.

Most focus is placed on table-like pandas-based objects.

Concepts
--------
* uri - boadata tries to support odo URIs
* data object - wrapper around basic data types (a.k.a odo.resource but with wrapper)
* data tree - browseable that can contain nodes (some of the nodes can be data objects)
* data conversion - between different object types
* view - visual representation of a data objects

Executables
------------
Run `command --help` to see full list of options

* `boa` - 
* `boa-describe <uri>` - show basic info about a data object (in command-line)
* `boa-tree <uri>` - list nodes in a data tree
* `boa-cat <uri>` - print tabular representation of a dataobject (command-line)
* `boa-convert <from+> <to>` - convert one data source into another

Status
------
* in (slow) development

Requirements
------------
* PyQt4 (to become optional / replaceable with PySide/PyQt5)
* pandas
* numpy
* numexpr
* click
* tabulate
* blinker (perhaps to be removed)
* h5py (optional)
* sqlalchemy (optional)
* pyqtgraph (to be removed)
* matplotlib (to become optional)
* bokeh (to become optional instead of matplotlib)
* seaborn
* pandas_profiling (optional - dataframe summaries)
* datadotworld (optional - for their datasets)

* Python 3.6+

Supported formats and sources
-----------------------------
* File system tree
* HDF5
* CSV (including web links)
* SQL based on SqlAlchemy (sqlite supported)
* pydataset datasets
* seaborn datasets
* MATLAB .fig files
* data.world datasets/tables (that can be imported pandas dataframes)

Supported GUI views
-------------------
* Table
* Histogram
* Scatter / line plot
* Text view
* Summary (from pandas_profiling)


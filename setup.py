#!/usr/bin/env python
from setuptools import setup, find_packages
import itertools
from boadata import __version__

options = dict(
    name='boadata',
    version=__version__,
    packages=find_packages(),
    license='MIT',
    description='(B)rowser (O)f (A)rbitrary Data - a Python GUI browser of data.',
    long_description=open('README.md').read(),
    author='Jan Pipek',
    author_email='jan.pipek@gmail.com',
    url='https://github.com/janpipek/boadata',
    python_requires='>=3.6',
    install_requires = ['clevercsv', 'numpy', 'pandas', 'blinker', 'sqlalchemy', 'numexpr', 'click', 'xarray', 'scipy',
        'matplotlib', 'orange3', 'seaborn', 'tabulate', 'physt'],
    extras_require = {
        'matlab' : ['pydons'],
        'h5py' : ['h5py'],
        'pydataset' : ['pydataset'],
        'feather' : ['feather'],
    },
    entry_points = {
        'console_scripts' : [
            'boaconvert = boadata.commands.boaconvert:run_app',
            'boadata = boadata.commands.boadata:run_app',
            'boadescribe = boadata.commands.boadescribe:run_app',
            'boatable = boadata.commands.boatable:run_app',
            'boaview = boadata.commands.boaview:run_app',
            'boatree = boadata.commands.boatree:run_app',
            'boaplot = boadata.commands.boaplot:run_app',
            'boahist = boadata.commands.boahist:run_app',
            'boacat = boadata.commands.boacat:run_app'
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ]
)

extras = options['extras_require']
extras['all'] = list(set(itertools.chain.from_iterable(extras.values())))
setup(**options)

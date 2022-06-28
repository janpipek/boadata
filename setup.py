#!/usr/bin/env python
from setuptools import setup, find_packages
import itertools
from boadata import __version__

options = dict(
    name='boadata',
    version=__version__,
    packages=find_packages(),
    license='MIT',
    description='(B)rother (O)f (A)rbitrary Data - Python CLI tools for data.',
    long_description=open('README.md').read(),
    author='Jan Pipek',
    author_email='jan.pipek@gmail.com',
    url='https://github.com/janpipek/boadata',
    python_requires='>=3.8',
    install_requires = ['clevercsv', 'numpy', 'pandas', 'blinker', 'sqlalchemy', 'numexpr', 'click', 'xarray', 'scipy',
        'matplotlib', 'seaborn', 'tabulate', 'physt', 'typer'],
    extras_require = {
        'matlab' : ['pydons'],
        'h5py' : ['h5py'],
        'pydataset' : ['pydataset'],
        'feather': ['feather'],
        'excel': ['openpyxl', 'xlrd']
    },
    entry_points = {
        'console_scripts' : [
            'boa = boadata.commands:run_app',

            # TODO: Remove the following?
            'boa-convert = boadata.commands.boaconvert:run_app',
            'boa-describe = boadata.commands.boadescribe:run_app',
            'boa-tree = boadata.commands.boatree:run_app',
            'boa-cat = boadata.commands.boacat:run_app'
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
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

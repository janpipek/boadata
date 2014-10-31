#!/usr/bin/env python
from setuptools import setup, find_packages
import itertools

options = dict(
    name='boadata',
    version='0.2.3',
    packages=find_packages(),
    license='MIT',
    description='(B)rowser (O)f (A)rbitrary Data - a Python GUI browser of data.',
    long_description=open('README.md').read(),
    author='Jan Pipek',
    author_email='jan.pipek@gmail.com',
    url='https://github.com/janpipek/boadata',
    install_requires = [ 'numpy', 'pandas', 'blinker' ],
    extras_require = {
        'sql' : ['sqlalchemy'],
        'pyqtgraph' : ['pyqtgraph'],
        'matplotlib' : ['matplotlib']
        'hdf5' : ['h5py']
    },
    entry_points = {
        'console_scripts' : [
            'boadata = boadata:run_app'
        ]
    }
)

extras = options['extras_require']
extras['full'] = list(set(itertools.chain.from_iterable(extras.values())))
setup(**options)
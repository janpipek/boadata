#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='boadata',
    version='0.2',
    packages=find_packages(),
    license='MIT',
    description='(B)rowser (O)f (A)rbitrary Data - a Python GUI browser of data.',
    long_description=open('README.md').read(),
    author='Jan Pipek',
    author_email='jan.pipek@gmail.com',
    url='https://github.com/janpipek/boadata',
    install_requires = [ 'numpy', 'pandas', 'blinker' ],
    entry_points = {
        'console_scripts' : [
            'boadata = boadata:run_app'
        ]
    }
)
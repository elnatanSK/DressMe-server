#!/usr/bin/env python

from distutils.core import setup
from setuptools import find_packages

setup(
        name='DressMe',
        version='1',
        description='Backend for the DressMe app',
        author='DressMe',
        author_email='mgaut72+dressme@gmail.com',
        url='mgaut72.github.io',
        packages=find_packages(),
        install_requires=['Flask>=0.10.1',
                          'Flask-RESTful>=0.2.11',
                          ]
        )

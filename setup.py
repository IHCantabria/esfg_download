#!/usr/bin/env python

from setuptools import setup

setup(name='ESFG',
      version='0.0.1',
      description='🌎 Download ESFG data and export.',
      author='Salvador Navas',
      author_email='navass@unican.es',
      packages=["ESFG"],
      package_data={'': ['wget-plantilla-ESGF.sh']},
      include_package_data = True,
      install_requires=[
          'numpy',
          'pandas',
          'scipy',
          'esgf-pyclient',
          'xarray',
          'tqdm',
          'netCDF4',
      ]
     )

#!/usr/bin/env python

import sys
from setuptools import setup, find_packages


sys.path.append('./src')
sys.path.append('./test')

classifiers = [
    "Development Status :: 3 - Alpha",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 2.7",
    "Intended Audience :: Developers",
    "Topic :: Scientific/Engineering :: GIS",
]

setup(
    name='py-geohex3',
    description='geohex v3.2 python implementation',
    url='https://github.com/uncovertruth/py-geohex3',
    version='0.0.2',
    author='UNCOVER TRUTH Inc.',
    author_email='info@uncovertruth.jp',
    test_suite='geohex_test.suite',
    classifiers=classifiers,
    platforms='any',
    keywords='gis geohex',
    packages=find_packages("src"),
    package_dir={"": "src"}
)

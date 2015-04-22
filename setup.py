#!/usr/bin/env python

import sys
from setuptools import setup, find_packages

sys.path.append('./src')
sys.path.append('./test')


setup(name='py-geohex3',
      version='0.0.1',
      description='geohex v3 python implementation',
      author='UNCOVER TRUTH Inc.',
      author_email='info@uncovertruth.jp',
      test_suite = 'geohex_test.suite',
      packages=find_packages("src"),
      package_dir={"": "src"})


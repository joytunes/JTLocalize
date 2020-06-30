#!/usr/bin/env python

import setuptools
from distutils.core import setup

setup(name='jtlocalize',
      version='1.0.0',
      description='iOS localization framework',
      author='JoyTunes',
      author_email='info@joytunes.com',
      url='https://github.com/joytunes/JTLocalize/',
      packages=['jtlocalize','jtlocalize.core', 'jtlocalize.configuration'],
      scripts=['jtlocalize/bin/jtlocalize'],
      license='MIT',
     )

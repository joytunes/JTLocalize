#!/usr/bin/env python

from distutils.core import setup

setup(name='jtlocalize',
      version='0.1.3',
      description='iOS localization framework',
      author='JoyTunes',
      author_email='info@joytunes.com',
      url='https://github.com/joytunes/JTLocalize/',
      packages=['jtlocalize','jtlocalize.core', 'jtlocalize.configuration'],
      scripts=['jtlocalize/bin/jtlocalize'],
      license='MIT',
     )

#!/usr/bin/env python

import os

from setuptools import setup, find_packages


here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'Readme.md')).read()

requires = [
    'requests>=2.7',
    'django>=1.9.1'
]

includes = (
    'wentong',
)

setup(
    name="normandy-pi-plugun-camera-wentong",
    version='0.0.1',
    packages=find_packages(),
    install_requires=requires,
    description='normandy-pi-plugun-camera-wentong',
    long_description=README,
    author="xumingze",
    license="BSD",
    url="https://github.com/xumingze2014/normandy-pi-plugun-camera-wentong"
)

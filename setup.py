#!/usr/bin/env python
# -*- coding: utf-8 -*-
import codecs
import sys
import os

from setuptools import setup, find_packages, Command

import mature_optimization

long_description = codecs.open("README.rst", "r", "utf-8").read()

setup(
    name='django-mature-optmization',
    version=mature_optimization.__version__,
    description=mature_optimization.__doc__,
    author=mature_optimization.__author__,
    author_email=mature_optimization.__contact__,
    url=mature_optimization.__homepage__,
    platforms=["any"],
    license="BSD",
    packages=find_packages(),
    scripts=[],
    zip_safe=False,
    install_requires=['django>=1.2'],
    cmdclass = {},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Framework :: Django",
        "Programming Language :: Python",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    long_description=long_description,
)

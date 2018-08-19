#!/usr/bin/env python
# -*- coding: utf-8 -*-
import io
import re

from setuptools import (find_packages, setup)

with io.open('README.md', 'rt', encoding='utf8') as fp:
    readme = fp.read()

with io.open('mujson/__init__.py', 'rt', encoding='utf8') as fp:
    version = re.search(r'__version__ = \'(.*?)\'', fp.read()).group(1)

setup(
    name='mujson',
    version=version,
    url='https://github.com/mattgiles/mujson',
    license='MIT',
    author='Matt Giles',
    author_email='matt.s.giles@gmail.com',
    description='Use the fastest JSON functions available at import time.',
    long_description=readme,
    packages=['mujson'],
    include_package_data=False,
    zip_safe=False,
    platforms='any',
    keywords='json',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ]
)

#!/usr/bin/env python
# encoding: utf-8
from setuptools import setup
import os

ROOT = os.path.dirname(os.path.abspath(__file__))

setup(
    name='rgc',
    version='0.1',
    url="https://github.com/sievetech/rgc",
    license="3-BSD",
    description='A tool to remove files from Rackspace in an efficient manner.',
    author="Dalton Barreto",
    author_email="dalton.matos@sieve.com.br",
    long_description=open(os.path.join(ROOT, 'README.md')).read(),
    packages=['rgc'],
    entry_points={
        'console_scripts': [
            'rgc = rgc.main:main',
        ]
    },
    install_requires=['python-modargs', 'python-cloudfiles', "clint"],
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Application Frameworks"
    ])

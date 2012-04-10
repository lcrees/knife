#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''setup for chainsaw'''

from os import getcwd
from os.path import join
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

install_requires = list(l.strip() for l in open(
    join(getcwd(), 'requirements.txt'), 'r',
).readlines())

setup(
    name='chainsaw',
    version='0.5.0',
    description='Things go in. Things get chainsawed. Things come out.',
    long_description=open(join(getcwd(), 'README.rst'), 'r').read(),
    keywords='pipe flow ETL iterator functional fluent chaining',
    license='BSD',
    author='L. C. Rees',
    author_email='lcrees@gmail.com',
    url='https://bitbucket.org/lcrees/chainsaw',
    packages=['chainsaw'],
    test_suite='chainsaw.tests',
    zip_safe=False,
    install_requires=install_requires,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: Utilities',
    ],
)

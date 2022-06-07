#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import io
import sys
from setuptools import setup, find_packages

VERSION = (0, 1, 1)


PATH_BASE = os.path.dirname(__file__)


def get_readme():
    # This will return README (including those with Unicode symbols).
    with io.open(os.path.join(PATH_BASE, 'README.rst')) as f:
        return f.read()


setup(
    name='pytest-race',
    version='.'.join(map(str, VERSION)),
    url='https://github.com/idlesign/pytest-race',

    description='Race conditions tester for pytest',
    long_description=get_readme(),
    license='BSD 3-Clause License',

    author='Igor `idle sign` Starikov',
    author_email='idlesign@yandex.ru',

    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    zip_safe=False,

    install_requires=[
        'pytest>=2.9.0'
    ],
    setup_requires=[] + (['pytest-runner'] if 'test' in sys.argv else []) + [],

    entry_points={
        'pytest11': [
            'race = race.entry',
        ],
    },

    test_suite='tests',

    tests_require=[
        'pytest'
    ],

    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Pytest',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: BSD License',
    ],

)

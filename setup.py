#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import io
import sys
from setuptools import setup


VERSION = (0, 1, 0)


PATH_BASE = os.path.dirname(__file__)
PATH_BIN = os.path.join(PATH_BASE, 'bin')

PYTEST_RUNNER = ['pytest-runner'] if 'test' in sys.argv else []


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

    install_requires=['pytest>=2.9.0'],
    setup_requires=[] + PYTEST_RUNNER,
    tests_require=['pytest'],

    py_modules=['pytest_race'],

    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Pytest',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: BSD License',
    ],
    entry_points={
        'pytest11': [
            'race = pytest_race',
        ],
    },
)

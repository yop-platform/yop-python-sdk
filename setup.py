# -*- coding: utf-8 -*-
#!/usr/bin/env python

# Copyright Yeepay.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0.

from setuptools import find_packages, setup

with open("README.rst", "r") as f:
    long_description = f.read()

setup(
    name='yop-python-sdk',
    version='3.3.7',
    description='YOP SDK based on the YOP Common Runtime',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='YOP SDK Common Runtime Team',
    author_email='yop@yeepay.com',
    url='https://github.com/yop-platform/yop-python-sdk',
    license='Apache License',
    platforms=["all"],
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Natural Language :: Chinese (Simplified)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Libraries'
    ],
    install_requires=[
        'oss2>=2.13.1',
        'pycrypto>=2.6.1',
        'requests_toolbelt>=0.9',
    ],
    # python_requires='~=2.7,~=3.2',
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
        'pytest-html',
    ],
)

# -*- coding: utf-8 -*-

# Copyright Yeepay.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0.

from setuptools import find_packages, setup

with open("README.MD", "r") as f:
    long_description = f.read()

setup(
    name='yop-python-sdk',
    version='4.1.1',
    description='YOP SDK based on the YOP Common Runtime',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='YOP Team',
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
        'Topic :: Software Development :: Libraries'
    ],
    # 务必删除 crypto 和 pycrypto
    # pip3 uninstall crypto
    # pip3 uninstall pycrypto
    # pip3 install pycryptodome
    install_requires=[
        'future>=0.18.2',
        'pycryptodome>=3.10.1',
        'pyOpenSSL>=20.0.1',
        'python-dateutil>=2.8.1',
        'requests_toolbelt>=0.9.1',
        'simplejson>=3.17.2',
    ],
    # python_requires='~=2.7,~=3.7',
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
        'pytest-html',
    ],
)

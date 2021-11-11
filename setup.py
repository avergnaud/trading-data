# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='trading-data',
    version='0.1.0',
    description='Trade data',
    author='Adrien Vergnaud',
    author_email='a.vergnaud@gmail.com',
    url='https://github.com/avergnaud/trading-data',
    packages=find_packages(exclude=('tests'))
)


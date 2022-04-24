#!/usr/bin/python3
# setup.py
# Copyright (C) 2022 CodeWriter21

from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    long_description = readme_file.read()

DESCRIPTION = "minipyer is a code minifier python package. You can use this package to minipy your codes. =)"
VERSION = "0.1.0"

setup(
    name="minipyer",
    version=VERSION,
    url='https://github.com/MPCodeWriter21/minipyer',
    author='CodeWriter21(Mehrad Pooryoussof)',
    author_email='<CodeWriter21@gmail.com>',
    license='Apache-2.0 License',
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    keywords=['python', 'minify', 'minipy', 'minipyer', 'code'],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.10",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows"
    ]
)

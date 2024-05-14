#!/bin/bash

# Build the distribution package
python setup.py sdist bdist_wheel

# Upload the distribution package to PyPI
twine upload dist/*

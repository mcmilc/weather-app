#!/bin/sh
# Navigate to the api directory
cd /app
# Build the package
python setup.py sdist bdist_wheel
# Install the package
pip install dist/*.whl
# Clean up build artifacts
rm -rf build dist *.egg-info
#!/bin/sh
python /app/setup.py sdist bdist_wheel
# Install the package
pip install /app/dist/*.whl --force-reinstall
# Clean up build artifacts
rm -rf build /app/dist /app/*.egg-info
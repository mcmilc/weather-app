#!/bin/sh
python3 /app/share/setup.py sdist bdist_wheel
# Install the package
pip3 install /app/share/dist/*.whl --force-reinstall
# Clean up build artifacts
rm -rf /app/share/build /app/share/dist /app/share/*.egg-info
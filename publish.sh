#!/bin/bash

# Build and publish to PyPI
echo "Building package..."
python -m build

echo "Uploading to PyPI..."
python -m twine upload dist/*

echo "Done! Package published to PyPI."
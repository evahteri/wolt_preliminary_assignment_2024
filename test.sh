#!/bin/bash

echo "Running tests..."

cd src/

pytest tests/

echo "Running coverage..."

coverage run --branch -m pytest

echo "Generating coverage report..."

coverage report
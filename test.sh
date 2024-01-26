#!/bin/bash

echo "Running tests..."

pytest src/tests/

echo "Running coverage..."

coverage run --branch -m pytest src

echo "Generating coverage report..."

coverage report -m
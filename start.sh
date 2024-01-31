#!/bin/bash

echo "Installing required dependencies..."

pip install -r requirements.txt

echo "Dependencies downloaded, starting the server..."

python src/main.py
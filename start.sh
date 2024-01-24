#!/bin/bash

echo "Installing required dependencies..."

pip install -r requirements.txt

echo "Dependencies downloaded, starting the server..."

cd src/

uvicorn main:app
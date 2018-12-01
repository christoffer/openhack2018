#!/bin/bash

echo "Installing Python requirements..."
pip install -r requirements.txt
echo "Installing NLTK data (this will take a while)..."
python -m nltk.downloader all
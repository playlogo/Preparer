#!/bin/bash

# Fix led permissions
sudo chmod 777 /dev/mem

# Venv
echo "Creating venv in .venv"
python3 -m venv .venv
source .venv/bin/activate

# Pip
echo "Installing packages"
pip install -r requirements.txt
pip install -e ../adapter

echo "Done installing!"

# Run
echo "Starting edge"
python src/main.py
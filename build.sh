#!/usr/bin/env bash

echo "Install requirements"
pip install -r requirements.txt
echo "Building packages"
pyinstaller --clean -F pyBankRapport.py
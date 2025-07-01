#!/bin/bash

source .venv/bin/activate
pyinstaller src/app/main.py --onefile --name hider --add-data "binaries/:binaries/"


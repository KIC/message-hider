#!/bin/bash

source .venv/bin/activate
pip install -r dev-requirements.txt
pyinstaller src/app/main.py --onefile --name hider --add-data "binaries/:binaries/"

# smoke test
./dist/hider audio hide --secret "geheimnins" -o /tmp/ src/tests/data/short.mp3 
./dist/hider audio reveil /tmp/short.mp3


#!/bin/bash

pyinstaller src/app/main.py --onefile --name hider --add-data "binaries/:binaries/"


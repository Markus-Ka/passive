#!/bin/bash

pyinstaller --onefile main.py
mv dist/main ~/customExec/passive
rm -r build
rm -r dist
echo Executable created
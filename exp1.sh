#!/bin/bash
python3 main_dock.py -e 2 -o decoys
python3 main_dock.py -e 4 -o decoys
python3 main_dock.py -e 8 -o decoys
python3 main_dock.py -e 16 -o decoys
python3 main_dock.py -e 32 -o decoys
python3 main_dock.py -e 64 -o decoys

#!/bin/bash

# Experiments on decoys
python3 main_dock.py -e 2 -o decoys
python3 main_dock.py -e 4 -o decoys
python3 main_dock.py -e 8 -o decoys
python3 main_dock.py -e 16 -o decoys
python3 main_dock.py -e 32 -o decoys
python3 main_dock.py -e 64 -o decoys

# Experiments on actives
python3 main_dock.py -d data/actives_split -e 2 -o actives
python3 main_dock.py -d data/actives_split -e 4 -o actives
python3 main_dock.py -d data/actives_split -e 8 -o actives
python3 main_dock.py -d data/actives_split -e 16 -o actives
python3 main_dock.py -d data/actives_split -e 32 -o actives
python3 main_dock.py -d data/actives_split -e 64 -o actives

#!/bin/bash
. ./venv/bin/activate
python3 focus_stack.py -6000 -6000 -6000
python3 make_hdr.py

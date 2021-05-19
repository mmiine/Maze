#!/bin/bash

python3 networking/server.py

# wait one second
sleep 1
python3 face_detector_main.py
# wait one second
sleep 1
python3 decision_main.py
# wait one second
sleep 1
python3 gui_main.py
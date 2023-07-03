#!/usr/bin/sh

echo "(1/5) Activating venv"
. venv/bin/activate

echo "(2/5) Executing automation script"
python3 main.py

echo "(3/5) Deactivating venv"
deactivate

echo "(4/5) Cleaning up processes"
kill $(ps ax | grep dbus-launch | awk '{print $1}' | head -n 1)

echo "(5/5) Finished! (Should be)"

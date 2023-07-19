#!/usr/bin/sh

xvfb-run java -Dwebdriver.chrome.driver=chromedriver/chromedriver_linux64_114-0-5735-16 -jar chromedriver/selenium-server-standalone.jar

echo "(1/5) Activating venv"
. venv/bin/activate

echo "(2/5) Executing automation script"
python3 main.py

echo "(3/5) Deactivating venv"
deactivate

echo "(4/5) Cleaning up processes"
kill $(ps ax | grep dbus-launch | awk '{print $1}' | head -n 1)

echo "(5/5) Finished! (Should be)"

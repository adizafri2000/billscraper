#!/usr/bin/sh

#xvfb-run java -Dwebdriver.chrome.driver=chromedriver/chromedriver_linux64_114-0-5735-16 -jar chromedriver/selenium-server-standalone.jar

echo "(1/6) Activating venv"
. venv/Scripts/activate

echo "(2/6) Installing dependencies from requirements.txt"
pip install -r requirements.txt

echo "(3/6) Executing automation script"
python3 main.py

#if $?!=0
#then
#  echo "Program exited with non-zero status code and failed."
#  set -e
#fi

echo "(4/6) Deactivating venv"
deactivate

echo "(5/6) Cleaning up processes"
kill $(ps ax | grep dbus-launch | awk '{print $1}' | head -n 1)

echo "(6/6) Finished! (Should be)"

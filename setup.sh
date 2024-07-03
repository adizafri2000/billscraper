#!/usr/bin/sh

sudo apt update -y && sudo apt upgrade -y

echo "(1/7) Installing Firefox..."
sudo apt install -y firefox

echo "(2/7) Installing GeckoDriver..."
GECKODRIVER_VERSION=$(curl -s https://api.github.com/repos/mozilla/geckodriver/releases/latest | grep 'tag_name' | cut -d\" -f4)
wget "https://github.com/mozilla/geckodriver/releases/download/$GECKODRIVER_VERSION/geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz"
tar -xzf geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz
sudo mv geckodriver /usr/local/bin/
rm geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz

echo "(3/7) Allow xhost (or something like that) and creating .Xauthority file ..."
sudo apt install -y x11-xserver-utils

touch ~/.Xauthority
sudo chmod 777 /etc/pam.d/su /etc/pam.d/sudo

echo "session optional pam_xauth.so" >> /etc/pam.d/su
tail -n 1 /etc/pam.d/su
echo "session optional pam_xauth.so" >> /etc/pam.d/sudo
tail -n 1 /etc/pam.d/sudo

xhost -f ~/.Xauthority +si:localuser:$USER

echo "(4/7) Installing Tkinter ..."
sudo apt-get install -y python3-tk python3-dev

echo "(5/7) Installing virtualenv for python and initializing a venv ..."
python3 -m pip install virtualenv
virtualenv venv

echo "(6/7) Activating venv and installing from requirements.txt ..."
. venv/bin/activate
python3 -m pip install -r requirements.txt

echo "(7/7) Deactivating venv ..."
deactivate

echo "Setup completed! To run the automation, execute './runner.sh'"

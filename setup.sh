#!/usr/bin/sh

sudo apt update -y && sudo apt upgrade -y

echo "(1/9) Installing Google Chrome..."
sudo curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add 
sudo bash -c "echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' >> /etc/apt/sources.list.d/google-chrome.list" 
sudo apt -y install google-chrome-stable

#echo "(2/9) Installing chromedriver v114.0.5735.16 ..."
#wget https://chromedriver.storage.googleapis.com/114.0.5735.16/chromedriver_linux64.zip
#unzip chromedriver_linux64.zip
#mv chromedriver chromedriver/chromedriver_linux64_114-0-5735-16
#sudo chown root:root chromedriver
#sudo chmod +x chromedriver

#echo "(3/9) Installing Java for Selenium Server ..."
#sudo apt install default-jdk
#
#echo "(4/9) Downloading Selenium Server v3.141.59 ..."
#wget https://selenium-release.storage.googleapis.com/3.141/selenium-server-standalone-3.141.59.jar
#mv selenium-server-standalone-3.141.59.jar chromedriver/selenium-server-standalone.jar

echo "(5/9) Allow xhost (or something like that) and creating .Xauthority file ..."
sudo apt install x11-xserver-utils

touch ~/.Xauthority
sudo chmod 777 /etc/pam.d/su /etc/pam.d/sudo

echo "session optional pam_xauth.so" >> /etc/pam.d/su
tail -n 1 /etc/pam.d/su
echo "session optional pam_xauth.so" >> /etc/pam.d/sudo
tail -n 1 /etc/pam.d/sudo

#echo "session optional pam_xauth.so" | sudo tee -a /etc/pam.d/su
#echo "session optional pam_xauth.so" | sudo tee -a /etc/pam.d/sudo
#X=$(xauth list $DISPLAY)
#sudo -- bash -c "xauth add $X && $@"
#sudo xauth add $X
xhost -f ~/.Xauthority +si:localuser:$USER

echo "(6/9) Installing Tkinter ..."
sudo apt-get install python3-tk python3-dev

echo "(7/9) Installing virtualenv for python and initialising a venv ..."
python3 -m pip install virtualenv
virtualenv venv

echo "(8/9) Activating venv and installing from requirements.txt ..."
. venv/bin/activate
python3 -m pip install -r requirements.txt

echo "(9/9) Deactivating venv ..."
deactivate

echo "Setup completed! To run the automation, execute './runner.sh'"



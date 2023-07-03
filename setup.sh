 #!/usr/bin/sh

sudo apt update -y && sudo apt upgrade -y

echo "(1/9) Installing Google Chrome..."
sudo curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add 
sudo bash -c "echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' >> /etc/apt/sources.list.d/google-chrome.list" 
sudo apt -y install google-chrome-stable

echo "(2/9) Installing chromedriver v114.0.5735.16 ..."
wget https://chromedriver.storage.googleapis.com/114.0.5735.16/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
#sudo mv chromedriver /usr/bin/chromedriver 
sudo chown root:root chromedriver 
sudo chmod +x chromedriver 

echo "(3/9) Installing Java for Selenium Server ..."
sudo apt install default-jdk

echo "(4/9) Downloading Selenium Server v3.141.59 ..."
wget https://selenium-release.storage.googleapis.com/3.141/selenium-server-standalone-3.141.59.jar 
mv selenium-server-standalone-3.141.59.jar selenium-server-standalone.jar 

echo "(5/9) Allow xhost (or something like that) and creating .Xauthority file ..."
xhost +
touch ~/.Xauthority

echo "(6/9) Installing Tkinter ..."
sudo apt-get install python3-tk python3-dev

echo "(7/9) Installing virtualenv for python and initialising a venv ..."
pip3 install virtualenv
virtualenv venv

echo "(8/9) Activating venv and installing requirements.txt ..."
. venv/bin/activate
pip install -r requirements.txt

echo "(9/9) Deactivating venv ..."
deactivate

echo "Setup completed! To run the automation, execute './runner.sh'"



# Billscraper

Headless (partly) automation script to scrape bills, calculate monthly bill (rent + utilities) and generate a text message which is later
sent to desired whatsapp recipients.

[![Dev branch build & test](https://github.com/adizafri2000/billscraper/actions/workflows/build-dev-branch.yml/badge.svg)](https://github.com/adizafri2000/billscraper/actions/workflows/build-dev-branch.yml)

## Features
1. Scrapes bills from [TNB portal](https://www.mytnb.com.my/) and [Air Selangor portal](https://crisportal.airselangor.com/?lang=en).
2. Calculates monthly bill (rent + utilities) and splits the total price among the total number of housemates.
3. Generates a whatsapp text and sends it to your whatsapp group for housemates (can even send it to just yourself, or other individual numbers).

## Requirements and supported platforms
1. Python (developed on v3.9)
2. Ubuntu 20.04 (developed on Windows machine with Ubuntu WSL)
3. A working phone number with a Whatsapp account

It is not guaranteed that the automation can run on different platforms, but it isn't guaranteed that it would not
be able to run either. If you are using an older/later python version or different Linux distro/version but it still
runs, you're good to go!

## Limitations
1. The whatsapp message sending module of the app will still open a Chrome window to send the message, hence **dependent on a display** and making the entire thing *not headless*.
3. Pywhatkit library **may not successfully send the message** sometimes. Sometimes, it opens [Whatsapp Web](https://web.whatsapp.com/), writes the message, but doesn't send it.
4. If the **HTML structure of [TNB portal](https://www.mytnb.com.my/) or [Air Selangor portal](https://crisportal.airselangor.com/?lang=en) changes** or either **websites are down**, the automation will fail. (**Seasonal web popups** that are not expected by the automation can cause it to fail too)
5. If **Pywhatkit fails**, the automation fails too. This is basically the case for all the core dependencies of the automation.

## How it Works
1. A Selenium webdriver for chrome is initialized, and will 'drive' on Google Chrome.
2. Opens [TNB portal](https://www.mytnb.com.my/) to:
   1. Login
   2. Retrieve billing details e.g. total cost, bill date etc.
3. Step 2 is repeated for [Air Selangor portal](https://crisportal.airselangor.com/?lang=en).
4. A Whatsapp text message is generated in the format of (e.g.):
```
*Bill July*

Utilities:
Elektrik = RM101.50
Air = RM34.85
Unifi = RM168.55
Credit card (Washing Machine) = RM193.17
Total utilities per person = RM498.07/5 = *RM99.61*

Sewa per person = RM1000/5 = *RM200*

Total per person = *RM299.61*
```

5. A Chrome window opens [Whatsapp Web](https://web.whatsapp.com/) to send the message generated in Step 4 to desired recipient(s).

## Setup
1. Create a .env file with the following details:

````
TNB_EMAIL=[your TNB account email]
TNB_PASSWORD=[your TNB account password]
AIR_EMAIL=[your Air Selangor account email]
AIR_PASSWORD=[your Air Selangor account password]
mynum=[your Whatsapp phone number]
ws_group_id=[your whatsapp group id]
````

Replace the placeholder details with your details. Make sure the remove the squared brackets, and leave no spaces
between the equals and your written details, e.g. `TNB_EMAIL=myemail@email.com`.

To find the ID of a whatsapp group, refer to [this](https://www.alphr.com/whatsapp-find-group/) link.

2. Run `./setup.sh` to install dependencies. (run `chmod u+x setup.sh` first if encountered permission problems)

## Execution
Run `./runner.sh` to execute the program. (run the chmod command if permission denied)

**NOTE**: You would most likely need to login to whatsapp web the first time you execute the program to link your 
whatsapp account to Ubuntu's Google Chrome.
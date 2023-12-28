# Bill Scraper

Headless automation script to scrape bills, calculate monthly bills (utilities & installments) and generate a text message which is later
sent to desired whatsapp recipients.

[![Master branch main cron job](https://github.com/adizafri2000/billscraper/actions/workflows/cron-master-main.yml/badge.svg)](https://github.com/adizafri2000/billscraper/actions/workflows/cron-master-main.yml)
[![Master branch cron job tests](https://github.com/adizafri2000/billscraper/actions/workflows/cron-master-test.yml/badge.svg)](https://github.com/adizafri2000/billscraper/actions/workflows/cron-master-test.yml)
[![Master branch build & test](https://github.com/adizafri2000/billscraper/actions/workflows/build-master.yml/badge.svg)](https://github.com/adizafri2000/billscraper/actions/workflows/build-master.yml)
[![Dev branch build & test](https://github.com/adizafri2000/billscraper/actions/workflows/build-dev-branch.yml/badge.svg?branch=dev&event=push)](https://github.com/adizafri2000/billscraper/actions/workflows/build-dev-branch.yml)

## Features
1. Scrapes bills from [TNB portal](https://www.mytnb.com.my/) and [Air Selangor portal](https://crisportal.airselangor.com/?lang=en).
2. Calculates monthly bill (utilities (rent inclusive) and installments) and splits the total price among the total number of housemates.
3. Generates a whatsapp text and sends it to your whatsapp group for housemates (can even send it to just yourself, or other individual numbers).
4. Persists all the scraped and calculated data to a remote postgresql instance.

## Requirements and supported platforms
1. Python (developed on v3.9)
2. Ubuntu 20.04 (developed on Windows machine with Ubuntu WSL)
3. A working phone number with a Whatsapp account
4. A [supabase](https://supabase.com/) account for database credentials
5. A GitHub account for GitHub Actions (optional)

It is not guaranteed that the automation can run on different platforms, but it isn't guaranteed that it would not
be able to run either. If you are using an older/later python version or different Linux distro/version but it still
runs, you're good to go!

## Limitations
1. The whatsapp message sending module of the app will still open a Chrome window to send the message, hence **dependent on a display** and making the entire thing *not headless*.
3. Pywhatkit library **may not successfully send the message** sometimes. Sometimes, it opens [Whatsapp Web](https://web.whatsapp.com/), writes the message, but doesn't send it.
4. If the **HTML structure of [TNB portal](https://www.mytnb.com.my/) or [Air Selangor portal](https://crisportal.airselangor.com/?lang=en) changes** or either **websites are down**, the automation will fail. (**Seasonal web popups** that are not expected by the automation can cause it to fail too)
5. If **any of the dependencies fail**, the automation fails too.
6. The automation **now** relies on a private API to send the whatsapp messages. If the API faces problems, the automation fails too (only on sending whatsapp messages).

## How it Works

1. A Selenium webdriver for chrome is initialized, and will 'drive' on Google Chrome.
2. Utility bills are scraped/generated:
   1. Opens [TNB portal](https://www.mytnb.com.my/) to:
      1. Login
      2. Retrieve billing details e.g. total cost, bill date etc.
   2. Step 2 is repeated for [Air Selangor portal](https://crisportal.airselangor.com/?lang=en).
   3. Internet bills and house rents are fixed for every month, so it is generated.
3. Active monthly installments are retrieved from the database and calculated.
   1. If on the current date of automation exeuction, the installment is being calculated on its final month, it will then automatically set the said installment to 'inactive' status afterwards.
4. A new monthly billing statement is produced based on the installments' and utilities' data and persisted to the db.
5. A Whatsapp text message is generated in the format of (e.g.):
```
*Bill September 2023*

Utilities:
Elektrik = RM87.85
Air = RM34.85
Unifi = RM168.55
Sewa = RM1000

Installments:
Credit card (Washing Machine) = RM193.17

Total per person = RM1484.42/5 = *RM296.88*
```
6. In this latest version of automation where it uses a private API, the message generated in Step 5.

## GitHub Actions

As of v0.1, the automation supports execution on **GitHub Actions**. There are 4 workflows, each of their .yml file in the .github/workflows directory:
- Dev branch build & test (build-dev-branch.yml)
  - Triggered on every push to the dev branch.
- Master branch build & test (build-master.yml)
  - Triggered on every pull request to the master branch.
- Master branch cron job tests (cron-master-test.yml)
  - Scheduled to run every 5 days at 9.00am (GMT+0 time).
- Master branch main cron job (cron-master-main.yml)
  - Scheduled to run on the 1st day of every month at 9.00am (GMT+0 time).

## Setup
1. Create a .env file with the following details:

````
TNB_EMAIL=[your TNB account email]
TNB_PASSWORD=[your TNB account password]
AIR_EMAIL=[your Air Selangor account email]
AIR_PASSWORD=[your Air Selangor account password]
mynum=[your Whatsapp phone number]
ws_group_id=[your whatsapp group id]
DB_URI=[ remote postgresql instance connection string URI/URL ]
DB_USERNAME=[ remote postgresql instance username ]
DB_PASSWORD=[ remote postgresql instance user password ]
DB_HOST=[ remote postgresql instance host name ]
DB_PORT=[ remote postgresql instance port ]
DB_DATABASE=[ remote postgresql instance default database for the automation ]
SUPABASE_API_URL=[ your supabase project API URL ]
SUPABASE_ANON_KEY=[ your supabase project anon key ]
````

Replace the placeholder details with your details. Make sure the remove the squared brackets, and leave no spaces
between the equals and your written details, e.g. `TNB_EMAIL=myemail@email.com`.

To find the ID of a whatsapp group, refer to [this](https://www.alphr.com/whatsapp-find-group/) link.

To find your supabase postgresql database credentials, refer to [this](https://supabase.com/docs/guides/database/connecting-to-postgres) link. Make sure to create an account first.

2. Run `./setup.sh` to install dependencies. (run `chmod u+x setup.sh` first if encountered permission problems)

## Execution
Run `./runner.sh` to execute the program. (run the chmod command if permission denied)

**NOTE**: You would most likely need to login to whatsapp web the first time you execute the program to link your 
whatsapp account to Ubuntu's Google Chrome.
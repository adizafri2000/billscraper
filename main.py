import os
import platform

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import automation
import credit_card_payments as ccp
import whatsapp
from main_logging import logger

# to avoid KeyError 'Display' when importing pywhatkit
os.environ['DISPLAY'] = ':0'

load_dotenv()
data = []


def clean_resources(driver: webdriver.Chrome):
    driver.close()
    driver.quit()
    logger.info("Closed and quit webdriver connection!")


def get_chromedriver(headless=False):
    """Returns a chromedriver executable based on detected machine OS"""
    driver_dir = "chromedriver" + os.sep
    if platform.system().lower() != "windows":
        driver_dir += "LINUX_64_chromedriver"
        driver_dir = "./" + driver_dir
    else:
        driver_dir += "WIN_32_chromedriver.exe"
    logger.info("Using chromedriver from {}".format(driver_dir))

    option = webdriver.ChromeOptions()
    if headless:
        logger.info("Running chromedriver in headless mode")
        option.add_argument("--headless=new")
    else:
        logger.info("Running chromedriver in normal GUI mode")

    option.add_argument('--disable-gpu')
    option.add_argument('--no-sandbox')
    option.add_argument("--window-size=1920x1080")

    return webdriver.Chrome(driver_dir, options=option)


def get_chromedriver_by_service(headless=False):
    option = webdriver.ChromeOptions()
    if headless:
        logger.info("Running chromedriver in headless mode")
        option.add_argument("--headless=new")
    else:
        logger.info("Running chromedriver in normal GUI mode")

    option.add_argument('--disable-gpu')
    option.add_argument('--no-sandbox')
    option.add_argument("--window-size=1920x1080")

    return webdriver.Chrome(
        #service=Service(ChromeDriverManager().install()),
        service=Service(),
        options=option
    )


def dump_dummy_data() -> []:
    return [{'type': 'Elektrik', 'to_pay': '36.85', 'bill_date': '24-Apr-2023', 'retrieved_date': '20230515-005254'},
            {'type': 'Air', 'to_pay': '6.00', 'bill_date': '28-Apr-2023', 'retrieved_date': '20230515-005300'},
            {'type': 'Unifi', 'to_pay': '168.55', 'bill_date': '10-May-2023', 'retrieved_date': '20230515-005300'}]
def main():
    driver = get_chromedriver_by_service(headless=True)
    driver.set_window_size(1920,1080)
    driver.implicitly_wait(5)
    logger.info(f"Driver window size: {driver.get_window_size()}")

    data.append(automation.automate_tnb(driver))
    data.append(automation.automate_air(driver))
    data.append(automation.generate_internet_bill())
    data.append(ccp.split_washing_machine())
    #data = dump_dummy_data()
    logger.debug(data)

    msg = whatsapp.generate_message(data)
    logger.info(msg)
    whatsapp.send_whatsapp_to_me(msg)
    #whatsapp.send_whatsapp_group(msg)

    clean_resources(driver)
    logger.info("Program finished!")

if __name__ == '__main__':
    main()

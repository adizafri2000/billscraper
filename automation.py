import os
from datetime import datetime

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import utilities
from main_logging import logger

load_dotenv()
TNB_URL = "https://www.mytnb.com.my/"
TNB_DASHBOARD_URL = "https://myaccount.mytnb.com.my/AccountManagement/IndividualDashboard"
AIR_URL = "https://crisportal.airselangor.com/?lang=en"
AIR_DASHBOARD_URL = 'https://crisportal.airselangor.com/profile/dashboard?lang=en'
SCREENSHOT_DIR = "screenshots"

# TODO Add logouts to all the automation logic
# TODO Clean up the mess(es) (basically everything)

def generate_scshot_name(bill_type):
    bill_type = bill_type.lower()
    folder = "tnb" if bill_type == "tnb" else "air" if bill_type == "air" else "unifi"
    logger.debug(f"Before reversing. At {os.getcwd()}")
    while os.path.basename(os.getcwd())!="billscraper":
        os.chdir("..")
        logger.debug(f"Moved back one directory. Currently at {os.getcwd()}")
    return SCREENSHOT_DIR + os.sep + folder + os.sep + f"{folder}-" + datetime.now().strftime("%Y%m%d-%H%M%S") + ".png"


# TODO Add a checkpoint in the logic to return e.g. False to caller
#  in case of failed automation
def automate_tnb(driver: webdriver.Chrome) -> {}:
    driver.get(TNB_URL)
    logger.info(f"Current browser URL: {driver.current_url}")

    tnb_email_input = driver.find_element(By.NAME, "email")
    tnb_password_input = driver.find_element(By.NAME, "password")
    tnb_login_button = driver.find_element(By.XPATH,
                                           "//*[@id=\"frm-login\"]/div[2]/div/div[2]/div/div[5]/div[2]/button")

    tnb_email = os.getenv("TNB_EMAIL")
    tnb_password = os.getenv("TNB_PASSWORD")

    tnb_email_input.send_keys(tnb_email)
    tnb_password_input.send_keys(tnb_password)
    tnb_login_button.click()

    time = 0
    while driver.current_url != TNB_DASHBOARD_URL or time < 15:
        # WebDriverWait(driver, 5).until(EC.url_changes(TNB_DASHBOARD_URL))
        driver.implicitly_wait(3)
        time += 3


    xpath = {
        "bill_date" : "//*[@id=\"mainBody\"]/div[5]/div[1]/div/div/div/div[2]/div[1]/div[2]/div[2]/label",
        "prev_balance" : "//*[@id=\"mainBody\"]/div[5]/div[1]/div/div/div/div[2]/div[1]/div[3]/div[2]/label",
        "current_charges" : "//*[@id=\"mainBody\"]/div[5]/div[1]/div/div/div/div[2]/div[1]/div[4]/div[2]/label",
        "rounding_adj" : "//*[@id=\"mainBody\"]/div[5]/div[1]/div/div/div/div[2]/div[1]/div[5]/div[2]/label",
        "to_pay" : "//*[@id=\"mainBody\"]/div[5]/div[1]/div/div/div/div[2]/div[2]/div[2]/div/span[2]",
        "latest_bill" : "//*[@id=\"mainBody\"]/div[5]/div[1]/div/div/div/div[2]/div[1]/div[3]/div[2]/label",
        "outstanding_charges" : "//*[@id=\"mainBody\"]/div[5]/div[1]/div/div/div/div[2]/div[1]/div[4]/div[2]/label",
        "popup_later_button_xpath" : "//*[@id=\"modal-button-1\"]/div/button[1]"
    }

    logger.info(f"Current browser URL: {driver.current_url}")

    try:
        logger.info("Attempting to find popup...")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath.get("popup_later_button_xpath"))))
        popup_later_button = driver.find_element(By.XPATH, xpath.get("popup_later_button_xpath"))
        popup_later_button.click()
        logger.info("Popup found & closed")
    except:
        logger.info("Popup not found")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.XPATH, xpath.get("to_pay"))))
    finally:
        driver.implicitly_wait(7)

        to_pay = driver.find_element(By.XPATH, xpath.get("to_pay")).text
        bill_date = driver.find_element(By.XPATH, xpath.get("bill_date")).text

        # different presented UI and needed steps if bill already paid
        if to_pay=="0.00":
            latest_bill = driver.find_element(By.XPATH,xpath.get("latest_bill")).text.split()[1]
            outstanding_charges = driver.find_element(By.XPATH, xpath.get("outstanding_charges")).text.split()[1]
            msg = (f"TNB Bill Scraped Data:\n"
            f"Bill Date: {bill_date}\n"
            f"Outstanding Charges: RM{outstanding_charges}\n"
            f"Latest Bill: RM{latest_bill}\n"
            f"Bill has been paid!")

            # since to_pay is 0.00 since it's already been paid, assign latest_bill to to_pay
            to_pay=latest_bill

        else:
            prev_balance = driver.find_element(By.XPATH, xpath.get("prev_balance")).text.split()[1]
            current_charges = driver.find_element(By.XPATH, xpath.get("current_charges")).text.split()[1]
            rounding_adj = driver.find_element(By.XPATH, xpath.get("rounding_adj")).text.split()[1]
            msg = (f"TNB Bill Scraped Data:\n"
            f"Bill Date: {bill_date}\n"
            f"Previous Balance: RM{prev_balance}\n"
            f"Current Charges: RM{current_charges}\n"
            f"Rounding Adjustment: RM{rounding_adj}\n"
            f"To pay: RM{to_pay}")

        logger.info(msg)

    img_name = generate_scshot_name("tnb")
    logger.info(f"Saving image to {img_name}")
    driver.save_screenshot(img_name)

    # logging out
    '''
    path_logout_button = "//*[@id=\"logout\"]/p/span"
    driver.find_element(By.XPATH,path_logout_button).click()

    if driver.current_url=="https://www.mytnb.com.my/":
        logger.info("Successfully logged out")
    '''

    return {
        "type": "Elektrik",
        "to_pay": to_pay,
        "bill_date": utilities.date_formatter(bill_date),
        "retrieved_date": datetime.now().strftime("%Y%m%d-%H%M%S")
    }


def automate_air(driver: webdriver.Chrome) -> {}:
    driver.get(AIR_URL)
    logger.info(f"Current browser URL: {driver.current_url}")

    # close popup
    try:
        popup_close_button = driver.find_element(By.XPATH, "//*[@id=\"__layout\"]/div/div[2]/div/div/span/i")
        popup_close_button.click()
        logger.info("Popup found and closed!")
        driver.save_screenshot(generate_scshot_name("air"))
    except:
        logger.info("No popup found!")
        driver.save_screenshot(generate_scshot_name("air"))
        pass

    driver.implicitly_wait(5)
    air_email_input = driver.find_element(By.XPATH,"//*[@id=\"__layout\"]/div/div[1]/div[2]/section/div[1]/div[2]/div/section/div/div/div/div/div[1]/div[1]/input")
    air_password_input = driver.find_element(By.XPATH, "//*[@id=\"__layout\"]/div/div[1]/div[2]/section/div[1]/div[2]/div/section/div/div/div/div/div[1]/div[2]/div/input")
    air_login_button = driver.find_element(By.XPATH, "//*[@id=\"__layout\"]/div/div[1]/div[2]/section/div[1]/div[2]/div/section/div/div/div/div/div[2]/div[2]/button")

    air_email = os.getenv("AIR_EMAIL")
    air_password = os.getenv("AIR_PASSWORD")

    air_email_input.send_keys(air_email)
    air_password_input.send_keys(air_password)
    air_login_button.click()

    while (driver.current_url != AIR_DASHBOARD_URL):
        # WebDriverWait(driver, 5).until(EC.url_changes(TNB_DASHBOARD_URL))
        driver.implicitly_wait(3)

    # Go to billing & payment page at https://crisportal.airselangor.com/profile/billing?lang=en
    driver.find_element(By.XPATH, "//*[@id=\"__layout\"]/div/div[1]/div[1]/div/div/a[4]").click()

    logger.info(f"Current browser URL: {driver.current_url}")

    to_pay = driver.find_element(By.XPATH, "//*[@id=\"printBill\"]/tbody/tr[1]/td[5]").text
    bill_date = driver.find_element(By.XPATH, "//*[@id=\"printBill\"]/tbody/tr[1]/td[3]").text

    logger.info(f"Air Selangor Bill Scraped Data:\nBill Date: {bill_date}\nTo pay: RM{to_pay}")

    img_name = generate_scshot_name("air")
    logger.info(f"Saving image to {img_name}")
    driver.save_screenshot(img_name)

    return {
        "type": "Air",
        "to_pay": to_pay,
        "bill_date": utilities.date_formatter(bill_date),
        "retrieved_date": datetime.now().strftime("%Y%m%d-%H%M%S")
    }

def generate_internet_bill():
    logger.info("Using generator method to generate internet bill and skip web scraping")
    datetoday = datetime.today().strftime("%d-%b-%Y")
    _, month, year = datetoday.split('-')
    datetoday = f"10-{month}-{year}"
    return {
        "type": "Unifi",
        "to_pay": "168.55",
        "bill_date": datetoday,
        "retrieved_date": datetime.now().strftime("%Y%m%d-%H%M%S")
    }

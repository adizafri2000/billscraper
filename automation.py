import os
import time
from datetime import datetime

from dotenv import load_dotenv
from selenium import webdriver
from selenium.common import NoSuchElementException, WebDriverException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import utilities
from DTO import AutomationDTO
from main_logging import logger
import storage
import requests

load_dotenv()
TNB_URL = "https://www.mytnb.com.my/"
TNB_DASHBOARD_URL = "https://myaccount.mytnb.com.my/AccountManagement/IndividualDashboard"
AIR_URL = "https://crisportal.airselangor.com/?lang=en"
AIR_DASHBOARD_URL = 'https://crisportal.airselangor.com/profile/dashboard?lang=en'
SCREENSHOT_DIR = "screenshots"

BILL_TNB = "tnb"
BILL_AIR = "air"


# TODO Add logouts to all the automation logic
# TODO Clean up the mess(es) (basically everything)

def generate_file_name(bill_type, extension, new=True):
    """
    Generates file name for the screenshot image file with .png extension
    :param extension: file extension e.g. "png", "html"
    :param bill_type: "tnb" or "air", depending on bill type
    :param new: True for GitHub Actions support i.e saving only filename + extension w/o relative/absolute paths, False for else
    :return: generated file name e.g air-20230706-003906.png. If new is set to False, includes absolute path
    """
    bill_type = bill_type.lower()
    folder = "tnb" if bill_type == "tnb" else "air" if bill_type == "air" else "unifi"
    logger.debug(f"Before reversing. At {os.getcwd()}")
    while os.path.basename(os.getcwd()) != "billscraper":
        os.chdir("..")
        logger.debug(f"Moved back one directory. Currently at {os.getcwd()}")
    if new:
        return f"{folder}-" + datetime.now().strftime("%Y%m%d-%H%M%S") + f".{extension}"
    return os.getcwd() + os.sep + SCREENSHOT_DIR + os.sep + folder + os.sep + f"{folder}-" + datetime.now().strftime(
        "%Y%m%d-%H%M%S") + f".{extension}"


def generate_screenshot(driver, bill_type):
    img_name = generate_file_name(bill_type, "png")
    logger.info(f"Will save image to {img_name}")
    time.sleep(3)
    res = driver.get_screenshot_as_file(img_name)
    logger.info(f"Is screenshot saved: {res}")
    storage.upload_to_bucket(folder=bill_type, file=img_name)


def generate_page_html(driver, bill_type):
    html_name = generate_file_name(bill_type, "html")
    logger.info(f"Will save page HTML to {html_name}")
    with open(html_name, "w", encoding="utf-8") as file:
        file.write(driver.page_source)
    logger.info(f"HTML saved to {html_name}")
    storage.upload_to_bucket(folder=bill_type, file=html_name)


def handle_scraping_error(driver, bill_type):
    """
    Handles error during scraping process. Takes screenshot, saves page HTML, and terminates program
    :param driver: Current webdriver
    :param bill_type: "tnb" or "air", depending on bill type
    """
    logger.error("Error occurred during scraping. Taking screenshot, saving page HTML, and terminate program")
    generate_screenshot(driver, bill_type)
    generate_page_html(driver, bill_type)
    logger.error("Terminating program...")
    exit(1)


def check_forbidden_status(url, bill_type):
    try:
        response = requests.get(url)
        logger.info(f"{url} return status code: {response.status_code}")
        if response.status_code == 403:
            logger.error(f"Error: 403 Forbidden on {url}, beginning program termination")
            handle_scraping_error(driver, bill_type)
    except requests.RequestException as e:
        logger.error(f"Error: {e}")


def automate_tnb(driver: webdriver.Chrome) -> {}:
    try:
        check_forbidden_status(TNB_URL, BILL_TNB)
        wait = WebDriverWait(driver, 20)
        driver.get(TNB_URL)
        logger.info(f"Current browser URL: {driver.current_url}")

        # take screenshot when arrived at login page
        logger.info("Generating screenshot at login page arrival")
        generate_screenshot(driver, BILL_TNB)

        try:
            time.sleep(5)
            popup = driver.find_element(By.XPATH, "//*[@id=\"content\"]/div/div[1]/div/div/div[2]/button")
            logger.info(f'popup displayed: {popup.is_displayed()}')
            popup.click()
            time.sleep(5)
        except:
            logger.info("popup not found...")
        finally:
            logger.info(
                "Generating screenshot before inputting to login inputs at login page, popup confirmed not present as of now")
            generate_screenshot(driver, BILL_TNB)

        tnb_email_input = driver.find_element(By.NAME, "Email")
        time.sleep(5)
        tnb_password_input = driver.find_element(By.NAME, "Password")
        # tnb_login_button = driver.find_element(By.XPATH,"//*[@id=\"frm-login\"]/div[2]/div/div[2]/div/div[5]/div[2]/button")

        tnb_email = os.getenv("TNB_EMAIL")
        tnb_password = os.getenv("TNB_PASSWORD")
        time.sleep(5)

        tnb_email_input.send_keys(tnb_email)
        tnb_password_input.send_keys(tnb_password)
        # tnb_login_button.click()
        # clicking login button replaced with sending enter key to password input
        tnb_password_input.send_keys(Keys.ENTER)

        time = 0
        while driver.current_url != TNB_DASHBOARD_URL or time < 15:
            # WebDriverWait(driver, 5).until(EC.url_changes(TNB_DASHBOARD_URL))
            driver.implicitly_wait(3)
            time += 3

        xpath = {
            "bill_date": "//*[@id=\"mainBody\"]/div[5]/div[1]/div/div/div/div[2]/div[1]/div[2]/div[2]/label",
            "prev_balance": "//*[@id=\"mainBody\"]/div[5]/div[1]/div/div/div/div[2]/div[1]/div[3]/div[2]/label",
            "current_charges": "//*[@id=\"mainBody\"]/div[5]/div[1]/div/div/div/div[2]/div[1]/div[4]/div[2]/label",
            "rounding_adj": "//*[@id=\"mainBody\"]/div[5]/div[1]/div/div/div/div[2]/div[1]/div[5]/div[2]/label",
            "to_pay": "//*[@id=\"mainBody\"]/div[5]/div[1]/div/div/div/div[2]/div[2]/div[2]/div/span[2]",
            "latest_bill": "//*[@id=\"mainBody\"]/div[5]/div[1]/div/div/div/div[2]/div[1]/div[3]/div[2]/label",
            "outstanding_charges": "//*[@id=\"mainBody\"]/div[5]/div[1]/div/div/div/div[2]/div[1]/div[4]/div[2]/label",
            "popup_later_button_xpath": "//*[@id=\"modal-button-2\"]/div/button[1]",  # if doesnt work, change to 1,
            "last_payment": "//*[@id=\"mainBody\"]/div[5]/div[2]/div/div/div/div[2]/div/div[2]"
        }

        logger.info(f"Current browser URL: {driver.current_url}")
        # take screenshot when arrived at dashboard
        logger.info("Generating screenshot at dashboard page")
        generate_screenshot(driver, BILL_TNB)

        try:
            logger.info("Attempting to find popup...")
            wait.until(EC.presence_of_element_located((By.XPATH, xpath.get("popup_later_button_xpath"))))
            popup_later_button = driver.find_element(By.XPATH, xpath.get("popup_later_button_xpath"))
            popup_later_button.click()
            logger.info("Popup found & closed")
        except:
            logger.info("Popup not found")
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                (By.XPATH, xpath.get("to_pay"))))
        finally:
            driver.implicitly_wait(7)
            WebDriverWait(driver, 20)

            # take screenshot when dashboard is ready to be scraped
            logger.info("Generating screenshot at before scraping data")
            generate_screenshot(driver, BILL_TNB)

            to_pay = driver.find_element(By.XPATH, xpath.get("to_pay")).text
            bill_date = driver.find_element(By.XPATH, xpath.get("bill_date")).text

            # different presented UI and needed steps if bill already paid
            if to_pay == "0.00":
                latest_bill = driver.find_element(By.XPATH, xpath.get("last_payment")).text.split()[1]
                outstanding_charges = driver.find_element(By.XPATH, xpath.get("outstanding_charges")).text.split()[1]
                msg = (f"TNB Bill Scraped Data:\n"
                       f"Bill Date: {bill_date}\n"
                       # f"Outstanding Charges: RM{outstanding_charges}\n"
                       f"Latest Bill: RM{latest_bill}\n"
                       f"Bill has been paid!")

                # since to_pay is 0.00 since it's already been paid, assign latest_bill to to_pay
                to_pay = latest_bill

            else:
                prev_balance = driver.find_element(By.XPATH, xpath.get("prev_balance")).text.split()[1]
                current_charges = driver.find_element(By.XPATH, xpath.get("current_charges")).text.split()[1]
                try:
                    rounding_adj = driver.find_element(By.XPATH, xpath.get("rounding_adj")).text.split()[1]
                except NoSuchElementException:
                    logger.info("No rounding adjustment found (no theft), setting value to 0")
                    rounding_adj = 0.00
                msg = (f"TNB Bill Scraped Data:\n"
                       f"Bill Date: {bill_date}\n"
                       f"Previous Balance: RM{prev_balance}\n"
                       f"Current Charges: RM{current_charges}\n"
                       f"Rounding Adjustment: RM{rounding_adj}\n"
                       f"To pay: RM{to_pay}")

            logger.info(msg)

        return AutomationDTO(
            type="Elektrik",
            id="1",
            to_pay=str(to_pay),
            retrieved_date=datetime.now().strftime("%Y%m%d-%H%M%S"),
            bill_date=utilities.date_formatter(bill_date)
        )
    except WebDriverException as e:
        logger.error(f"Error occurred during scraping: {e}")
        handle_scraping_error(driver, BILL_TNB)


def automate_air(driver: webdriver.Chrome) -> {}:
    try:
        check_forbidden_status(AIR_URL, BILL_AIR)
        driver.get(AIR_URL)
        logger.info(f"Current browser URL: {driver.current_url}")

        # take screenshot when arrived at home page
        logger.info("Generating screenshot at login page arrival")
        generate_screenshot(driver, BILL_AIR)

        # close popup
        try:
            popup_close_button = driver.find_element(By.XPATH, "//*[@id=\"__layout\"]/div/div[2]/div/div/span/i")
            popup_close_button.click()
            logger.info("Popup found and closed!")
        except:
            logger.info("No popup found!")
            pass

        # take screenshot after popups and before inputting to login fields
        logger.info("Generating screenshot before inputting login fields at login page")
        generate_screenshot(driver, BILL_AIR)

        driver.implicitly_wait(5)
        air_email_input = driver.find_element(By.XPATH,
                                              "//*[@id=\"__layout\"]/div/div[1]/div[2]/section/div[1]/div[2]/div/section/div/div/div/div/div[1]/div[1]/input")
        air_password_input = driver.find_element(By.XPATH,
                                                 "//*[@id=\"__layout\"]/div/div[1]/div[2]/section/div[1]/div[2]/div/section/div/div/div/div/div[1]/div[2]/div/input")
        air_login_button = driver.find_element(By.XPATH,
                                               "//*[@id=\"__layout\"]/div/div[1]/div[2]/section/div[1]/div[2]/div/section/div/div/div/div/div[2]/div[2]/button")

        air_email = os.getenv("AIR_EMAIL")
        air_password = os.getenv("AIR_PASSWORD")

        air_email_input.send_keys(air_email)
        air_password_input.send_keys(air_password)
        air_login_button.click()

        while driver.current_url != AIR_DASHBOARD_URL:
            # WebDriverWait(driver, 5).until(EC.url_changes(TNB_DASHBOARD_URL))
            driver.implicitly_wait(3)

        # take screenshot when arrived at dashboard
        logger.info("Generating screenshot at dashboard page arrival")
        generate_screenshot(driver, BILL_AIR)

        # Go to billing & payment page at https://crisportal.airselangor.com/profile/billing?lang=en
        driver.find_element(By.XPATH, "//*[@id=\"__layout\"]/div/div[1]/div[1]/div/div/a[4]").click()

        logger.info(f"Current browser URL: {driver.current_url}")

        # take screenshot when arrived at billing & payment page
        logger.info("Generating screenshot at billing & payment page arrival & before scraping")
        generate_screenshot(driver, BILL_AIR)

        to_pay = driver.find_element(By.XPATH, "//*[@id=\"printBill\"]/tbody/tr[1]/td[4]").text
        bill_date = driver.find_element(By.XPATH, "//*[@id=\"printBill\"]/tbody/tr[1]/td[3]").text

        logger.info(f"Air Selangor Bill Scraped Data:\nBill Date: {bill_date}\nTo pay: RM{to_pay}")

        return AutomationDTO(
            type="Air",
            id="2",
            to_pay=str(to_pay),
            retrieved_date=datetime.now().strftime("%Y%m%d-%H%M%S"),
            bill_date=bill_date
        )
    except WebDriverException as e:
        logger.error(f"Error occurred during scraping: {e}")
        handle_scraping_error(driver, BILL_AIR)

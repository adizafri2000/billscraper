import os

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import utilities

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
    return SCREENSHOT_DIR + os.sep + folder + os.sep + f"{folder}-" + datetime.now().strftime("%Y%m%d-%H%M%S") + ".png"


# TODO Add a checkpoint in the logic to return e.g. False to caller
#  in case of failed automation
def automate_tnb(driver: webdriver.Chrome) -> {}:
    driver.get(TNB_URL)
    #driver.fullscreen_window()
    print(f"Current browser URL: {driver.current_url}")
    #driver.set_window_size(1920,1080)
    print(driver.get_window_size())

    tnb_email_input = driver.find_element(By.NAME, "email")
    tnb_password_input = driver.find_element(By.NAME, "password")
    tnb_login_button = driver.find_element(By.XPATH,
                                           "//*[@id=\"frm-login\"]/div[2]/div/div[2]/div/div[5]/div[2]/button")

    tnb_email = os.getenv("TNB_EMAIL")
    tnb_password = os.getenv("TNB_PASSWORD")

    #driver.maximize_window()
    #driver.set_window_size(1920, 1080)
    #driver.fullscreen_window()
    tnb_email_input.send_keys(tnb_email)
    tnb_password_input.send_keys(tnb_password)
    tnb_login_button.click()
    #driver.maximize_window()

    time = 0
    while driver.current_url != TNB_DASHBOARD_URL or time < 15:
        # WebDriverWait(driver, 5).until(EC.url_changes(TNB_DASHBOARD_URL))
        driver.implicitly_wait(3)
        time += 3

    #driver.maximize_window()

    xpath = {
        "bill_date" : "//*[@id=\"mainBody\"]/div[5]/div[1]/div/div/div/div[2]/div[1]/div[2]/div[2]/label",
        "prev_balance" : "//*[@id=\"mainBody\"]/div[5]/div[1]/div/div/div/div[2]/div[1]/div[3]/div[2]/label",
        "current_charges" : "//*[@id=\"mainBody\"]/div[5]/div[1]/div/div/div/div[2]/div[1]/div[4]/div[2]/label",
        "rounding_adj" : "//*[@id=\"mainBody\"]/div[5]/div[1]/div/div/div/div[2]/div[1]/div[5]/div[2]/label",
        "to_pay" : "//*[@id=\"mainBody\"]/div[5]/div[1]/div/div/div/div[2]/div[2]/div[2]/div/span[2]",
        "popup_later_button_xpath" : "//*[@id=\"modal-button-1\"]/div/button[1]"
    }


    try:
        print("trying...")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath.get("popup_later_button_xpath"))))
        popup_later_button = driver.find_element(By.XPATH, "//*[@id=\"modal-button-1\"]/div/button[1]")
        popup_later_button.click()
        print("popup found & closed")
    except:
        print("Error occured, now in except block")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.XPATH, "//*[@id=\"mainBody\"]/div[5]/div[1]/div/div/div/div[2]/div[2]/div[2]/div/span[2]")))
    finally:
        print("Now in finally block")
        driver.implicitly_wait(7)
        to_pay = driver.find_element(By.XPATH, xpath.get("to_pay")).text
        bill_date = driver.find_element(By.XPATH, xpath.get("bill_date")).text
        prev_balance = driver.find_element(By.XPATH, xpath.get("prev_balance")).text.split()[1]
        current_charges = driver.find_element(By.XPATH, xpath.get("current_charges")).text.split()[1]
        rounding_adj = driver.find_element(By.XPATH, xpath.get("rounding_adj")).text.split()[1]


        print(f"TNB Bill Scraped Data:\n"
              f"Bill Date: {bill_date}\n"
              f"Previous Balance: RM{prev_balance}\n"
              f"Current Charges: RM{current_charges}\n"
              f"Rounding Adjustment: RM{rounding_adj}\n"
              f"To pay: RM{to_pay}")

    '''
        if float(to_pay) == 0:
            to_pay = str(float(cur_charge) + float(rounding_adj))
            print(f"Electric bill already paid, generating total from current charge + rounding adjustment: RM{to_pay}")
    '''

    driver.save_screenshot(generate_scshot_name("tnb"))
    return {
        "type": "Elektrik",
        "to_pay": to_pay,
        "bill_date": utilities.date_formatter(bill_date),
        "retrieved_date": datetime.now().strftime("%Y%m%d-%H%M%S")
    }


def automate_air(driver: webdriver.Chrome) -> {}:
    driver.get(AIR_URL)
    driver.maximize_window()
    print(f"Current browser URL: {driver.current_url}")
    driver.save_screenshot(generate_scshot_name("air"))

    # close popup
    try:
        popup_close_button = driver.find_element(By.XPATH, "//*[@id=\"__layout\"]/div/div[2]/div/div/span/i")
        popup_close_button.click()
        print("Popup found and closed!")
        driver.save_screenshot(generate_scshot_name("air"))
    except:
        print("No popup found!")
        driver.save_screenshot(generate_scshot_name("air"))
        pass

    driver.implicitly_wait(5)
    air_email_input = driver.find_element(By.XPATH,"//*[@id=\"__layout\"]/div/div[1]/div[2]/section/div[1]/div[2]/div/section/div/div/div/div/div[1]/div[1]/input")
    #air_email_input = driver.find_element(By.XPATH,"/html/body/div/div/div/div[1]/div[2]/section/div[1]/div[2]/div/section/div/div/div/div/div[1]/div[1]/input")
    air_password_input = driver.find_element(By.XPATH, "//*[@id=\"__layout\"]/div/div[1]/div[2]/section/div[1]/div[2]/div/section/div/div/div/div/div[1]/div[2]/div/input")
    air_login_button = driver.find_element(By.XPATH, "//*[@id=\"__layout\"]/div/div[1]/div[2]/section/div[1]/div[2]/div/section/div/div/div/div/div[2]/div[2]/button")

    air_email = os.getenv("AIR_EMAIL")
    air_password = os.getenv("AIR_PASSWORD")

    driver.maximize_window()
    air_email_input.send_keys(air_email)
    air_password_input.send_keys(air_password)
    air_login_button.click()
    driver.maximize_window()

    while (driver.current_url != AIR_DASHBOARD_URL):
        # WebDriverWait(driver, 5).until(EC.url_changes(TNB_DASHBOARD_URL))
        driver.implicitly_wait(3)

    driver.fullscreen_window()  # webdriver cannot detect searched elements is using maximize_window()

    # Go to billing & payment page at https://crisportal.airselangor.com/profile/billing?lang=en
    driver.find_element(By.XPATH, "//*[@id=\"__layout\"]/div/div[1]/div[1]/div/div/a[4]").click()

    driver.fullscreen_window()
    print(driver.current_url)
    to_pay = driver.find_element(By.XPATH, "//*[@id=\"printBill\"]/tbody/tr[1]/td[5]").text
    bill_date = driver.find_element(By.XPATH, "//*[@id=\"printBill\"]/tbody/tr[1]/td[3]").text

    print(f"Air Selangor Bill Scraped Data:\nBill Date: {bill_date}\nTo pay: RM{to_pay}")

    driver.save_screenshot(generate_scshot_name("air"))
    print(driver.current_url)
    return {
        "type": "Air",
        "to_pay": to_pay,
        "bill_date": utilities.date_formatter(bill_date),
        "retrieved_date": datetime.now().strftime("%Y%m%d-%H%M%S")
    }

# TODO Move this somewhere else e.g. a bill generator method
#  instead of an automation method
def automate_internet(driver: webdriver.Chrome, skip_automation=True):
    if skip_automation:
        print("Skipping automation for unifi bill scraping")
        datetoday = datetime.today().strftime("%d-%b-%Y")
        _, month, year = datetoday.split('-')
        datetoday = f"10-{month}-{year}"
        return {
            "type": "Unifi",
            "to_pay": "168.55",
            "bill_date": datetoday,
            "retrieved_date": datetime.now().strftime("%Y%m%d-%H%M%S")
        }
    else:
        driver.get("https://www.google.com")
        driver.fullscreen_window()
        print(driver.current_url)
        driver.save_screenshot(generate_scshot_name("unifi"))


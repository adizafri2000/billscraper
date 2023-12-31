import argparse
import os
import platform

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

import automation
import installments as ccp
import data_services
import whatsapp
from DTO import WhatsappMessageDTO
from data_services import calculate_new_statement, insert_statement, insert_monthly_utility, insert_monthly_installment
from main_logging import logger

load_dotenv()
utilities = []
installments = []


def clean_resources(driver: webdriver.Chrome, conn=None):
    driver.close()
    driver.quit()
    logger.info("Closed and quit webdriver connection!")
    data_services.close_connection()
    logger.info("Closed and quit database connection!")


@DeprecationWarning
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
    # add user agent option to bypass cloudflare
    option.add_argument(
        'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36')

    return webdriver.Chrome(
        # service=Service(ChromeDriverManager().install()),
        service=Service(),
        options=option
    )


def parse_arguments():
    """
  This function parses the command line arguments and returns a dictionary of the arguments. Generated via Bard
  """

    # Create the parser
    parser = argparse.ArgumentParser()

    # Add the arguments
    parser.add_argument("-m", "--send_message", action="store_true",
                        help="Whether to send a message to the WhatsApp group.")
    parser.add_argument("-db", "--database_schema", help="The database schema to use. Defaults to `sqa`.")

    # Parse the arguments
    args = parser.parse_args()

    # Set the default value for the database_schema argument
    if not args.database_schema:
        args.database_schema = "sqa"

    # Return the arguments as a dictionary
    return vars(args)


def main():
    """
    Optional command line arguments:

    -m / --send_message
        - Will send a whatsapp message to the group. Defaults to skipping if not provided. Only need to
          include the flag, does not need any arguments.
    -db/ --database_schema
        - Will use the defined database schema given in the argument. Defaults to 'sqa' if not provided.
          Possible values: 'sqa', 'billing'
    """

    # Get the parsed arguments
    args = parse_arguments()

    # Do something with the arguments
    if args["send_message"]:
        logger.info("Execution will send message to WhatsApp group...")
    else:
        logger.info("Skipping WhatsApp message...")

    logger.info(f"Using database schema: {args['database_schema']}")
    data_services.schema = args["database_schema"]

    # print(f"At main.main, cwd: {os.getcwd()}")

    # chromedriver setup
    driver = get_chromedriver_by_service(headless=True)
    driver.set_window_size(1920, 1080)
    driver.implicitly_wait(5)
    logger.info(f"Driver window size: {driver.get_window_size()}")

    # execute automation for utilities
    utilities.append(automation.automate_tnb(driver))
    utilities.append(automation.automate_air(driver))
    utilities.append(automation.generate_internet_bill())
    utilities.append(automation.generate_house_rent_bill())

    # retrieve monthly payment data for active installments
    installments.extend(ccp.calculate_installments())

    data = {
        "utilities": utilities,
        "installments": installments
    }

    # perform calculation for a new billing statement
    statement = calculate_new_statement(data)

    # persist to database
    statement_id = insert_statement(statement)
    insert_monthly_installment(statement_id, installments)
    insert_monthly_utility(statement_id, utilities)
    logger.info(f"Statement details: {statement}")

    # generate details for whatsapp message
    message = WhatsappMessageDTO(statement, utilities, installments)
    logger.info(f"Normal formatted whatsapp message:\n{message.format_normal_msg()}")

    # send whatsapp message via REST API if argument received
    if args["send_message"]:
        logger.info(f"Sending formatted message to API: {whatsapp.send_whatsapp_message(message.format_api_msg())}")

    clean_resources(driver)
    logger.info("Program finished!")


if __name__ == '__main__':
    main()

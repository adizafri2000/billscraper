import argparse
import os
import platform

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions

import automation
import fixed_price_utility
import installments as ccp
import data_services
import whatsapp
from DTO import WhatsappMessageDTO
from data_services import calculate_new_statement, insert_statement, insert_monthly_utility, insert_monthly_installment
from main_logging import logger

load_dotenv()
utilities = []
installments = []


def clean_resources(driver: webdriver.Firefox, conn=None):
    driver.close()
    driver.quit()
    logger.info("Closed and quit webdriver connection!")
    data_services.close_connection()
    logger.info("Closed and quit database connection!")


def get_geckodriver(headless=False):
    """Returns a geckodriver executable based on detected machine OS"""
    logger.info("Using geckodriver for Firefox")

    options = FirefoxOptions()
    if headless:
        logger.info("Running geckodriver in headless mode")
        options.add_argument("--headless")
    else:
        logger.info("Running geckodriver in normal GUI mode")

    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument("--window-size=1920x1080")

    service = FirefoxService()
    return webdriver.Firefox(service=service, options=options)


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

    # geckodriver setup
    driver = get_geckodriver(headless=True)
    driver.set_window_size(1920, 1080)
    driver.implicitly_wait(5)
    logger.info(f"Driver window size: {driver.get_window_size()}")

    # execute automation for utilities
    utilities.append(automation.automate_tnb(driver))
    utilities.append(automation.automate_air(driver))
    # utilities.append(automation.generate_internet_bill())
    # utilities.append(automation.generate_house_rent_bill())

    # retrieve fixed-price monthly utilities
    utilities.extend(fixed_price_utility.calculate_fixed_utilities())

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

import os
import re
from datetime import datetime


def date_formatter(date):
    pattern = r'([\d]{1,2})([- ])(.+)([- ])([\d]{,4})'
    result = re.match(pattern, date)
    day = result[1]
    month = result[3]
    year = result[5]
    splitter = result[2]
    if result[2] == " " and result[4] == " ":
        date = day + "-" + month + "-" + year

    return date

def generate_log_file_name():
    now = datetime.now()
    log_folder = "logs"
    if not os.path.exists(log_folder):
        print("Dedicated log directory not found. Creating new directory logs/")
        os.mkdir(log_folder)
    os.chdir(log_folder)
    return now.strftime("%Y%m%d-%H%M%S")+".log"

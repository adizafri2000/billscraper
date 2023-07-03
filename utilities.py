import re


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

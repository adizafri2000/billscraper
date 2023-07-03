import utilities
from datetime import datetime
def split_washing_machine() -> {}:
    name = "Washing Machine"
    WASHING_MACHINE_TOTAL = 1159.00
    WASHING_MACHINE_MONTHS = 6
    WASHING_MACHINE_PEOPLE = 5
    WASHING_MACHINE_MONTHLY = 193.17

    datetoday = datetime.today().strftime("%d-%b-%Y")
    day, month, year = datetoday.split('-')
    datetoday = f"{day}-{month}-{year}"

    to_pay = WASHING_MACHINE_MONTHLY
    #bill date is set to the date the script is executed
    return {
        "type": f"Credit card ({name})",
        "to_pay": f"{to_pay:.2f}",
        "bill_date": datetoday,
        "retrieved_date": datetime.now().strftime("%Y%m%d-%H%M%S")
    }

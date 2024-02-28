from datetime import datetime

from DTO import AutomationDTO
from data_services import get_utility_details


def retrieve_fixed_price_utilities() -> []:
    utilities = [(a, b, c, d, e, f, g) for a, b, c, d, e, f, g in get_utility_details() if f is not None]
    utility_details = []
    for i in utilities:
        utility_details.append({
            "id": i[0],
            "name": i[1],
            "price": i[5]
        })

    return utility_details


def calculate_fixed_utilities(utility_details=retrieve_fixed_price_utilities()) -> []:
    monthly_fixed_utilities = []
    for i in utility_details:
        id = i["id"]
        name = i["name"]
        price = i["price"]

        monthly_fixed_utilities.append(AutomationDTO(
            type=f"{name}",
            id=id,
            to_pay=f"{price:.2f}",
            retrieved_date=datetime.now().strftime("%Y%m%d-%H%M%S")
        ))

    return monthly_fixed_utilities

# print(calculate_fixed_utilities())

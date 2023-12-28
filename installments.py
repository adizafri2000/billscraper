from datetime import datetime

from DTO import AutomationDTO
from data_services import get_installment_details, deactivate_installment
from dateutil.relativedelta import relativedelta
from main_logging import logger


def retrieve_installments() -> []:
    """Retrieves active installments' IDs, names, and total
    and returns them in the form of an array of dictionaries of
    id, name, total and period e.g.:

        list = [{"id":"a","name":"b","total":"c","period":"d"},...]
    """
    installments = get_installment_details()
    installment_details = []
    for i in installments:
        installment_details.append({
            "id": i[0],
            "name": i[1],
            "total": i[3],
            "period": i[4],
            "start_date": i[8]
        })

    return installment_details


def calculate_installments(installment_details=retrieve_installments()) -> []:
    monthly_installments = []
    for i in installment_details:
        id = i["id"]
        name = i["name"]
        total = i["total"]
        period = i["period"]

        # total to pay is total installment price divided by the total payment period (months)
        to_pay = total / period
        monthly_installments.append(AutomationDTO(
            type=f"Credit card ({name})",
            id=id,
            to_pay=f"{to_pay:.2f}",
            retrieved_date=datetime.now().strftime("%Y%m%d-%H%M%S")
        ))

        # check if current payment period has reached its end and close it if applicable
        if is_completed_installment(i):
            logger.info(f"Installment {i['name']} has reached end of payment period, setting to inactive")
            close_installment(i)

    return monthly_installments


def is_completed_installment(installment: {}) -> bool:
    """Checks if an installment has reached its end of payment period. An installment is considered completed
    if the current date is greater than or equal to the end date of the installment. The end date is calculated
    by adding the installment's period to its start date."""
    period = installment["period"]
    start_date = installment["start_date"]
    today = datetime.now().date()
    end_date = start_date + relativedelta(months=period)
    return today >= end_date


def close_installment(installment: {}):
    """Closes an installment by setting its status to inactive"""
    deactivate_installment(installment["id"])

from datetime import datetime

from DTO import AutomationDTO
from data_services import get_installment_details


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
            "period": i[4]
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

    return monthly_installments

import datetime


class AutomationDTO:
    """Automation DTO class to represent formatted scraped utilities'
    and calculated installments' data before being persisted to the database"""

    def __init__(self, type: str, id: str, to_pay: str, retrieved_date: datetime, bill_date=None):
        self.type = type
        self.id = id
        self.to_pay = to_pay
        self.retrieved_date = retrieved_date
        self.bill_date = bill_date

    def __repr__(self):
        return f"AutomationDTO(type={self.type}, id={self.id}, to_pay={self.to_pay}, retrieved_date={self.retrieved_date}, bill_date={self.bill_date})"


class StatementDTO:
    """DTO class to represent a Statement entity, final endpoint before persisted to database"""

    def __init__(self, name: str, month: datetime, total: float, active_residents: int, split_total: float):
        self.name = name
        self.month = month
        self.total = total
        self.active_residents = active_residents
        self.split_total = split_total

    def __repr__(self):
        return f"StatementDTO(name={self.name}, month={self.month}, total={self.total}, active_residents={self.active_residents}, split_total={self.split_total})"


class WhatsappMessageDTO:
    """DTO class to contain the entire relevant data to form a whatsapp message"""

    msg = {}

    def __init__(self, statement: StatementDTO, utilities: [], installments: []):
        self.statement = statement
        self.installments = installments
        self.utilities = utilities
        self.populate_message()

    def populate_message(self):
        title = f"*{self.statement.name}*"
        utilities_section = "Utilities:"
        utilities_msg = []
        for i in self.utilities:
            utilities_msg.append(f"{i.type} = RM{i.to_pay}")
        installments_section = "Installments:"
        installments_msg = []
        for i in self.installments:
            installments_msg.append(f"{i.type} = RM{i.to_pay}")
        total_per_person = f"Total per person = RM{self.statement.total:.2f}/{self.statement.active_residents} = *RM{self.statement.split_total:.2f}*"
        self.msg = {
            "header": title,
            "utilities_section_header": utilities_section,
            "utilities_msg_list": utilities_msg,
            "installments_section_header": installments_section,
            "installments_msg_list": installments_msg,
            "closing": total_per_person
        }

    def default_message_formatter(self, api=True) -> str:
        br = "<br>" if api else "\n"
        normal_msg = ""
        normal_msg += self.msg["header"]
        normal_msg += br
        normal_msg += br
        normal_msg += self.msg["utilities_section_header"]
        normal_msg += br
        for i in self.msg["utilities_msg_list"]:
            normal_msg += i
            normal_msg += br
        normal_msg += br

        # only add the installments section if there are active installments for that month
        if len(self.installments) > 0:
            normal_msg += self.msg["installments_section_header"]
            normal_msg += br
            for i in self.msg["installments_msg_list"]:
                normal_msg += i
                normal_msg += br
            normal_msg += br

        normal_msg += self.msg["closing"]
        return normal_msg

    def format_normal_msg(self) -> str:
        return self.default_message_formatter(api=False)

    def format_api_msg(self) -> str:
        return self.default_message_formatter(api=True)

from DTO import StatementDTO
from database import Database
import datetime as dt
import calendar

# data access/update methods designed from service (class) approach for prototyping

# init db instance and database query string
conn = Database()
schema = "sqa"
query = " "


# Read methods
def get_total_residents():
    """Counts how many residents will the statement total be divided with"""
    return conn.count(
        f"select count(*) from {schema}.resident where is_resident IS TRUE"
    )


def get_total_installments(is_active=True):
    """Counts the total credit card installments. Set to active installments by default."""
    return conn.count(
        f"select count(*) from {schema}.installment where is_active IS {is_active}"
    )


def get_installment_details(is_active=True):
    """Retrieves the credit card installment details. Set to active installments by default.
    Returned fields:
        - id : int
        - name : string
        - is_active : boolean
        - total : decimal
        - period : int
        - created_at : datetime.datetime
        - updated_at : datetime.datetime
        - resident_id : int
        - start_date : datetime.date

    """
    return conn.fetch_all(
        f"select * from {schema}.installment where is_active IS {is_active}"
    )


def deactivate_installment(id: int):
    """Deactivates an installment by setting its is_active status to False"""
    conn.save(
        f"update {schema}.installment set is_active = FALSE where id = {id}"
    )


def get_total_utilities():
    """Counts the total utilities."""
    return conn.count(
        f"select count(*) from {schema}.utility"
    )


def get_utility_details():
    """Retrieves the utility details.
    Returned fields:
        - id : int
        - name : string
        - resident_id : int
        - created_at : datetime.datetime
        - updated_at : datetime.datetime
    """
    return conn.fetch_all(
        f"select * from {schema}.utility"
    )


def get_latest_statement():
    """Retrieves the latest statement's generated date. Returns in the format of:

        - YYYY-M-D : datetime.date
    """
    return conn.fetch_one(
        f"select month from {schema}.statement order by month desc"
    )


def get_latest_statement_id():
    """Retrieves the latest statement's id for use of insertion on the
    monthly_installment and monthly_utility tables as foreign keys"""
    return conn.fetch_one(
        f"select id from {schema}.statement order by id desc"
    )[0]


# Insertion methods
def insert_statement(dto: StatementDTO) -> int:
    """Inserts a new statement and returns its id"""

    conn.save(
        f"insert into {schema}.statement (name,month,total,active_residents,split_total) values "
        f"('{dto.name}','{dto.month}',{dto.total},'{dto.active_residents}',{dto.split_total})"
    )

    id = conn.fetch_one(
        f"select id from {schema}.statement order by id desc"
    )[0]  # data returned as a tuple: ({id},)

    return id


def insert_monthly_installment(id: int, installments: []):
    """

        :param id: The ID for the billing statement
        :param installments: A list of AutomationDTOs containing scraped installments' data
        :return: None
        """
    for i in installments:
        conn.save(
            f"insert into {schema}.monthly_installment (statement_id,installment_id,total) values "
            f"('{id}','{i.id}',{i.to_pay})"
        )


def insert_monthly_utility(id: int, utilities: []):
    """

    :param id: The ID for the billing statement
    :param utilities: A list of AutomationDTOs containing scraped utilities' data
    :return: None
    """
    for i in utilities:
        conn.save(
            f"insert into {schema}.monthly_utility (statement_id,utility_id,total) values "
            f"('{id}','{i.id}',{i.to_pay})"
        )


def calculate_new_statement(data: {}) -> StatementDTO:
    """
    Calculates the cumulative total and split totals for a new statement and returns a StatementDTO
    :param data: A dictionary containing keys "utilities" and "installments", which contains a list of those data
    :return: A StatementDTO for the calculated and formatted data
    """
    utilities = data["utilities"]
    installments = data["installments"]

    date = str(dt.date.today()).split("-")[:2]
    name = f"Bill {calendar.month_name[int(date[1])]} {date[0]}"
    month_date = dt.date(int(date[0]), int(date[1]), 1)
    active_residents = get_total_residents()
    total = 0.00

    for i in utilities:
        total += float(i.to_pay)

    for j in installments:
        total += float(j.to_pay)

    split_total = total / active_residents

    # conversion to 2 decimal places
    total = f"{total:.2f}"
    split_total = f"{split_total:.2f}"

    # re-convert to float values
    total = float(total)
    split_total = float(split_total)

    return StatementDTO(
        name=name,
        month=month_date,
        total=total,
        active_residents=active_residents,
        split_total=split_total
    )


def close_connection():
    conn.close_connection()

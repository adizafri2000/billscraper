import os
import pywhatkit
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()


def generate_message(data):
    msg = f"*Bill {datetime.today().strftime('%B')}*\n\nUtilities:\n"
    total_utils = 0.00
    for item in data:
        type = item['type']
        to_pay = float(item['to_pay'])
        tmp_msg = f"{type} = RM{to_pay:.2f}\n"
        msg += tmp_msg
        total_utils += to_pay

    util_per_person = total_utils / 5
    monthly_total_per_person = util_per_person + 200

    msg += f"Total utilities per person = RM{total_utils:.2f}/5 = *RM{util_per_person:.2f}*\n\n"
    msg += f"Sewa per person = RM1000/5 = *RM200*\n\n"
    msg += f"Total per person = *RM{monthly_total_per_person:.2f}*"

    return msg


def sendwhatmsg_instantly(
        phone_no: str,
        message: str,
        wait_time: int = 15,
        tab_close: bool = False,
        close_time: int = 3,
) -> None:
    """Altered version of pywhatkit.sendwhatmsg_instantly where no log files will be saved"""

    from pywhatkit.core import core, exceptions
    import webbrowser as web
    import time
    import pyautogui as pg
    from urllib.parse import quote

    if not core.check_number(number=phone_no):
        raise exceptions.CountryCodeException("Country Code Missing in Phone Number!")

    web.open(f"https://web.whatsapp.com/send?phone={phone_no}&text={quote(message)}")
    time.sleep(4)
    pg.click(core.WIDTH / 2, core.HEIGHT / 2)
    time.sleep(wait_time - 4)
    pg.press("enter")
    if tab_close:
        core.close_tab(wait_time=close_time)


def send_whatsapp_to_me(msg: str):
    mynum = os.getenv("mynum")
    sendwhatmsg_instantly(mynum, msg, tab_close=True)

def send_whatsapp_group(msg: str):
    group_id = os.getenv("ws_group_id")
    pywhatkit.sendwhatmsg_to_group_instantly(group_id,msg,tab_close=True)

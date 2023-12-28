import os
import pywhatkit
from datetime import datetime
from dotenv import load_dotenv
import requests

load_dotenv()

service_url = os.environ["ws_api_url"]
ws_api_id = os.environ["ws_api_id"]


def send_whatsapp_message(content: str):
    """Sends a message to the WhatsApp API"""
    params = {
        "number": ws_api_id,
        "content": content
    }
    headers = {
        "accept": "application/json",
    }
    res = requests.post(service_url, params=params)
    return res


@DeprecationWarning
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

@DeprecationWarning
def send_whatsapp_to_me(msg: str):
    mynum = os.getenv("mynum")
    sendwhatmsg_instantly(mynum, msg, tab_close=True)
    # pywhatkit.sendwhats_image(
    #     receiver=mynum,
    #     img_path="QR_CODE.jpeg",
    #     tab_close=True,
    #     caption=msg
    # )

@DeprecationWarning
def send_whatsapp_group(msg: str):
    group_id = os.getenv("ws_group_id")
    pywhatkit.sendwhatmsg_to_group_instantly(
        group_id=group_id,
        message=msg,
        tab_close=True)

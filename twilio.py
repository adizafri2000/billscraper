import os

from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

account_sid = os.getenv("TWILIO_account_sid")
auth_token = os.getenv("TWILIO_auth_token")
client = Client(account_sid, auth_token)
msg_from = "whatsapp:+14155238886"

def send_message(body,to):
    to = f"whatsapp{to}"
    client.messages.create(
        from_=msg_from,
        body=body,
        to=to
    )
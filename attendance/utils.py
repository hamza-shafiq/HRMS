import os

import certifi
import requests
from dotenv import load_dotenv
from slack_bolt import App

load_dotenv()
os.environ['SSL_CERT_FILE'] = certifi.where()

SLACK_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
SIGNING_SECRET = os.environ.get("SLACK_SIGNING_SECRET")
SLACK_APP_LEVEL_TOKEN = os.environ.get("SLACK_APP_LEVEL_TOKEN")

app = App(token=SLACK_TOKEN, signing_secret=SIGNING_SECRET)

def send_leave_request_message(name, start_date, end_date, leave_type, status, team_lead_name):

    slack_url = "https://slack.com/api/chat.postMessage"
    headers = {
        "Authorization": f"Bearer {SLACK_TOKEN}",
        "Content-Type": "application/json"
    }


    if status == "Pending" :
        if start_date != end_date:
            message = (
                f"📢 *Leave Request*:\n"
                f"*{name}* has requested *{leave_type}* from *{start_date}* to *{end_date}*.\n"
                f"Team Lead: *{team_lead_name}*"
            )
        else:
            message = (
                f"📢 *Leave Request*:\n"
                f"*{name}* has requested *{leave_type}* on *{start_date}*.\n"
                f"Team Lead: *{team_lead_name}*"
            )
    elif status == "Approved"  :
        if start_date != end_date:
            message = (
                f"✅ *Leave Request Approved*:\n"
                f"*{name}*'s request for *{leave_type}* from *{start_date}* to *{end_date}* has been approved.\n"
                f"Approved by:  *{team_lead_name}*"
            )
        else:
            message = (
                f"✅ *Leave Request Approved*:\n"
                f"*{name}*'s request for *{leave_type}* on *{start_date}* has been approved.\n"
                f"Approved by: *{team_lead_name}*"
            )

    payload = {
        "channel": "C088CPH13K5",
        "text": message,
        "mrkdwn": True
    }

    response = requests.post(slack_url, json=payload, headers=headers)
    if response.status_code == 200 and response.json().get("ok"):
        print("Message sent successfully!")
    else:
        print(f"Failed to send message: {response.text}")

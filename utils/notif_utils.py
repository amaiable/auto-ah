import requests
from api_utils import make_post_request
from dotenv import load_dotenv
import os

def send_notification(message: str) -> None:

    load_dotenv()
    data = {
        "token": os.getenv("PUSHOVER_TOKEN"),
        "user": os.getenv("PUSHOVER_USER_KEY"),
        "message": message

    }
    make_post_request("https://api.pushover.net/1/messages.json", data=data)
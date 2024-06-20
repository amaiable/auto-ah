import requests
import json
import time
import random
from typing import Dict

MAX_RETRIES = 5

def make_get_request(endpoint: str) -> Dict[any, any]:

    retry_delay = 1
    
    for attempt in range(0, MAX_RETRIES):
        try:
            response = requests.get(endpoint)
            response.raise_for_status()
            return response.json()
        except requests.RequestException:
            time.sleep(retry_delay)
            retry_delay *= 2
            retry_delay += random.uniform(0, 1)

    return Exception("Maximum retry attempts have been made with no success")
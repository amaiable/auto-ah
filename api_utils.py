import requests
import json

def make_get_request(endpoint: str):

    # TODO: Implement exponential backoff

    response = requests.get(endpoint)
    formatted_data = json.loads(response.text)

    if "success" not in formatted_data:
        raise KeyError("Success flag not found in API response", formatted_data)
    elif not formatted_data["success"]:
        raise Exception("GENERIC API FAILED ERROR")

    return formatted_data
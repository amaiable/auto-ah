"""
Grabs data from API of my active / completed auction house listings
"""

import requests
import json
from collections import defaultdict
from dotenv import load_dotenv
import os

DEFAULT_NUM_AUCTION_SLOTS = 14

def get_player_auctions(api_key: str, player_uuid: str) -> dict:

    endpoint = f"https://api.hypixel.net/v2/skyblock/auction?key={api_key}&player={player_uuid}"
    response = requests.get(endpoint)
    formatted_data = json.loads(response.text)

    if not formatted_data["success"]:
        print("get_player_auctions call failed with", api_key, player_uuid)

        # TODO: Add more handling to this
        raise Exception("API request failed")
    return formatted_data["auctions"]

def get_formatted_auction_data() -> str:
    load_dotenv()
    my_api_key = os.getenv("API_KEY")
    my_uuid = os.getenv("UUID")

    my_ah_data = get_player_auctions(my_api_key, my_uuid)

    # Process auctions for active and completed
    active_auctions = defaultdict(lambda: 0)
    active_auction_count = 0
    completed_auctions = defaultdict(lambda: 0)

    for listing in my_ah_data:
        # Only handling bin auctions in this script
        if listing["bin"] is False:
            continue

        item_name = listing["item_name"]
        if len(listing["bids"]) == 1:
            completed_auctions[item_name] += 1
        else:
            active_auctions[item_name] += 1
            active_auction_count += 1

    output_string = "---------------------------------------\n"
    output_string += "AH Data\n"
    output_string += "---------------------------------------\n"
    output_string += "Active auctions\n"
    output_string += "---------------------------------------\n"

    if len(active_auctions) == 0:
        output_string += "None\n"
    else:
        for item_name, count in active_auctions.items():
            output_string += f"{item_name}: {count}\n"

    output_string += "---------------------------------------\n"
    output_string += "Completed auctions\n"
    output_string += "---------------------------------------\n"

    if len(completed_auctions) == 0:
        output_string += "None\n"
    else:
        for item_name, count in completed_auctions.items():
            output_string += f"{item_name}: {count}\n"

    output_string += "---------------------------------------\n"

    output_string += f"{DEFAULT_NUM_AUCTION_SLOTS - active_auction_count} auction house {'slots' if DEFAULT_NUM_AUCTION_SLOTS - active_auction_count != 1 else 'slot'} available\n"
    output_string += "---------------------------------------\n"

    return output_string

if __name__ == "__main__":
    print(get_formatted_auction_data())
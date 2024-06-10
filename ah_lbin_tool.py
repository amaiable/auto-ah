"""
Finds the k lowest bin price in auction house for specified parameters
"""

import requests
import json

def get_lowest_bin(item_name: str) -> int:

    endpoint = f"https://api.hypixel.net/v2/skyblock/auctions"
    response = requests.get(endpoint)
    formatted_data = json.loads(response.text)

    if not formatted_data["success"]:
        print("get_lowest_bin call failed with", item_name)

        # TODO: Add more handling to this
        raise Exception("API request failed")

    page_count = formatted_data["totalPages"]
    print(f"There are a total of {page_count} pages")

    best_price = float("inf")

    for i in range(0, page_count):
        print("Currently on page", i)
        endpoint = f"https://api.hypixel.net/v2/skyblock/auctions?page={i}"
        response = requests.get(endpoint)
        formatted_data = json.loads(response.text)

        if not formatted_data["success"]:
            print("get_lowest_bin call failed with", item_name)

            # TODO: Add more handling to this
            raise Exception("API request failed")
        
        if formatted_data["page"] != i:
            raise IndexError

        auctions = formatted_data["auctions"]

        bin_name_auctions = [auction for auction in auctions if item_name in auction["item_name"] and auction["bin"] is True]
        if len(bin_name_auctions) == 0:
            continue

        bin_name_auctions.sort(key=lambda x: x["starting_bid"])

        lbin_auction = bin_name_auctions[0]
        best_price = min(best_price, lbin_auction["starting_bid"])
    
    return best_price

if __name__ == "__main__":
    print(get_lowest_bin("Shadow Assassin Cloak"))
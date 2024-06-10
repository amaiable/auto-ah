"""
Finds the lowest bin price in auction house for specified parameters

Using multithreading to quickly go through the different pages (> 90 seconds -> < 30 seconds)
"""

import requests
import json
from threading import Lock, Thread

def fetch_items(item_name: str, i: int, results: list, lock) -> None:

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

    page_bin_name_auctions = [auction for auction in auctions if item_name in auction["item_name"].lower() and auction["bin"] is True]
    if len(page_bin_name_auctions) == 0:
        return

    page_bin_name_auctions.sort(key=lambda x: x["starting_bid"])

    results.append(page_bin_name_auctions[0])


def get_lowest_bin(item_name: str) -> int:

    print(f"Getting lowest price for item: {item_name}")

    item_name = item_name.lower()

    endpoint = f"https://api.hypixel.net/v2/skyblock/auctions"
    response = requests.get(endpoint)
    formatted_data = json.loads(response.text)

    if not formatted_data["success"]:
        print("get_lowest_bin call failed with", item_name)

        # TODO: Add more handling to this
        raise Exception("API request failed")

    page_count = formatted_data["totalPages"]

    print(f"There are a total of {page_count} pages")

    results = []
    threads = []
    lock = Lock()

    for i in range(0, page_count):
        thread = Thread(target=fetch_items, args=(item_name, i, results, lock))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
    
    return min([result["starting_bid"] for result in results])

if __name__ == "__main__":
    # ✪✪✪✪✪
    from time import time
    start = time()
    print(f"{get_lowest_bin('Handle'):,}")
    end = time()
    print(f"Took {end - start} seconds")
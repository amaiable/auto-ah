"""
Grabs data from API for prices of spirit wing / spirit bone

Item names:
Spirit wing: "SPIRIT_WING"
Spirit bone: "SPIRIT_BONE"

TODO: Add some analysis for pricing anomalies
"""

import requests
import json

def get_bz_info_item(item_name: str) -> dict:

    endpoint = f"https://api.hypixel.net/v2/skyblock/bazaar"
    response = requests.get(endpoint)
    formatted_data = json.loads(response.text)

    if not formatted_data["success"]:
        print("get_bz_info_item call failed with", api_key, player_uuid)

        # TODO: Add more handling to this
        raise Exception("API request failed")
    products = formatted_data["products"]

    if item_name not in products:
        print(item_name, "is not a valid item name")

        # TODO: Add more handling to this
        raise KeyError("Cannot find itemname")

    relevant_item_quick_data = products[item_name]["quick_status"]

    prices = {"ask": relevant_item_quick_data["buyPrice"], "bid": relevant_item_quick_data["sellPrice"]}

    return prices



def get_formatted_spirit_item_data() -> str:

    spirit_bone_prices = get_bz_info_item("SPIRIT_BONE")
    spirit_wing_prices = get_bz_info_item("SPIRIT_WING")

    output_string = "---------------------------------------\n"
    output_string += "Spirit Item BZ Data\n"
    output_string += "---------------------------------------\n"
    output_string += "Spirit Wing\n"
    output_string += "---------------------------------------\n"

    output_string += f"Bid: {spirit_bone_prices['bid']} / Ask: {spirit_bone_prices['ask']}\n"

    output_string += "---------------------------------------\n"
    output_string += "Spirit Bone\n"
    output_string += "---------------------------------------\n"

    output_string += f"Bid: {spirit_wing_prices['bid']} / Ask: {spirit_wing_prices['ask']}\n"

    output_string += "---------------------------------------\n"

    output_string += f"2x Spirit Bone + 1x Spirit Wing Insta-Buy = ${2 * spirit_bone_prices['ask'] + spirit_wing_prices['ask']}\n"
    output_string += "---------------------------------------\n"

    return output_string

if __name__ == "__main__":
    print(get_formatted_spirit_item_data())
"""
File for running all scripts in one go
"""

from ah_flip_tool import get_formatted_auction_data
from bz_spirit_tool import get_formatted_spirit_item_data

def main():
    print(get_formatted_auction_data())
    print(get_formatted_spirit_item_data())

if __name__ == "__main__":
    main()
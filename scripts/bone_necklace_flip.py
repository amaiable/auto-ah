from time import time

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from bazaar_utils import BazaarUtil

INSTANT_FLAG = False

def main():
    bz_util = BazaarUtil()

    spirit_bone_prices = bz_util.get_item_prices("Spirit Bone")
    spirit_wing_prices = bz_util.get_item_prices("Spirit Wing")
    soul_string_prices = bz_util.get_item_prices("Soul String")
    essence_wither_prices = bz_util.get_item_prices("Essence Wither")
    thorn_fragment_prices = bz_util.get_item_prices("Thorn Fragment")

    if INSTANT_FLAG is True:
        price_tag = "ask"
    else:
        price_tag = "bid"

    buy_all_price = 2 * spirit_bone_prices[price_tag] + 1 * spirit_wing_prices[price_tag] \
                            + 96 * soul_string_prices[price_tag] + 8 * thorn_fragment_prices[price_tag] \
                            + 370 * essence_wither_prices[price_tag] + 35000

    print(buy_all_price)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "INSTANT":
        INSTANT_FLAG = True

    start = time()
    main()
    end = time()
    print(f"Process took {end - start} seconds to complete")
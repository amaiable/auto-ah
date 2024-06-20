from api_utils import make_get_request
from threading import Lock, Thread
from typing import List, Dict

class AuctionHouseUtil:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def get_active_auctions(self) -> List[any]:
        ah_endpoint = "https://api.hypixel.net/v2/skyblock/auctions"
        ah_data = make_get_request(ah_endpoint)

        page_count = ah_data["totalPages"]

        def fetch_page(page_num: int, auctions: list, lock: Lock) -> None:
            page_endpoint = f"https://api.hypixel.net/v2/skyblock/auctions?page={page_num}"
            page_data = make_get_request(page_endpoint)
            page_auctions = page_data["auctions"]
            with lock:
                auctions.extend(page_auctions)

        threads = []
        lock = Lock()

        auctions = []

        for page_num in range(0, page_count):
            thread = Thread(target=fetch_page, args=(page_num, auctions, lock))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        return auctions

    def get_auctions_by_player_uuid(self, player_uuid: str) -> List[any]:
        ah_endpoint = f"https://api.hypixel.net/v2/skyblock/auction?key={self.api_key}&player={player_uuid}"
        player_ah_data = make_get_request(ah_endpoint)
        
        return player_ah_data["auctions"]

    def get_auctions_by_item_name(self, item_name: str, bin_flag: bool = True, modifiers: List[str] = []) -> List[any]:
        item_name = item_name.lower()
        modifiers = [modifier.lower() for modifier in modifiers]

        active_auctions = self.get_active_auctions()

        def item_name_filter(auction: Dict[any, any]) -> bool:
            lower_auction_item_name = auction["item_name"].lower()
            return item_name in lower_auction_item_name

        def modifier_filter(auction: Dict[any, any]) -> bool:
            lower_auction_item_name = auction["item_name"].lower()
            lower_auction_item_lore = auction["item_lore"].lower()
            lower_auction_tier = auction["tier"].lower()
            for modifier in modifiers:
                if modifier not in lower_auction_item_name and modifier not in lower_auction_item_lore and modifier not in lower_auction_tier:
                    return False
            return True

        return [auction for auction in active_auctions if item_name_filter(auction) and modifier_filter(auction) and auction["bin"] == bin_flag]
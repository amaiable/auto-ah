from api_utils import make_get_request
from threading import Lock, Thread
from typing import List

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

    def get_auctions_by_item_name(self, item_name: str, )
from functools import cache
from heapq import heappush, heappop

from api_utils import make_get_request

BAZAAR_ENDPOINT = "https://api.hypixel.net/v2/skyblock/bazaar"

class BazaarUtil:
    def __init__(self, api_key: str):
        self.api_key = api_key

        self.bazaar_data = {}
        self.bazaar_produtcs = []
        self.bazaar_item_names = set()
        self.refresh_bazaar_data()

    def refresh_bazaar_data(self) -> None:
        self.bazaar_data = make_get_request(BAZAAR_ENDPOINT)
        self.bazaar_products = self.bazaar_data["products"]
        self.bazaar_item_names = set(self.bazaar_products.keys())

    def search_item_names(self, query: str, num_results: int = 5) -> List[str]:
        """
        Uses edit distance DP algorithm to find the num_results items with the most similar name
        TODO: edit distance might not be the best algorithm for this, as it may favor shorter (but incorrect) names
        """

        # TODO: Need to unit test this
        def edit_distance(s1: str, s2: str) -> int:

            @cache
            def solve(i: int, j: int) -> int:
                if i == len(s1) or j == len(s2):
                    return len(s1) + len(s2) - i - j
                elif s1[i] == s2[j]:
                    return solve(i + 1, j + 1)
                else:
                    return 1 + min(solve(i + 1, j), solve(i, j + 1), solve(i + 1, j + 1))

            return solve(0, 0)

        query = query.lower()

        word_distances = []

        for item_name in self.bazaar_item_names:
            item_name = item_name.lower()
            word_distance = edit_distance(query, item_name)

            if word_distance == 0:
                return [item_name]

            heappush(word_distances, (-word_distance, item_name))
            if len(results) > k:
                heappop(word_distances)

        return [item_name for _, item_name in word_distances]

    def get_item_prices(self, query: str) -> Dict[str, float]:

        if query not in self.bazaar_item_names:
            raise KeyError(f"Cannot find item: '{query}'. Perhaps you meant one of {self.search_item_names(query)}")

        self.refresh_bazaar_data()

        bid_price = self.bazaar_products[query]["quick_status"]["sellPrice"]
        ask_price = self.bazaar_products[query]["quick_status"]["buyPrice"]

        return {"bid": bid_price, "ask": ask_price}

    def get_item_top_order_data(self, query: str) -> Dict[str, List[Dict[str, float]]]:

        if query not in self.bazaar_item_names:
            raise KeyError(f"Cannot find item: '{query}'. Perhaps you meant one of {self.search_item_names(query)}")

        self.refresh_bazaar_data()

        bid_orders = self.bazaar_products[query]["sell_summary"]
        ask_orders = self.bazaar_products[query]["buy_summary"]

        # Clean data (remove unnecessary data and change key names)
        def clean_order(raw_order_info: Dict[str, float]) -> Dict[str, float]:
            cleaned_order_info = {}
            cleaned_order_info["quantity"] = raw_order_info["amount"]
            cleaned_order_info["unit_price"] = raw_order_info["pricePerUnit"]
            return cleaned_order_info

        bid_orders = [cleaned_order_info(raw_order_info) for raw_order_info in bid_orders]
        ask_orders = [cleaned_order_info(raw_order_info) for raw_order_info in ask_orders]
        
        return {"bid_orders": bid_orders, "ask_orders": ask_orders}

    def find_mean_reversion_flips(self) -> any:
        """
        Using recent historical data, find short term flip from expected mean reverting price behaviour
        """
        pass
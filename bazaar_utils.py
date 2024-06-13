from functools import cache
from heapq import heappush, heappop

from api_utils import make_get_request

class BazaarUtil:
    def __init__(self, api_key: str):
        self.api_key = api_key

        self.bazaar_item_names = []
        bazaar_data = make_get_request(f"https://api.hypixel.net/v2/skyblock/bazaar")
        for product_name in bazaar_data["products"]:
            self.bazaar_item_names.append(product_name)

    def search_items(self, query: str, num_results: int = 5):

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
            heappush(word_distances, (edit_distance(query, item_name)))
            if len(results) > k:
                heappop(word_distances)

        return [item_name for _, item_name in word_distances]


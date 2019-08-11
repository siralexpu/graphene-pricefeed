import sys
import requests
from . import FeedSource, _request_headers


class Okcoin(FeedSource):
    def _fetch(self):
        feed = {}
        for base in self.bases:
            for quote in self.quotes:
                if quote == base:
                    continue
                url = "https://www.okcoin.com/api/spot/v3/instruments/{}-{}/ticker".format(quote.upper(), base.upper())
                response = requests.get(url=url, headers=_request_headers, timeout=self.timeout)
                result = response.json()
                self.add_rate(feed, base, quote, float(result["last"]), float(result["base_volume_24h"]))
                feed[self.alias(base)]["response"] = result
        return feed

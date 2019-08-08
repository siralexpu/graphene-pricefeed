import requests
from . import FeedSource, _request_headers


class Zb(FeedSource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.base_url = getattr(self, 'url', 'http://api.zb.com')

    def _fetch(self):
        feed = {}
        url = "{base_url}/data/v1/ticker?market={quote}_{base}"
        for base in self.bases:
            for quote in self.quotes:
                if base == quote:
                    continue
                response = requests.get(
                    url=url.format(base_url=self.base_url, base=base, quote=quote),
                    headers=_request_headers,
                    timeout=self.timeout)
                result = response.json()
                if "ticker" in result and \
                    "last" in result["ticker"] and \
                    "vol" in result["ticker"]:
                    self.add_rate(feed, base, quote, float(result["ticker"]["last"]), float(result["ticker"]["vol"]))
                else:
                    print("\nFetched data from {0} is empty!".format(type(self).__name__))
                    continue
        return feed

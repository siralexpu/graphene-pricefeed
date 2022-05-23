import requests
from . import FeedSource, _request_headers

class Goldprice(FeedSource):
    def _fetch(self):
        feed = {}
        for base in self.bases:
            for quote in self.quotes:
                if quote == base:
                    continue
                pair = '{}-{}'.format(base.upper(), quote.upper())
                url = "http://data-asg.goldprice.org/GetData/{}/1".format(pair)
                r = requests.get(url=url, headers=_request_headers, timeout=self.timeout)
                r = r.json()
                response = float(r[0].split(',')[1])
                price_troyounce = response
                self.add_rate(feed, base, quote, float(price_troyounce), 1.0)
        return feed

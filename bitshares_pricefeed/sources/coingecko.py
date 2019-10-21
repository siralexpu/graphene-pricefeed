import requests
from . import FeedSource, _request_headers

class CoinGecko(FeedSource):
    def _fetch(self):
        feed = {}
        formated_bases = ','.join([ base.lower() for base in self.bases ])
        formated_quotes = ','.join([ quote.lower() for quote in self.quotes ])
        url = "https://api.coingecko.com/api/v3/simple/price?ids={}&vs_currencies={}&include_24hr_vol=true".format(formated_quotes, formated_bases)
        response = requests.get(url=url, headers=_request_headers, timeout=self.timeout)
        result = response.json()
        for quote in self.quotes:
            for base in self.bases:
                low_quote = quote.lower()
                low_base = base.lower()
                if low_quote in result and low_base in result[low_quote]:
                    ticker = float(result[low_quote][low_base])
                    volume = float(result[low_quote][low_base + '_24h_vol']) / ticker
                    self.add_rate(feed, base, quote, ticker, volume)
        return feed

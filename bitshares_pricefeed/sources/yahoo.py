import requests
from . import FeedSource, _request_headers
import json

# https://finance.yahoo.com
# pylint: disable=no-member
class Yahoo(FeedSource):  # Yahoo direct request
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.feed = {}


    def _request(self, quote_base, raw):
        post_x = "=X" if (raw == False) else ""

        url = "https://query1.finance.yahoo.com/v10/finance/quoteSummary/%s?modules=price" % (quote_base + post_x)
        response = requests.get(url=url, headers=_request_headers, timeout=self.timeout)

        return response


    def _checkAdd(self, quote, base, response, result):

        if (response.status_code != 200):
            raise Exception(json.loads(response.text)['quoteSummary']['error']['description'])

        if (response.status_code == 200) and (result['quoteSummary']['error'] == None):
            if quote == base:
                return
            curr = 1 / float(result['quoteSummary']['result'][0]['price']['regularMarketPrice']['raw'])
            self.add_rate(self.feed, quote, base, curr, 1.0)
            # for volume: regularMarketVolume
        else:
            raise Exception(json.loads(response.text)['quoteSummary']['error']['description'])


    def _fetch(self):
        for base in self.bases:
            for quote in self.quotes:
                if quote == base:
                    continue

                response = self._request(quote + base, False)
                result = response.json()

                self._checkAdd(quote, base, response, result)
                # result['quoteSummary']['result'][0]['price']['regularMarketPrice']['raw']

        # For Separate Quotes
        for market in self.separate_quotes:
            quote, base = market.split(":")
            for dataset in self.separate_quotes[market]:
                response = self._request(dataset, True)
                result = response.json()
                self._checkAdd(quote, base, response, result)

        return self.feed

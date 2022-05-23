import requests
from . import FeedSource, _request_headers

# https://www.currate.ru
# pylint: disable=no-member
class Currate(FeedSource):  # C 10.05.2019 введены ограничения 1000 запросов в сутки по API ключу
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not hasattr(self, "api_key"):
            raise Exception("Currate FeedSource requires 'api_key'")

    def _fetch(self):
        feed = {}
        pairs_string = ''

        for base in self.bases:
            for quote in self.quotes:
                if quote == base:
                    continue
                if pairs_string == '':
                    pairs_string = quote + base
                else:
                    pairs_string = pairs_string + "," + quote + base

        url = "https://currate.ru/api/?get=rates&pairs=%s&key=%s" % (pairs_string, self.api_key)
        response = requests.get(url=url, headers=_request_headers, timeout=self.timeout)
        result = response.json()

        if (result.get("status") == 200) and (result['message'] == 'rates') and (len(result.get("data")) != 0):
            for base in self.bases:
                for quote in self.quotes:
                    if quote == base:
                        continue
                    self.add_rate(feed, base, quote, 1 / float(result["data"][base + quote]), 1.0)
        else:
            raise Exception(result.get("message"))

        return feed

import requests
from . import FeedSource, _request_headers


class Biki(FeedSource):
    def _fetch(self):
        feed = {}
        url = "https://openapi.biki.cc/open/api/get_ticker?symbol={quote}{base}"
        for base in self.bases:
            for quote in self.quotes:
                if quote == base:
                    continue
                response = requests.get(url=url.format(
                    quote=quote,
                    base=base
                ), headers=_request_headers, timeout=self.timeout)
                result = response.json()
                if 'msg' in result and result['msg'] != 'suc':
                    continue
                self.add_rate(feed, base, quote, float(result['data']["last"]), float(result['data']["vol"]))
        return feed
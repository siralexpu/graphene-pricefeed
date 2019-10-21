from bitshares_pricefeed.sources.coingecko import CoinGecko

def test_coingecko_fetch(checkers):
    source = CoinGecko(quotes=['bitshares', 'bitcoin'], bases=['EUR', 'USD'], aliases={'bitshares': 'BTS', 'bitcoin': 'BTC'}) 
    feed = source.fetch()
    checkers.check_feed(feed, ['BTS:EUR', 'BTS:USD', 'BTC:USD', 'BTC:EUR'])



from bitshares_pricefeed.pricefeed import Feed

config = 'bitshares_pricefeed/examples/norm.yaml'

def test_norm_computation(conf, checkers):
    feed = Feed(conf)
    feed.fetch()
    feed.derive({'URTHR', 'VERTHANDI', 'SKULD'})
    prices = feed.get_prices()
    checkers.check_price(prices, 'URTHR', 'BTS', 0.1)
    checkers.check_price(prices, 'VERTHANDI', 'BTS', 0.1)
    checkers.check_price(prices, 'SKULD', 'BTS', 0.1)

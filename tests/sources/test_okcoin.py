from bitshares_pricefeed.sources.okcoin import Okcoin

def test_okcoin_fetch(checkers):
    source = Okcoin(quotes=['BTC'], bases=['USD', 'EUR']) 
    feed = source.fetch()
    checkers.check_feed(feed, ['BTC:USD', 'BTC:EUR'])



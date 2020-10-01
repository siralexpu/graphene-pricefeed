from bitshares_pricefeed.sources.biki import Biki

def test_biki_fetch(checkers):
    source = Biki(quotes=['BTS', 'BTC'], bases=['USDT'], aliases={'USDT':'USD'}) 
    feed = source.fetch()
    checkers.check_feed(feed, ['BTS:USD', 'BTC:USD'])



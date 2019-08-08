from bitshares_pricefeed.sources.bitshares_orderbook import BitsharesOrderbook

def test_bitsharesorderbook_fetch(checkers):
    source = BitsharesOrderbook(assets=['USD'], quotes=['USD'], bases=['BTS'], mode='center_price', quote_volume=100)
    feed = source.fetch()
    checkers.check_feed(feed, ['USD:BTS'])



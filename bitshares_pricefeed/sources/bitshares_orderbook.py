import logging
import math

from . import FeedSource

log = logging.getLogger(__name__)


class BitsharesOrderbook(FeedSource):
    """
        This price source uses bitshares orderbooks to calculate the price. The idea is to provide price based on
        ordersbooks liquidity and depth.

        Properties used by this feed source:
        - self.mode: price calculation mode
          - "center_price": measure bids/asks depth and calculate center price. In this mode borrowers may be force
            settled at price which is higher than highest_bid. Consider setting "Force Settlement Offset" in bitasset
            settings.
          - "buy_support": measure depth of bids and calculate buy support price. In this mode borrowers are in more
            safety because force settlements will be performed at price lower than highest_bid price.
        - self.quote_volume: measure orderbook for this depth of QUOTE asset volume to calculate price. We don't use
          similar self.base_volume param because BASE asset is different across several markets, so the comparison is
          disturbed in such case.

         For example, we have a smartcoin FOO which is backed by BTS, and UIAs xxx.FOO and yyy.FOO. We want to provide
         pricefeed for FOO based on orderbooks of xxx.FOO and yyy.FOO in various pairs with BTS, BTC, CNY, USD and so
         on. Actually we can use orderbooks of FOO itself too.

    """

    def _fetch(self):
        from bitshares.market import Market
        self.fetch_depth = 50
        feed = {}
        for base in self.bases:
            for quote in self.quotes:
                if quote == base:
                    continue

                market = Market("{}/{}".format(quote, base))
                price = 0
                volume = 0

                if self.mode == 'center_price':
                    price, volume = self.get_market_center_price(market, quote_amount=self.quote_volume)
                elif self.mode == 'buy_support':
                    price, volume = self.get_market_buy_price(market, quote_amount=self.quote_volume)
                else:
                    raise Exception('Unsupported mode given')

                # If measurement depth was given in BASE, recalc volume to QUOTE
                # TODO: self.base_volume is officially unsupported but still can be used after minimal modifications
                quote_volume = volume
                #if self.base_volume > self.quote_volume:
                #    quote_volume = volume / price

                if price:
                    log.info('Price on market {}/{}: {}, volume: {}'.format(quote, base, price, volume))
                    self.add_rate(feed, base, quote, price, volume)
        return feed

    def get_market_buy_price(self, market, quote_amount=0, base_amount=0):
        """ Returns the BASE/QUOTE price for which [depth] worth of QUOTE could be sold, enhanced with
            moving average or weighted moving average. Most of this method is taken from DEXBot

            :param bitshares.Market: Market instance
            :param float | quote_amount:
            :param float | base_amount:
            :return: tuple with ("price as float", volume) where volume is actual base or quote volume
        """
        # In case amount is not given, return price of the highest buy order on the market
        if quote_amount == 0 and base_amount == 0:
            raise Exception("quote_amount or base_amount must be given")

        # Like get_market_sell_price(), but defaulting to base_amount if both base and quote are specified.
        asset_amount = base_amount

        """ Since the purpose is never get both quote and base amounts, favor base amount if both given because
            this function is looking for buy price.
        """
        if base_amount > quote_amount:
            base = True
        else:
            asset_amount = quote_amount
            base = False

        market_orders = market.orderbook(self.fetch_depth)['bids']
        market_fee = market['base'].market_fee_percent

        target_amount = asset_amount * (1 + market_fee)

        quote_amount = 0
        base_amount = 0
        missing_amount = target_amount

        for order in market_orders:
            if base:
                # BASE amount was given
                if order['base']['amount'] <= missing_amount:
                    quote_amount += order['quote']['amount']
                    base_amount += order['base']['amount']
                    missing_amount -= order['base']['amount']
                else:
                    base_amount += missing_amount
                    quote_amount += missing_amount / order['price']
                    break
            elif not base:
                # QUOTE amount was given
                if order['quote']['amount'] <= missing_amount:
                    quote_amount += order['quote']['amount']
                    base_amount += order['base']['amount']
                    missing_amount -= order['quote']['amount']
                else:
                    base_amount += missing_amount * order['price']
                    quote_amount += missing_amount
                    break

        # Prevent division by zero
        if not quote_amount:
            return (0.0, 0)

        return (base_amount / quote_amount, base_amount if base else quote_amount)

    def get_market_sell_price(self, market, quote_amount=0, base_amount=0):
        """ Returns the BASE/QUOTE price for which [depth] worth of QUOTE could be bought, enhanced with
            moving average or weighted moving average. Most of this method is taken from DEXBot

            :param bitshares.Market: Market instance
            :param float | quote_amount:
            :param float | base_amount:
            :return: tuple with ("price as float", volume) where volume is actual base or quote volume
        """
        # In case amount is not given, return price of the highest buy order on the market
        if quote_amount == 0 and base_amount == 0:
            raise Exception("quote_amount or base_amount must be given")

        asset_amount = quote_amount
        """ Since the purpose is never get both quote and base amounts, favor quote amount if both given because
            this function is looking for sell price.
        """
        if quote_amount > base_amount:
            quote = True
        else:
            asset_amount = base_amount
            quote = False

        market_orders = market.orderbook(self.fetch_depth)['asks']
        market_fee = market['quote'].market_fee_percent

        target_amount = asset_amount * (1 + market_fee)

        quote_amount = 0
        base_amount = 0
        missing_amount = target_amount

        for order in market_orders:
            if quote:
                # QUOTE amount was given
                if order['quote']['amount'] <= missing_amount:
                    quote_amount += order['quote']['amount']
                    base_amount += order['base']['amount']
                    missing_amount -= order['quote']['amount']
                else:
                    base_amount += missing_amount * order['price']
                    quote_amount += missing_amount
                    break
            elif not quote:
                # BASE amount was given
                if order['base']['amount'] <= missing_amount:
                    quote_amount += order['quote']['amount']
                    base_amount += order['base']['amount']
                    missing_amount -= order['base']['amount']
                else:
                    base_amount += missing_amount
                    quote_amount += missing_amount / order['price']
                    break

        # Prevent division by zero
        if not quote_amount:
            return (0.0, 0)

        return (base_amount / quote_amount, quote_amount if quote else base_amount)

    def get_market_center_price(self, market, base_amount=0, quote_amount=0):
        """ Returns the center price of market.

            :param bitshares.Market: Market instance
            :param float | base_amount:
            :param float | quote_amount:
            :return tuple: Tuple with market center price as float, volume in buy or sell side which is lower
        """
        center_price = None
        buy_price, buy_volume = self.get_market_buy_price(market, quote_amount=quote_amount,
                                              base_amount=base_amount)
        sell_price, sell_volume = self.get_market_sell_price(market, quote_amount=quote_amount,
                                                base_amount=base_amount)
        if ((buy_price is None or buy_price == 0.0) or
            (sell_price is None or sell_price == 0.0)):
                return (0, 0)

        center_price = buy_price * math.sqrt(sell_price / buy_price)        
        return (center_price, min(buy_volume, sell_volume))


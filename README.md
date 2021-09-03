# Price Feed Script for Graphene blockchain

## Installation 

### Installation using Docker

Build docker image:
```
cd ~
git clone https://github.com/graphene-blockchain/graphene-pricefeed.git
cd graphene-pricefeed
docker build -t graphene-pricefeed .
```

### Alternative manual installation on Ubuntu 16.04 LTS or similar.

Install globally:

```
cd ~
git clone https://github.com/graphene-blockchain/graphene-pricefeed.git
cd graphene-pricefeed
python setup.py install
```

Or in a dedicated virtualenv environment:

```
cd ~
git clone https://github.com/graphene-blockchain/graphene-pricefeed.git
cd graphene-pricefeed
pip install virtualenv 
virtualenv -p python3 wrappers_env/ 
source wrappers_env/bin/activate
python setup.py install
```

### Create the configuration file:

You can generate a sample configuration file using:

```
graphene-pricefeed create
```
Or copy one from the `examples` directory:

File | Description
 --- | --- 
[default](examples/default.yaml) | Default configuration generated by `create` command. Use to publish all the main Graphene gp-assets.

Add a feed producer name to the `config.yml` file just created:

```
vim config.yml
# The producer name(s)
producer: your_witness_name
```
### Manual publication

IF you use docker image you can run:

```
docker run -v /path/to/config.yml:/config/config.yml graphene-pricefeed update --active-key=XXXXXXX
```

If you installed graphene-pricefeed locally use:
```
graphene-pricefeed update --active-key=XXXXXXX
```

See [help](#help) for the full description of the command.

Above solution will pass active key credentials on the command line, if you want to reuse a pybitshares wallet see instruction in [Use pybitshares encrypted wallet](#use-pybitshares-encrypted-wallet).

### Schedule publication

Using cron:

```
$ crontab -e
ACTIVE_KEY="XXXXXXXXXXXXXXXX"

0,15,30,45 * * * * docker run -v /path/to/config.yaml:/config/config.yaml graphene-pricefeed update --skip-critical --active-key=$ACTIVE_KEY
```

## Help

```
$ graphene-pricefeed --help
Usage: graphene-pricefeed [OPTIONS] COMMAND [ARGS]...

Options:
  --configfile TEXT
  --node <wss://host:port>  Node to connect to
  --help                    Show this message and exit.

Commands:
  addkey  Add a private key to the wallet
  create  Create config file
  update  Update price feed for assets
```

```
$ graphene-pricefeed update --help
Usage: graphene-pricefeed update [OPTIONS] [ASSETS]...

  Update price feed for assets

Options:
  --dry-run                       Only compute prices and print result, no
                                  publication.
  --active-key WIF                Active key to be used to sign transactions.
  --confirm-warning / --no-confirm-warning
                                  Need for manual confirmation of warnings
  --skip-critical / --no-skip-critical
                                  Skip critical feeds
  --help                          Show this message and exit.
```

## Sources

The following data sources are currently available:

Name | Status | Assets type | API Key | Description
 --- | ---    | ---         | ---     |   ---
 AEX |  OK    |   Crypto    | No      | last and volume (in quote currency) from CEX ticker api with 15 sec delay 
AlphaVantage | OK | FIAT, Stocks, BTC | Yes | last from unknown source for currencies and from iex for stocks. volume only for stocks (in nb of shares).
Biki | OK | Crypto | No | last and volume (in quote currency) from CEX ticker api
Big.One | OK | Crypto | Yes | bid/ask average and volume (in quote currency) from bulk CEX ticker API.
Binance | OK | Crypto | No | last and volume (in quote currency) from CEX ticker api
BitcoinAverage | OK | Crypto | No | Use APIv2, get last and volume from an average of multiple exchanges.
Bitcoin Venezuela | OK | Crypto | No | ticker from api with 15 minutes delay, no volume
BitsharesFeed | OK | Crypto (MPA) | No | current feed price in Bitshares DEX, no volume.
BitsharesOrderbook | OK | Crypto | No | measure orderbook depth on Bitshares DEX
Bitstamp | OK | Crypto | No | last and volume (in quote currency) from CEX ticker api
Bittrex | OK | Crypto | No | last and volume (in quote currency) from summary api (bulk)
Coinbase | OK | Crypto | No | Use Coinbase Pro (ex GDAX) ticker api to get last and 24h volume.
Coincap | Fails, to be fixed  | ALTCAP & ALTCAP.X | No | use provided market cap, no volume
CoinEgg | OK | Crypto |No | last and volume (in quote currency) from CEX ticker api
CoinGecko | OK | Crypto | No | volume weighted price, sum of market volume.
Coinmarketcap | Warn | Crypto | No | volume weighted average of all prices reported at each market, volume in USD, 5 minutes delay (see https://coinmarketcap.com/faq/). V1 API will be closed December 4th, 2018. 
CoinmarketcapPro | OK | Crypto | Yes | volume weighted average of all prices reported at each market, volume in quote, 1 minutes delay. Use v2 api.
Currencylayer | Fails, to be fixed | FIAT, BTC | Yes | ticker from api, only USD as base and hourly updated with free subscription, no volume info. From various source (https://currencylayer.com/faq)
CoinTiger | OK | Crypto | No | last and volume (in quote currency) from summary api (bulk)
Fixer | OK | FIAT | Yes |  Very similar to CurrencyLayer, ticker from api, daily from European Central Bank, only EUR with free subscription, no volume info.
Graphene | OK | Crypto, FIAT, Stocks | No | last and volume (in quote currency) from Bitshares DEX in realtime
Huobi | OK | Crypto | No | close price and volume (in quote currency) from CEX API in realtime
IEX  | Fails, to be fixed | Stocks | No | last ("IEX real time price", "15 minute delayed price", "Close" or "Previous close") and volume. 
IndoDax | OK | Crypto | No | last and volume (in quote currency) from CEX ticker API.
Kraken | OK | Crypto | No | last and volume (in quote currency) from CEX ticker API.
LBank | OK | Crypto | No | last and volume (in quote currency) from CEX API in realtime
MagicWallet | OK | BITCNY/CNY | Yes | BITCNY/CNY ratio from deposti/withdraw on MagicWallet.
OkCoin  | Fails, to be fixed | Crypto | No | last and volume (in quote currency) from CEX API in realtime
OpenExchangeRates | OK | FIAT, BTC | Yes | ticker from api, only USD as base and hourly updated with free subscription, no volume info. From unknown sources except Bitcoin wich is from CoinDesk (https://openexchangerates.org/faq#sources)
Poloniex | OK | Crypto | No | last and volume (in quote currency) from CEX API in realtime
Quantl | OK | Commodities | Yes | daily price from London Bullion Market Association (LBMA), no volume
RobinHood | Fails, to be fixed | Stocks | No | last, no volume, from unknown source in real time
WorldCoinIndex | OK | Crypto | Yes| volume weighted price, sum of market volume.
ZB | OK | Crypto | No |last and volume (in quote currency) from CEX API in realtime

### Special sources:

#### Manual

A manual source is available to inject some manually set / constand data to the source feed.
This could be usefull for:
  -  testing to avoid connection to a third party datasource.
  -  inject a static rate like BitUSD/USD 

Example:
```
exchanges:
  manual:
    klass: Manual
    feed:
      USD:
        BTS:
          price: 42
          volume: 1
```

#### Composite

A composite source could be used to group multiple sources together in order to aggregate them using a specific fomula.

Aggregation types formulas could be:
  - `min`: select the minimum value for each pairs
  - `max`: select the maximum value for each pairs
  - `mean`: compute the mean price of all the pairs and sum the volume.
  - `weighted_mean`: compute the volume weighted mean price of all the pairs and sum the volume.
  - `median`: compute the median price of all the pairs and sum the volume.
  - `first_valid`: select the first pairs where the source match an ordered list of sources.

The main use cases is if you want to retrieve a pair like BTC/USD from multiples sources (worldcoinindex, bitcoinaverage, coinmarketcap), but you want to use only one of the value in all your computations. The same apply for FIAT exchange rates from (fixer, currencylayer, openexchangerate, ...).

See [example configuration](examples/composite.yaml).


### History storage configuration

To store and load the computed prices, multiple storage macanism option are implemented:

   - file
   - database

#### File storage

To use a 'file' storage you should add in the configuration:

```
history:
    klass: FileHistory
    dirname: prices_db
```

This will save all the computed prices in the relative `prices_db` folder using a CSV file per asset.

#### Database storage

```
history:
    klass: SqlHistory
    url: "postgres+pypostgresql://user:pass@localhost:5432/postgres"
    schema_name: 'price_feed'
    table_name: 'raw_prices'
```

Any kind of [database supported by SQLAlchemy can be used](https://docs.sqlalchemy.org/en/13/dialects/).
However, the appropriate Python drivers should be installed.
As an example to use Postgresql you should first run: 

```
pip install SQLAlchemy py-postgresql
```

As this is a popular option you can also install it using the `history_db_postgresql` feature: 

```
pip install .[history_db_postgresql]
```

See [SQLAlchemy documentation](https://docs.sqlalchemy.org/en/13/core/engines.html) for more details on how to connect to the database.

By default the script will use a table `raw_prices` in the `price_feed` schema. Schema and table names are configurable, they will be automatically created if they does not exists.

## Use of encrypted wallet

Initialize wallet and enter credentials:

```
$ graphene-pricefeed addkey
```

You will need to enter your cli wallet encryption passphrase. If you
don't have a pybitshares wallet, yet, one will be created:

```
Wallet Encryption Passphrase:
Repeat for confirmation:
```

You will need to enter your Private Key (Active key) here. Hit enter the second time it asks you.

```
Private Key (wif) [Enter to quit]:
```

Then you can run the feed update without any argument, it will prompt for the Wallet Encryption Passphrase.

```
$ graphene-pricefeed update
Current Wallet Passphrase:
```

If you don't want to type the Wallet Encryption Passphrase each time, use `UNLOCK` environment variable.

Example in cron:

```
$ crontab -e

SHELL=/bin/bash
PATH=/home/ubuntu/bin:/home/ubuntu/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin
UNLOCK="PASSWD"

0,15,30,45 * * * * graphene-pricefeed --configfile /home/ubuntu/config.yml --skip-critical --no-confirm-warning update >> /var/log/graphene-pricefeed.log 2>&1
```

Or with Docker image:

```
docker run -v /path/to/config:/config -v /path/to/wallet:/root/.local/share/bitshares -e UNLOCK=PASS graphene-pricefeed
```


## Development

To run tests you need get API keys for the providers, and register them as environment variables:

```
export QUANDL_APIKEY=
export OPENEXCHANGERATE_APIKEY=
export FIXER_APIKEY=
export CURRENCYLAYER_APIKEY=
export ALPHAVANTAGE_APIKEY=
export WORLDCOININDEX_APIKEY= 
export MAGICWALLET_APIKEY=
export COINMARKETCAP_APIKEY=
```

To run all tests use:  `PYTHONPATH=. pytest`.

To run a specific test: `PYTHONPATH=. pytest -k bitcoinvenezuela`.

# IMPORTANT NOTE

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
    THE SOFTWARE.

import os
from datetime import datetime, timedelta
import dateutil.parser
import csv

class FileHistory:
    def __init__(self, dirname, **kvargs):
        self.dirname = dirname
        os.makedirs(dirname, exist_ok=True)

    def _get_filename(self, asset_symbol):
        return os.path.join(self.dirname, asset_symbol + '.csv')

    def save(self, asset_symbol, price, at=datetime.utcnow()):
        with open(self._get_filename(asset_symbol), 'a+') as f:
            writer = csv.writer(f)
            writer.writerow((at.isoformat(), price))

    def load(self, asset_symbol, n_days, with_dates=False):
        try:
            with open(self._get_filename(asset_symbol), 'r') as f:
                reader = csv.reader(f)
                oldest_valid_date = datetime.utcnow() - timedelta(days=n_days)
                prices = []
                for row in reader:
                    timestamp = dateutil.parser.isoparse(row[0])
                    price = float(row[1])
                    if timestamp >= oldest_valid_date:
                        if with_dates:
                            prices.append([timestamp, price])
                        else:
                            prices.append(price)
                return prices
        except IOError:
            return []


from sqlalchemy import create_engine
from sqlalchemy import Table, Column, DateTime, Float, String, MetaData
from sqlalchemy.sql import select, and_
from sqlalchemy.schema import CreateSchema

class SqlHistory:
    def __init__(self, url, schema_name='price_feed', table_name='raw_prices', **kvargs):
        extra = {}
        if 'extras' in kvargs:
            extra = kvargs['extras']
        self.db = create_engine(url, **extra)

        if not self.db.dialect.has_schema(self.db, schema_name):
            self.db.execute(CreateSchema(schema_name))

        metadata = MetaData()

        self.prices = Table(table_name, metadata,
            Column('timestamp', DateTime, nullable=False),
            Column('asset', String, nullable=False),
            Column('price', Float, nullable=False),
            schema=schema_name
        )

        metadata.create_all(self.db)


    def save(self, asset_symbol, price, at=datetime.utcnow()):
        self.db.execute(self.prices.insert(), {
            'timestamp': at,
            'asset': asset_symbol,
            'price': price
        })
        pass

    def load(self, asset_symbol, n_days, with_dates=False):
        fields = [self.prices.c.price]
        if with_dates:
            fields = [self.prices.c.timestamp, self.prices.c.price]
        
        oldest_valid_date = datetime.utcnow() - timedelta(days=n_days)
        query = select(fields).where(
            and_(
                self.prices.c.asset == asset_symbol, 
                self.prices.c.timestamp >= oldest_valid_date
            )).order_by(self.prices.c.timestamp)
        rows = self.db.execute(query).fetchall()
        if with_dates:
            return [[timestamp, price] for (timestamp, price) in rows ]
        else:
            return [ price for (price, ) in rows ]

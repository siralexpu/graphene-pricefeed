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

import unittest
import tempfile
import shutil
import os
from datetime import datetime, timedelta

class HistoryTestCase(unittest.TestCase):
    def test_file_history(self):
        from bitshares_pricefeed.history import FileHistory

        db_dir = tempfile.mkdtemp()
        try:
            history = FileHistory(db_dir)
            history.save('USD', .023, at=(datetime.utcnow() - timedelta(days=3)))
            history.save('USD', .024, at=(datetime.utcnow() - timedelta(days=2)))
            history.save('USD', .025, at=(datetime.utcnow() - timedelta(days=1)))
            history.save('USD', .026, at=(datetime.utcnow() - timedelta(hours=1)))

            prices = history.load('USD', 2)
            self.assertListEqual(prices, [.025, .026])

            prices = history.load('USD', 2, with_dates=True)
            self.assertListEqual([row[1] for row in prices ], [.025, .026])
        finally:
            shutil.rmtree(db_dir)

    def test_file_history_dynamic_loading(self):
        import bitshares_pricefeed.history
        options = { 'klass': 'FileHistory', 'dirname': tempfile.mkdtemp() }
        try:
            klass = getattr(bitshares_pricefeed.history, options['klass'])
            history = klass(**options)
            history.save('USD', .023)
            prices = history.load('USD', 2)
            self.assertListEqual(prices, [ .023 ])
        finally:
            shutil.rmtree(options['dirname'])

    def test_file_history_empty(self):
        from bitshares_pricefeed.history import FileHistory

        db_dir = tempfile.mkdtemp()
        try:
            history = FileHistory(db_dir)
            prices = history.load('USD', 2)
            self.assertListEqual(prices, [])
        finally:
            shutil.rmtree(db_dir)

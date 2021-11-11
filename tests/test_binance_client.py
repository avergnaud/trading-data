# -*- coding: utf-8 -*-

import unittest
from input.binance_exchange.binance_client import BinanceClient


class BinanceClientTestCase(unittest.TestCase):
    """Basic test cases."""

    def test_add(self):
        client = BinanceClient()
        ohlc = client.get_ohlc('ETHUSDT', '5m', '1 hour ago UTC')
        # https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.size.html
        # "return the number of rows (12) times number of columns (open high low close volume)"
        self.assertEqual(ohlc.size, 12*5)

# -*- coding: utf-8 -*-

import unittest

import pandas as pd

from input.binance_exchange.binance_client import BinanceClient
from persistence.ohlc_dao import get_by_timestamp


class OhlcDataTestCase(unittest.TestCase):
    """Basic test cases."""

    def test_compare(self):
        client = BinanceClient()
        ohlc_binance = client.get_ohlc('ETHUSDT', '1h', 1606939487)

        ohlc_brochain = get_by_timestamp({'exchange': 'binance', 'pair': 'ETHUSDT', 'interval': '1h'}, 1606939487)
        df = pd.DataFrame(ohlc_brochain,
                          columns=['_id', 'exchange', 'pair', 'interval', 'timestamp', 'open', 'high', 'low', 'close',
                                   'volume'])
        df['close'] = pd.to_numeric(df['close'])
        df['high'] = pd.to_numeric(df['high'])
        df['low'] = pd.to_numeric(df['low'])
        df['open'] = pd.to_numeric(df['open'])
        df['volume'] = pd.to_numeric(df['volume'])

        del df['_id']
        del df['exchange']
        del df['pair']
        del df['interval']

        df = df.set_index(df['timestamp'])
        df.index = pd.to_datetime(df.index, unit='ms')
        del df['timestamp']

        # probable que la base ne soit pas à jour lancer le main du BinanceFeed si c'est le cas
        self.assertEqual(ohlc_binance.size, df.size)

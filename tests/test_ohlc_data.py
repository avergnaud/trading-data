# -*- coding: utf-8 -*-

import unittest

from input.binance_exchange.binance_client import BinanceClient
from persistence.ohlc_dao import get_by_timestamp, mongoDataToDataframe


class OhlcDataTestCase(unittest.TestCase):
    """Basic test cases."""

    def test_compare(self):
        client = BinanceClient()
        ohlc_binance = client.get_ohlc('ETHUSDT', '1h', 1606939487)

        ohlc_brochain = mongoDataToDataframe(
            get_by_timestamp({'exchange': 'binance', 'pair': 'ETHUSDT', 'interval': '1h'}, 1606939487))

        # probable que la base ne soit pas à jour lancer le main du BinanceFeed si c'est le cas
        self.assertEqual(ohlc_binance.size, ohlc_brochain.size)

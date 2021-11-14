# 1502928000000 = 17 August 2017 00:00:00
# exchange : binance
# pair : ETHUSDT
# interval '1d'
from persistence import mongo_client
from input.binance_exchange.binance_client import BinanceClient

EXCHANGE = 'binance'


class BinanceFeed:
    def __init__(self, pair, interval):
        print('constructing BinanceFeed')
        self.exchange = EXCHANGE
        self.pair = pair
        self.interval = interval

    def update_data(self):
        print(f"running BinanceFeed update_data for {self.pair}, {self.interval}")

        start_ohlc = mongo_client.get_last_timestamp(
            {'exchange': self.exchange, 'pair': self.pair, 'interval': self.interval})
        if start_ohlc is None:
            start = 1502928000000
        else:
            start = start_ohlc['timestamp']

        binanceClient = BinanceClient()
        ohlc_dataframe = binanceClient.get_ohlc(self.pair, self.interval, start)

        # peu performant uniquement pour les premiers insert, en cas nominal start est récent:
        for ind in ohlc_dataframe.index:
            ohlc = {'exchange': self.exchange, 'pair': self.pair, 'interval': self.interval,
                    'timestamp': int(ind.timestamp()),
                    'open': ohlc_dataframe['open'][ind], 'high': ohlc_dataframe['high'][ind],
                    'low': ohlc_dataframe['low'][ind], 'close': ohlc_dataframe['close'][ind],
                    'volume': ohlc_dataframe['volume'][ind]}
            mongo_client.insert_or_update(ohlc)


if __name__ == "__main__":
    binanceFeed = BinanceFeed('ETHEUR', '1h')
    binanceFeed.update_data()

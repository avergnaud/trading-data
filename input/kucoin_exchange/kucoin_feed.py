from input.kucoin_exchange.kucoin_client import KucoinClient
from persistence import ohlc_dao

EXCHANGE = 'kucoin'


class KucoinFeed:
    def __init__(self, pair, interval):
        print('constructing KucoinFeed')
        self.exchange = EXCHANGE
        self.pair = pair
        self.interval = interval

    def update_data(self):
        print(f"running KucoinFeed update_data for {self.pair}, {self.interval}")

        start_ohlc = ohlc_dao.get_last_timestamp(
            {'exchange': self.exchange, 'pair': self.pair, 'interval': self.interval})
        if start_ohlc is None:
            # 1502928000000 = 17 August 2017 00:00:00
            start = 1502928000000
        else:
            start = start_ohlc['timestamp']

        kucoinClient = KucoinClient()
        ohlc_dataframe = kucoinClient.get_ohlc(self.pair, self.interval, start)

        # peu performant uniquement pour les premiers insert, en cas nominal start est récent:
        for ind in ohlc_dataframe.index:
            ohlc = {'exchange': self.exchange, 'pair': self.pair, 'interval': self.interval,
                    'timestamp': int(ind.timestamp()),
                    'open': ohlc_dataframe['open'][ind], 'high': ohlc_dataframe['high'][ind],
                    'low': ohlc_dataframe['low'][ind], 'close': ohlc_dataframe['close'][ind],
                    'volume': ohlc_dataframe['volume'][ind]}
            ohlc_dao.insert_or_update(ohlc)


if __name__ == "__main__":
    kucoinFeed = KucoinFeed('BTC-USDT', '5min')
    kucoinFeed.update_data()

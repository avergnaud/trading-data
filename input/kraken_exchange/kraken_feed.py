from input.kraken_exchange.kraken_client import KrakenClient
from persistence import ohlc_dao

EXCHANGE = 'kraken'


class KrakenFeed:
    def __init__(self, pair, interval):
        self.exchange = EXCHANGE
        self.pair = pair
        self.interval = interval

    def update_data(self):
        print(f"KrakenFeed | {self.pair}, {self.interval} | updating")
        # computing start timestamp
        start_ohlc = ohlc_dao.get_last_timestamp(
            {'exchange': self.exchange, 'pair': self.pair, 'interval': self.interval})
        if start_ohlc is None:
            # 1502928000000 = 17 August 2017 00:00:00
            start = 1499000000
        else:
            start = start_ohlc['timestamp']
        # updating data
        krakenClient = KrakenClient()
        ohlc_dataframe = krakenClient.get_ohlc(self.pair, self.interval, start)
        # peu performant uniquement pour les premiers insert, en cas nominal start est récent:
        for ind in ohlc_dataframe.index:
            ohlc = {'exchange': self.exchange, 'pair': self.pair, 'interval': self.interval,
                    'timestamp': int(ind.timestamp()),
                    'open': ohlc_dataframe['open'][ind], 'high': ohlc_dataframe['high'][ind],
                    'low': ohlc_dataframe['low'][ind], 'close': ohlc_dataframe['close'][ind],
                    'volume': ohlc_dataframe['volume'][ind]}
            ohlc_dao.insert_or_update(ohlc)
        print(f"KrakenFeed | {self.pair}, {self.interval} | done")


if __name__ == "__main__":
    binanceFeed = KrakenFeed('XETHZEUR', 60)
    binanceFeed.update_data()

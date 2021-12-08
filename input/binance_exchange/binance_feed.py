from persistence import ohlc_dao
from input.binance_exchange.binance_client import BinanceClient


EXCHANGE = 'binance'


# used as a key in feed_cron_manager.py
class BinanceFeed:
    def __init__(self, pair, interval):
        self.exchange = EXCHANGE
        self.pair = pair
        self.interval = interval

    def update_data(self):
        print(f"BinanceFeed | {self.pair}, {self.interval} | updating")
        # computing start timestamp
        start_ohlc = ohlc_dao.get_last_timestamp(
            {'exchange': self.exchange, 'pair': self.pair, 'interval': self.interval})
        if start_ohlc is None:
            # 1502928000000 = 17 August 2017 00:00:00
            start = 1502928000000
        else:
            start = start_ohlc['timestamp']
        # updating data
        binanceClient = BinanceClient()
        ohlc_dataframe = binanceClient.get_ohlc(self.pair, self.interval, start)
        # peu performant uniquement pour les premiers insert, en cas nominal start est récent:
        for ind in ohlc_dataframe.index:
            ohlc = {'exchange': self.exchange, 'pair': self.pair, 'interval': self.interval,
                    'timestamp': int(ind.timestamp()),
                    'open': ohlc_dataframe['open'][ind], 'high': ohlc_dataframe['high'][ind],
                    'low': ohlc_dataframe['low'][ind], 'close': ohlc_dataframe['close'][ind],
                    'volume': ohlc_dataframe['volume'][ind]}
            ohlc_dao.insert_or_update(ohlc)
        print(f"BinanceFeed | {self.pair}, {self.interval} | done")

    def __hash__(self):
        return hash((self.pair, self.interval))

    def __eq__(self, other):
        return (self.pair, self.interval) == (other.pair, other.interval)

    def __ne__(self, other):
        # Not strictly necessary, but to avoid having both x==y and x!=y
        # True at the same time
        return not(self == other)


if __name__ == "__main__":
    binanceFeed = BinanceFeed('ETHUSDT', '1h')
    binanceFeed.update_data()

from input.gate_exchange.gate_client import GateClient
from persistence import ohlc_dao


EXCHANGE = 'gate'


# used as a key in feed_cron_manager.py
class GateFeed:
    def __init__(self, pair, interval):
        self.exchange = EXCHANGE
        self.pair = pair
        self.interval = interval

    def update_data(self):
        print(f"GateFeed | {self.pair}, {self.interval} | updating")
        # computing start timestamp
        start_ohlc = ohlc_dao.get_last_timestamp(
            {'exchange': self.exchange, 'pair': self.pair, 'interval': self.interval})
        if start_ohlc is None:
            # 1606939487 = 2 December 2020 20:04:47
            start = 1606939487
        else:
            start = start_ohlc['timestamp']
        # updating data
        gateClient = GateClient()
        ohlc_dataframe = gateClient.get_ohlc(self.pair, self.interval, start)
        # peu performant uniquement pour les premiers insert, en cas nominal start est récent:
        for ind in ohlc_dataframe.index:
            ohlc = {'exchange': self.exchange, 'pair': self.pair, 'interval': self.interval,
                    'timestamp': int(ind.timestamp()),
                    'open': ohlc_dataframe['open'][ind], 'high': ohlc_dataframe['high'][ind],
                    'low': ohlc_dataframe['low'][ind], 'close': ohlc_dataframe['close'][ind],
                    'volume': ohlc_dataframe['volume'][ind]}
            ohlc_dao.insert_or_update(ohlc)
        print(f"GateFeed | {self.pair}, {self.interval} | done")

    def __hash__(self):
        return hash((self.pair, self.interval))

    def __eq__(self, other):
        return (self.pair, self.interval) == (other.pair, other.interval)

    def __ne__(self, other):
        # Not strictly necessary, but to avoid having both x==y and x!=y
        # True at the same time
        return not(self == other)


if __name__ == "__main__":
    gateFeed = GateFeed('ETH_USDT', '1h')
    gateFeed.update_data()

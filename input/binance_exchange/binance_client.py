import pandas as pd
from binance.client import Client


class BinanceClient:
    def __init__(self):
        print('constructing BinanceClient')

    def get_ohlc(self, pair, interval, start):
        """Calls the Binance API, transforms some data, return the klines data

        Parameters
        ----------
        pair : str
            trading pair. Example: "ETHUSDT"
        interval : str.
            One of Binance Kline interval
            KLINE_INTERVAL_1MINUTE = '1m'
            KLINE_INTERVAL_3MINUTE = '3m'
            KLINE_INTERVAL_5MINUTE = '5m'
            KLINE_INTERVAL_15MINUTE = '15m'
            KLINE_INTERVAL_30MINUTE = '30m'
            KLINE_INTERVAL_1HOUR = '1h'
            KLINE_INTERVAL_2HOUR = '2h'
            KLINE_INTERVAL_4HOUR = '4h'
            KLINE_INTERVAL_6HOUR = '6h'
            KLINE_INTERVAL_8HOUR = '8h'
            KLINE_INTERVAL_12HOUR = '12h'
            KLINE_INTERVAL_1DAY = '1d'
            KLINE_INTERVAL_3DAY = '3d'
            KLINE_INTERVAL_1WEEK = '1w'
            KLINE_INTERVAL_1MONTH = '1M'
        start : (str|int)
            Start date string in UTC format or timestamp in milliseconds
            Example : "01 november 2021", 1635724800000

        Returns
        -------
        pandas.core.frame.DataFrame
            a panda DataFrame containing timestamp (index), open, high, low, close
        """

        client = Client()

        klines_t = client.get_historical_klines(pair, interval, str(start))

        df = pd.DataFrame(klines_t,
                          columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_av',
                                   'trades', 'tb_base_av', 'tb_quote_av', 'ignore'])
        df['close'] = pd.to_numeric(df['close'])
        df['high'] = pd.to_numeric(df['high'])
        df['low'] = pd.to_numeric(df['low'])
        df['open'] = pd.to_numeric(df['open'])
        df['volume'] = pd.to_numeric(df['volume'])

        del df['ignore']
        del df['close_time']
        del df['quote_av']
        del df['trades']
        del df['tb_base_av']
        del df['tb_quote_av']

        df = df.set_index(df['timestamp'])
        df.index = pd.to_datetime(df.index, unit='ms')
        del df['timestamp']
        return df.copy()


    def get_pairs(self):
        """Calls the Binance API, gets available trading pairs

        Parameters
        ----------

        Returns
        -------
        pandas.core.frame.DataFrame
            ?
        """

        client = Client()
        pairs = client.get_all_tickers()
        return pairs


if __name__ == "__main__":
    cclient = BinanceClient()
    pairs = cclient.get_pairs()
    print(pairs)
    # 1700
    # ohlc = cclient.get_ohlc('ETHUSDT', '5m', '1 hour ago UTC')
    # ohlc = cclient.get_ohlc('ETHUSDT', '1h', 1635724800000)
    # print(ohlc.size)

    # client = Client()
    # klines_t = client.get_historical_klines('ETHUSDT', '1d', "01 july 2017", "10 september 2017")
    # print(klines_t)

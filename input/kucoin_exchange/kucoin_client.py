import pandas as pd
from kucoin.client import Client

api_key = '<api_key>'
api_secret = '<api_secret>'
api_passphrase = '<api_passphrase>'


class KucoinClient:

    def __init__(self):
        pass

    def get_ohlc(self, pair, interval, start):
        """Calls the  Kucoin API, transforms some data, return the klines data

        Parameters
        ----------
        pair : str
            trading pair. Example: "BTC-USDT"
        interval : str.
            1min, 3min, 5min, 15min, 30min, 1hour, 2hour, 4hour, 6hour, 8hour, 12hour, 1day, 1week
        start : (str|int)
            Start date string in UTC format or timestamp in milliseconds
            Example : "01 november 2021", 1635724800000

        Returns ------- pandas.core.frame.DataFrame a panda DataFrame containing timestamp (index), opening price,
        closing price, highest price, lowest price, Transaction amount, Transaction volume
        """

        client = Client(api_key, api_secret, api_passphrase, sandbox=True)

        klines_t = client.get_kline_data(pair, interval, start)
        df = pd.DataFrame(klines_t,
                          columns=['timestamp', 'open', 'close', 'high', 'low', 'amount', 'volume'])

        df['close'] = pd.to_numeric(df['close'])
        df['high'] = pd.to_numeric(df['high'])
        df['low'] = pd.to_numeric(df['low'])
        df['open'] = pd.to_numeric(df['open'])
        df['volume'] = pd.to_numeric(df['volume'])

        del df['amount']

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

        client = Client(api_key, api_secret, api_passphrase, sandbox=True)

        resp = client.get_ticker()
        return resp['ticker']


if __name__ == "__main__":
    kucoinClient = KucoinClient()
    # pairs = kucoinClient.get_pairs()
    # print(pairs)
    ohlc = kucoinClient.get_ohlc('BTC-USDT', '5min', 1606939487)
    # 2 December 2020 20:04:47
    print(ohlc.size)

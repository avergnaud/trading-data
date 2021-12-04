import pandas as pd
from kucoin.client import Client
from datetime import datetime

api_key = '<api_key>'
api_secret = '<api_secret>'
api_passphrase = '<api_passphrase>'


class KucoinClient:

    def __init__(self):
        pass

    # helper
    def convert_to_seconds(self, interval):
        match interval:
            case '1min':
                return 60
            case '3min':
                return 180
            case '5min':
                return 300
            case '15min':
                return 900
            case '30min':
                return 1800
            case '1hour':
                return 3600
            case '2hour':
                return 7200
            case '4hour':
                return 14400
            case '6hour':
                return 21600
            case '8hour':
                return 28800
            case '12hour':
                return 43200
            case '1day':
                return 86400
            case '1week':
                return 604800
            case _:
                # Anything not matched by the above
                print(f"No feeder found for {interval}")
                return None

    # helper pagination
    def get_ohlc_chunk(self, pair, interval, start, end):

        client = Client(api_key, api_secret, api_passphrase, sandbox=True)
        klines_t = client.get_kline_data(pair, interval, start, end)
        df = pd.DataFrame(klines_t,
                          columns=['timestamp', 'open', 'close', 'high', 'low', 'amount', 'volume'])

        df['close'] = pd.to_numeric(df['close'])
        df['high'] = pd.to_numeric(df['high'])
        df['low'] = pd.to_numeric(df['low'])
        df['open'] = pd.to_numeric(df['open'])
        df['volume'] = pd.to_numeric(df['volume'])

        del df['amount']

        df = df.set_index(df['timestamp'])
        df.index = pd.to_datetime(df.index, unit='s')
        del df['timestamp']
        return df

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
            Example : "01 november 2021", 1635724800

        Returns
        -------
        pandas.core.frame.DataFrame
            a panda DataFrame containing timestamp (index), opening price,
            closing price, highest price, lowest price, Transaction amount, Transaction volume
        """
        # For each query, the system would return at most **1500** pieces of data. To obtain more data, please page
        # the data by time. ce premier appel a toujours lieu :
        now_seconds = int(datetime.now().timestamp())
        interval_seconds = self.convert_to_seconds(interval)
        from_seconds = start
        # est-ce qu'il y a plus de 1000 périodes ?
        to_seconds = min(now_seconds, from_seconds + 1499 * interval_seconds)
        df = self.get_ohlc_chunk(pair, interval, from_seconds, to_seconds)
        # les appels suivants ont lieu si number_of_intervals > 1500
        # number_of_intervals = (now_seconds - since) / interval_seconds
        while to_seconds < now_seconds:
            from_seconds = to_seconds + interval_seconds
            to_seconds = min(now_seconds, from_seconds + 1499 * interval_seconds)
            chunk_df = self.get_ohlc_chunk(pair, interval, from_seconds, to_seconds)
            df = df.append(chunk_df)

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

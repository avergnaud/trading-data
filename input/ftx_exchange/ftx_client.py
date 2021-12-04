import os
from datetime import datetime

import ftx
import pandas as pd

api_endpoint = 'https://ftx.com/api'
api_key = os.getenv('FTX_API_KEY')
api_secret = os.getenv('FTX_API_SECRET')


class FtxClient:
    def __init__(self):
        self.x = ftx.FtxClient()

    def get_pairs(self):
        """Calls the FTX API, gets available trading pairs
       Parameters
       ----------
       Returns
       -------
       list
       """

        liste = []
        for key in self.x.get_markets():
            liste.append(key['name'])
        return liste

    # helper pagination
    def get_ohlc_chunk(self, pair, interval, since, to):
        ret = self.x.get_historical_data(market_name=pair, resolution=interval, limit=50000,
                                         start_time=since, end_time=to)

        df = pd.DataFrame(ret,
                          columns=['startTime', 'time', 'open', 'high', 'low', 'close', 'volume', 'timestamp'])

        df['close'] = pd.to_numeric(df['close'])
        df['high'] = pd.to_numeric(df['high'])
        df['low'] = pd.to_numeric(df['low'])
        df['open'] = pd.to_numeric(df['open'])
        df['volume'] = pd.to_numeric(df['volume'])
        df['timestamp'] = df['time']

        del df['startTime']
        del df['time']

        df = df.set_index(df['timestamp'])
        df.index = pd.to_datetime(df.index, unit='ms')
        del df['timestamp']
        return df

    def get_ohlc(self, pair, interval, since):
        """Calls the FTX API...

        Parameters
        ----------
        market_name ---> pair : str
            trading pair. Example: "BTC/USDT"
        resolution --> interval : int.
           15, 60, 300, 900, 3600, 14400, 86400, or any multiple of 86400 up to 30*86400
        start_time --> since : int
            Since date, timestamp in seconds
            since=1548111600
        limit = Mettre une limite très haute

        Returns
        -------
        pandas.core.frame.DataFrame
            a panda DataFrame containing time (index), open, high, low, close, volume

        """
        # limit – optional with a 5000 limit
        # ce premier appel a toujours lieu :
        now_seconds = int(datetime.now().timestamp())
        interval_seconds = interval
        from_seconds = since
        # est-ce qu'il y a plus de 1000 périodes ?
        to_seconds = min(now_seconds, from_seconds + 4999 * interval_seconds)
        df = self.get_ohlc_chunk(pair, interval, from_seconds, to_seconds)
        # les appels suivants ont lieu si number_of_intervals > 5000
        # number_of_intervals = (now_seconds - since) / interval_seconds
        while to_seconds < now_seconds:
            from_seconds = to_seconds + interval_seconds
            to_seconds = min(now_seconds, from_seconds + 4999 * interval_seconds)
            chunk_df = self.get_ohlc_chunk(pair, interval, from_seconds, to_seconds)
            df = df.append(chunk_df)

        return df.copy()


if __name__ == "__main__":
    client = FtxClient()
    # pairs = client.get_pairs()
    # print(pairs)
    # ohlcs = client.get_ohlc('ETH/USDT', 3600, 1606939487)  # Wed Dec 02 2020 20:04:47 GMT+0000
    ohlcs = client.get_ohlc('ETH/USDT', 300, 1606939487)  # Wed Dec 02 2020 20:04:47 GMT+0000
    print(ohlcs)
    print(ohlcs.size)

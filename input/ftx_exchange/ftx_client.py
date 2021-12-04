import hmac
import json
import os
import time

import ftx
import pandas as pd
from requests import Request, Session

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
        ret = self.x.get_historical_data(market_name=pair, resolution=interval, limit=50000,
                                         start_time=since)

        df = pd.DataFrame(ret,
                          columns=['startTime', 'time', 'open', 'high', 'low', 'close', 'volume','timestamp'])

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
        return df.copy()


def get_pairs_old(self):
    """Calls the FTX API, gets available trading pairs

    Parameters
    ----------

    Returns
    -------
    list
    """

    if api_key is None:
        return []

    s = Session()

    ts = int(time.time() * 1000)
    request = Request('GET', api_endpoint + '/markets')
    prepared = request.prepare()
    signature_payload = f'{ts}{prepared.method}{prepared.path_url}'.encode()
    signature = hmac.new(api_secret.encode(), signature_payload, 'sha256').hexdigest()

    request.headers['FTX-KEY'] = api_key
    request.headers['FTX-SIGN'] = signature
    request.headers['FTX-TS'] = str(ts)

    resp = s.send(prepared)

    # print(resp.status_code)
    my_json_string = resp.content.decode('utf8').replace("'", '"')
    my_json = json.loads(my_json_string)
    return my_json['result']


def get_ohlc_old(self, pair, interval, since):
    """Calls the FTX API...

    Parameters
    ----------
    pair : str
        trading pair. Example: "XBTUSD"
    interval : int.
        Time frame interval in minutes
        1 5 15 30 60 240 1440 10080 21600
    since : int
        Since date, timestamp in seconds
        since=1548111600

    Returns
    -------
    ?
        Return committed OHLC data
    """

    # ret = self.k.query_public('OHLC', data = {'pair': pair, 'interval': interval, 'since': since})

    s = Session()

    ts = int(time.time() * 1000)
    # params = dict(resolution='3600',limit=limit,start_time='1609462800',end_time=end_time)
    # params = dict(resolution='3600', start_time='1609462800')
    params = dict(resolution='86400', start_time='1609462800')

    request = Request('GET', api_endpoint + '/markets/BTC-0924/candles', params=params)
    prepared = request.prepare()
    signature_payload = f'{ts}{prepared.method}{prepared.path_url}'.encode()
    signature = hmac.new(api_secret.encode(), signature_payload, 'sha256').hexdigest()

    request.headers['FTX-KEY'] = api_key
    request.headers['FTX-SIGN'] = signature
    request.headers['FTX-TS'] = str(ts)

    resp = s.send(prepared)

    # print(resp.status_code)
    my_json_string = resp.content.decode('utf8').replace("'", '"')
    my_json = json.loads(my_json_string)
    print(my_json)

    # df['close'] = pd.to_numeric(df['close'])
    # df['high'] = pd.to_numeric(df['high'])
    # df['low'] = pd.to_numeric(df['low'])
    # df['open'] = pd.to_numeric(df['open'])
    # df['volume'] = pd.to_numeric(df['volume'])

    return []


if __name__ == "__main__":
    client = FtxClient()
    # pairs = client.get_pairs()
    # print(pairs)
    ohlcs = client.get_ohlc('BTC/USDT', 60, 1499000000)  # UTC 2017-07-02 12:53:20
    print(ohlcs)
    print(ohlcs.size)

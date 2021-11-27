import os
import time
import hmac
import json
from requests import Request, Session

api_endpoint = 'https://ftx.com/api'
api_key = os.getenv('FTX_API_KEY')
api_secret = os.getenv('FTX_API_SECRET')


class FtxClient:
    def __init__(self):
        print('constructing FTXClient')

    def get_pairs(self):
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

    def get_ohlc(self, pair, interval, since):
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
    list = client.get_ohlc('','','')
    print(list)
import krakenex
import pandas as pd


class KrakenClient:
    def __init__(self):
        print('constructing KrakenClient')
        self.k = krakenex.API()

    def get_ohlc(self, pair, interval, since):
        """Calls the Kraken API...

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
        pandas.core.frame.DataFrame
            a panda DataFrame containing timestamp (index), open, high, low, close, 'volume', 'vwap', 'count'
            Krakenex utilise pykrakenapi
                https://github.com/dominiktraxl/pykrakenapi
        """

        ret = self.k.query_public('OHLC', data={'pair': pair, 'interval': interval, 'since': since})

        # {"_id": ObjectId("6197feb16fa0141720dd2448"), "exchange": "kraken", "pair": "XXBTZUSD"}

        ohlcs = ret['result'][pair]

        df = pd.DataFrame(ohlcs,
                          columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'vwap', 'count'])

        df['close'] = pd.to_numeric(df['close'])
        df['high'] = pd.to_numeric(df['high'])
        df['low'] = pd.to_numeric(df['low'])
        df['open'] = pd.to_numeric(df['open'])
        df['volume'] = pd.to_numeric(df['volume'])

        del df['vwap']
        del df['count']

        df = df.set_index(df['timestamp'])
        df.index = pd.to_datetime(df.index, unit='ms')
        del df['timestamp']
        return df.copy()

    def get_pairs(self):
        """Calls the Kraken API, gets available trading pairs

        Parameters
        ----------

        Returns
        -------
        liste
        """

        resp = self.k.query_public('AssetPairs')
        result = resp['result'].keys()
        liste = []
        for key in result:
            liste.append(key)
        return liste


if __name__ == "__main__":
    client = KrakenClient()
    # ohlc = client.get_ohlc('XETHZEUR', 60, 1499000000)  # UTC 2017-07-02 12:53:20
    # print(ohlc.size)
    pairs = client.get_pairs()
    print(pairs)

import krakenex


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
        ?
            Return committed OHLC data
        """

        ret = self.k.query_public('OHLC', data = {'pair': pair, 'interval': interval, 'since': since})

        ohlcs = ret['result']['']

        {"_id": ObjectId("6197feb16fa0141720dd2448"), "exchange": "kraken", "pair": "XXBTZUSD"}

        # df['close'] = pd.to_numeric(df['close'])
        # df['high'] = pd.to_numeric(df['high'])
        # df['low'] = pd.to_numeric(df['low'])
        # df['open'] = pd.to_numeric(df['open'])
        # df['volume'] = pd.to_numeric(df['volume'])

        return


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
    client.get_ohlc('XBTUSD', 60, 1634774400)

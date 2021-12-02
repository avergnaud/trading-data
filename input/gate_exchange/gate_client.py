import gate_api
import pandas as pd
from gate_api.exceptions import ApiException, GateApiException

# Defining the host is optional and defaults to https://api.gateio.ws/api/v4
# See configuration.py for a list of all supported configuration parameters.
configuration = gate_api.Configuration(host="https://api.gateio.ws/api/v4")
api_client = gate_api.ApiClient(configuration)

# Create an instance of the API class
api_instance = gate_api.SpotApi(api_client)


class GateClient:
    def __init__(self):
        print('constructing GateClient')

    def get_ohlc(self, pair, interval, since):
        """Calls the Kraken API...

    pair : str
            trading pair. Example: "ETHUSDT"
        interval : str.
            One of GateIO interval
             '10s', '1m', '5m', '15m', '30m', '1h', '4h', '8h', '1d', '1w', '1M'
        start : (str|int)
            Start date string in UTC format or timestamp in milliseconds
            Example : "01 november 2021", 1635724800000

    Returns
        -------
        pandas.core.frame.DataFrame
            a panda DataFrame containing timestamp (index), open, high, low, close, volume
            Attention l'API limite a 1000 points donc interval pas trop bas et pas trop une date trop loin....
        """
        try:
            api_response = api_instance.list_candlesticks(currency_pair=pair, interval=interval, _from=since)
        except GateApiException as ex:
            print("Gate api exception, label: %s, message: %s\n" % (ex.label, ex.message))
        except ApiException as e:
            print("Exception when calling SpotApi->list_candlesticks: %s\n" % e)

        df = pd.DataFrame(api_response,
                          columns=['timestamp', 'volume', 'open', 'high', 'low', 'close'])

        df['close'] = pd.to_numeric(df['close'])
        df['high'] = pd.to_numeric(df['high'])
        df['low'] = pd.to_numeric(df['low'])
        df['open'] = pd.to_numeric(df['open'])
        df['volume'] = pd.to_numeric(df['volume'])

        df = df.set_index(df['timestamp'])
        df.index = pd.to_datetime(df.index, unit='ms')
        del df['timestamp']
        return df.copy()

    def get_pairs(self):
        """Calls the Gate.io API, gets available trading pairs

        Parameters
        ----------

        Returns
        -------
        pandas.core.frame.DataFrame

        """

        try:
            api_response = api_instance.list_currency_pairs()
        except GateApiException as ex:
            print("Gate api exception, label: %s, message: %s\n" % (ex.label, ex.message))
        except ApiException as e:
            print("Exception when calling SpotApi->list_currency_pairs: %s\n" % e)

        liste = []
        for resp in api_response:
            liste.append(resp.id)
        return liste


if __name__ == "__main__":
    gate_client = GateClient()
    # pairs = gate_client.get_pairs()
    # print(pairs)
    ohlc = gate_client.get_ohlc('BTC_USDT', '1d', 1606939487)  # UTC Wednesday 2 December 2020 20:04:47
    print(ohlc.size)

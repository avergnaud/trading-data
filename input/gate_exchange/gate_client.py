import gate_api
import pandas as pd
from gate_api.exceptions import ApiException, GateApiException
from datetime import datetime

# Defining the host is optional and defaults to https://api.gateio.ws/api/v4
# See configuration.py for a list of all supported configuration parameters.
configuration = gate_api.Configuration(host="https://api.gateio.ws/api/v4")
api_client = gate_api.ApiClient(configuration)

# Create an instance of the API class
api_instance = gate_api.SpotApi(api_client)


class GateClient:
    def __init__(self):
        print('constructing GateClient')

    # helper
    def convert_to_seconds(self, interval):
        match interval:
            case '5m':
                return 300
            case '15m':
                return 900
            case '30m':
                return 1800
            case '1h':
                return 3600
            case '4h':
                return 14400
            case '8h':
                return 28800
            case '1d':
                return 86400
            case '1w':
                return 604800
            case '1M':
                # je suis pas sûr, le problème se posera dans 1000 mois
                return 2592000
            case _:
                # Anything not matched by the above
                print(f"No feeder found for {interval}")
                return None

    # helper pagination
    def get_ohlc_chunk(self, pair, interval, from_seconds, to_seconds):
        try:
            api_response = api_instance.list_candlesticks(currency_pair=pair, interval=interval, _from=from_seconds, to=to_seconds)
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
        df.index = pd.to_datetime(df.index, unit='s')
        del df['timestamp']
        return df

    def get_ohlc(self, pair, interval, since):
        """Calls the Kraken API...

    pair : str
            trading pair. Example: "ETHUSDT"
        interval : str.
            One of GateIO interval
             ('10s', '1m') '5m', '15m', '30m', '1h', '4h', '8h', '1d', '1w', '1M'
        start : (str|int)
            Start date string in UTC format or timestamp in seconds
            Example : 1606939487 = 2 December 2020 20:04:47

    Returns
        -------
        pandas.core.frame.DataFrame
            a panda DataFrame containing timestamp (index), open, high, low, close, volume
            Attention l'API limite a 1000 points donc interval pas trop bas et pas trop une date trop loin....
        """

        # ce premier appel a toujours lieu
        now_seconds = int(datetime.now().timestamp())
        interval_seconds = self.convert_to_seconds(interval)
        from_seconds = since
        # est-ce qu'il y a plus de 1000 périodes ?
        to_seconds = min(now_seconds, from_seconds + 999 * interval_seconds)
        df = self.get_ohlc_chunk(pair, interval, from_seconds, to_seconds)
        # les appels suivants ont lieu si number_of_intervals > 1000
        # number_of_intervals = (now_seconds - since) / interval_seconds
        while to_seconds < now_seconds:
            from_seconds = to_seconds + interval_seconds
            to_seconds = min(now_seconds, from_seconds + 999 * interval_seconds)
            chunk_df = self.get_ohlc_chunk(pair, interval, from_seconds, to_seconds)
            df = df.append(chunk_df)

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
    print(int(datetime.now().timestamp()))
    gate_client = GateClient()
    # pairs = gate_client.get_pairs()
    # print(pairs)
    # ohlc = gate_client.get_ohlc('BTC_USDT', '1d', 1606939487)  # UTC Wednesday 2 December 2020 20:04:47
    ohlc = gate_client.get_ohlc('BTC_USDT', '1h', 1606939487)  # UTC Wednesday 2 December 2020 20:04:47
    print(ohlc.size)

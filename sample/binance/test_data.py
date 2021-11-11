from input.binance_exchange.binance_client import BinanceClient


def main():

    # https://python-binance.readthedocs.io/en/latest/binance.html#binance.client.Client.get_historical_klines
    # klinesT = client.get_historical_klines("ETHUSDT", Client.KLINE_INTERVAL_1HOUR, "01 november 2021")
    # klinesT = client.get_historical_klines("ETHUSDT", Client.KLINE_INTERVAL_1HOUR, 1635724800000)

    client = BinanceClient()
    # ohlc = client.get_ohlc('ETHUSDT', '1h', 1635724800000)
    ohlc = client.get_ohlc('ETHUSDT', '5m', '1 hour ago UTC')

    print(type(ohlc))
    print(ohlc)

if __name__ == "__main__":
    main()
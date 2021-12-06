import ta

from input.binance_exchange.binance_client import BinanceClient


class BinanceBot:
    def __init__(self):
        pass

    def launchBot(self, ohlc):
        ohlc['SMA200'] = ta.trend.sma_indicator(ohlc['close'], 200)
        ohlc['SMA600'] = ta.trend.sma_indicator(ohlc['close'], 600)
        print(ohlc)

        usdt = 500
        btc = 0
        last_index = ohlc.first_valid_index()

        for index, row in ohlc.iterrows():
            if ohlc['SMA200'][last_index] > ohlc['SMA600'][last_index] and usdt > 10:
                btc = usdt / ohlc['close'][index]
                btc = btc - 0.0007 * btc
                usdt = 0
                print("Buy BTC at", ohlc['close'][index], '$ the', index)

            if ohlc['SMA200'][last_index] < ohlc['SMA600'][last_index] and btc > 0.0001:
                usdt = btc * ohlc['close'][index]
                usdt = usdt - 0.0007 * usdt
                btc = 0
                print("Sell BTC at", ohlc['close'][index], '$ the', index)
            last_index = index

        final_result = usdt + btc * ohlc['close'].iloc[-1]
        print("Final result", final_result, 'USDT')
        print("Buy and hold result", (1000 / ohlc['close'].iloc[0]) * ohlc['close'].iloc[-1], 'USDT')


if __name__ == "__main__":
    bclient = BinanceClient()
    ohlc = bclient.get_ohlc('BTCUSDT', '1h', 1606939487)
    print(ohlc.size)
    bibot = BinanceBot()
    bibot.launchBot(ohlc)

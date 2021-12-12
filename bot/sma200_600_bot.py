import ta
from bot.generic_bot import GenericBot
from input.binance_exchange.binance_client import BinanceClient


class Sma200600Bot(GenericBot):

    NAME = "SMA200 + SMA600"

    def __init__(self):
        pass

    @classmethod
    def getName(cls):
        return cls.NAME

    @classmethod
    def description(cls):
        description = 'Ce bot permet de calculer les Moyennes Mobiles Simple 200 (rapide) et 600 (lente). ' \
                      'Achat lorque la MM200 croise a la hausse la MM600' \
                      'Vente lorque la MM200 croise a la baisse la MM600'
        return description

    def backTest(self, ohlc):
        ohlc['SMA200'] = ta.trend.sma_indicator(ohlc['close'], 200)
        ohlc['SMA600'] = ta.trend.sma_indicator(ohlc['close'], 600)

        usdt = 1000
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
        # print("Buy and hold result", (1000 / ohlc['close'].iloc[0]) * ohlc['close'].iloc[-1], 'USDT')


if __name__ == "__main__":
    bclient = BinanceClient()
    ohlcs = bclient.get_ohlc('BTCUSDT', '1h', 1606939487)
    print(ohlcs.size)
    # ohlc_brochain = get_by_timestamp({'exchange': 'binance', 'pair': 'ETHUSDT', 'interval': '1h'}, 1606939487)
    sma_bot = Sma200600Bot()
    sma_bot.backTest(ohlcs)

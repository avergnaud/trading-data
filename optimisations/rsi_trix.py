import base64
import io
from math import ceil

import pandas as pd
import ta
from IPython.display import clear_output
from matplotlib import pyplot as plt

import warnings
from persistence.ohlc_dao import mongoDataToDataframe, get_by_timestamp
from utils.utils import pyplotToBase64Img


class RsiTrix:
    def __init__(self):
        pass

    # -- Condition to BUY market --
    @staticmethod
    def buyCondition(row, stoch_top):
        if row['TRIX_HISTO'] > 0 and row['STOCH_RSI'] < stoch_top:
            return True
        else:
            return False

    # -- Condition to SELL market --
    @staticmethod
    def sellCondition(row, stoch_bottom):
        if row['TRIX_HISTO'] < 0 and row['STOCH_RSI'] > stoch_bottom:
            return True
        else:
            return False

    # Permet de tester une plage de valeur pour un paramètre de l'indicateur Trix
    def launchOptimization(self, df):

        # -- Drop all columns we do not need --
        df.drop(df.columns.difference(['open', 'high', 'low', 'close', 'volume']), axis=1, inplace=True)

        # -- Indicators, you can edit every value --
        df['EMA200'] = ta.trend.ema_indicator(close=df['close'], window=200)
        # -- Trix Indicator --
        trix_length = 7
        trix_signal = 15
        df['TRIX'] = ta.trend.ema_indicator(
            ta.trend.ema_indicator(ta.trend.ema_indicator(close=df['close'], window=trix_length), window=trix_length),
            window=trix_length)
        df['TRIX_PCT'] = df["TRIX"].pct_change() * 100
        df['TRIX_SIGNAL'] = ta.trend.sma_indicator(df['TRIX_PCT'], trix_signal)
        df['TRIX_HISTO'] = df['TRIX_PCT'] - df['TRIX_SIGNAL']

        # -- Stochasitc RSI --
        df['STOCH_RSI'] = ta.momentum.stochrsi(close=df['close'], window=12, smooth1=3, smooth2=3)
        stoch_top = 0.7
        stoch_bottom = 0.28

        print("Indicators loaded 100%")

        # -- Uncomment the line below if you want to check your dataset with indicators --
        # print(df)

        newdt = pd.DataFrame(columns=['param1', 'result'])
        # df_test = df.copy()

        # -- Run le backtest sur une période donnée --
        df_test = df['2021-01-01':]

        # on test de 7 à 30 par pas de 1
        loopI = [7, 30, 1]
        enumI = ceil((loopI[1] - loopI[0]) / loopI[2])

        count = 0
        max_count = enumI
        for i in range(loopI[0], loopI[1], loopI[2]):
            clear_output(wait=True)
            count += 1
            # print("Loading...", count, '/', max_count)
            # -- You can change variables below --
            usdt = 1000
            coin = 0

            df_test['STOCH_RSI'] = ta.momentum.stochrsi(close=df_test.loc[:, 'close'], window=i, smooth1=3, smooth2=3)

            for index, row in df_test.iterrows():
                # BUY
                if self.buyCondition(row, stoch_top) and usdt > 0:
                    coin = (usdt / df_test['close'][index]) - 0.0007 * (usdt / df_test['close'][index])
                    usdt = 0

                # SELL
                elif self.sellCondition(row, stoch_bottom) and coin > 0:
                    usdt = coin * df_test['close'][index] - (0.0007 * coin * df_test['close'][index])
                    coin = 0

            myrow = {'param1': i, 'result': coin * df_test.iloc[len(df_test) - 1]['close'] + usdt}
            newdt = newdt.append(myrow, ignore_index=True)

        # Affichage en direct du résultat
        # print(dt.sort_values(by=['result']))

        # Affichage du graphe sous forme d image
        newdt.plot.scatter(x='param1', y=1, c='result', s=50, colormap='OrRd', figsize=(8, 6))
        # plt.show()
        return plt


if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    # bclient = BinanceClient()
    # 17 aout 2017
    # ohlcs = bclient.get_ohlc('ETHUSDT', '1h', 1502928000000)
    # print(ohlcs.size)
    ohlc_brochain = mongoDataToDataframe(
        get_by_timestamp({'exchange': 'binance', 'pair': 'ETHUSDT', 'interval': '1h'}, 1606939487))
    rsitrix = RsiTrix()
    plt = rsitrix.launchOptimization(ohlc_brochain)

    print(pyplotToBase64Img(plt))
    # affiche les résultat en tableau

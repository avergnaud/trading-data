from math import ceil

import pandas as pd
import ta
from IPython.display import clear_output
from matplotlib import pyplot as plt

from input.binance_exchange.binance_client import BinanceClient

dfTest = None
dt = None
dt = pd.DataFrame(columns=['param1', 'result'])


class ParamOpti:
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
        df.drop(df.columns.difference(['open', 'high', 'low', 'close', 'volume']), 1, inplace=True)

        # -- Indicators, you can edit every value --
        df['EMA200'] = ta.trend.ema_indicator(close=df['close'], window=200)
        # -- Trix Indicator --
        trixLength = 7
        trixSignal = 15
        df['TRIX'] = ta.trend.ema_indicator(
            ta.trend.ema_indicator(ta.trend.ema_indicator(close=df['close'], window=trixLength), window=trixLength),
            window=trixLength)
        df['TRIX_PCT'] = df["TRIX"].pct_change() * 100
        df['TRIX_SIGNAL'] = ta.trend.sma_indicator(df['TRIX_PCT'], trixSignal)
        df['TRIX_HISTO'] = df['TRIX_PCT'] - df['TRIX_SIGNAL']

        # -- Stochasitc RSI --
        df['STOCH_RSI'] = ta.momentum.stochrsi(close=df['close'], window=12, smooth1=3, smooth2=3)
        stochTop = 0.7
        stochBottom = 0.28

        print("Indicators loaded 100%")

        # -- Uncomment the line below if you want to check your dataset with indicators --
        # df

        dt = pd.DataFrame(columns=['param1', 'result'])
        # dfTest = df.copy()

        # -- Run le backtest sur une période donnée --
        dfTest = df['2021-01-01':]

        # on test de 7 à 30 par pas de 1
        loopI = [7, 30, 1]
        enumI = ceil((loopI[1] - loopI[0]) / loopI[2])

        count = 0
        max_count = enumI
        for i in range(loopI[0], loopI[1], loopI[2]):
            clear_output(wait=True)
            count += 1
            print("Loading...", count, '/', max_count)
            # -- You can change variables below --
            usdt = 1000
            coin = 0

            dfTest['STOCH_RSI'] = ta.momentum.stochrsi(close=dfTest['close'], window=i, smooth1=3, smooth2=3)

            for index, row in dfTest.iterrows():
                # BUY
                if self.buyCondition(row, stochTop) and usdt > 0:
                    coin = (usdt / dfTest['close'][index]) - 0.0007 * (usdt / dfTest['close'][index])
                    usdt = 0

                # SELL
                elif self.sellCondition(row, stochBottom) and coin > 0:
                    usdt = coin * dfTest['close'][index] - (0.0007 * coin * dfTest['close'][index])
                    coin = 0

            myrow = {'param1': i, 'result': coin * dfTest.iloc[len(dfTest) - 1]['close'] + usdt}
            dt = dt.append(myrow, ignore_index=True)

        # Affichage du graphe sous forme d image
        dt.plot.scatter(x='param1', y=1, c='result', s=50, colormap='OrRd', figsize=(8, 6))
        plt.show()

        return dt


if __name__ == "__main__":
    bclient = BinanceClient()
    # 17 aout 2017
    ohlcs = bclient.get_ohlc('ETHUSDT', '1h', 1502928000000)
    # print(ohlcs.size)
    param_opti = ParamOpti()
    dt = param_opti.launchOptimization(ohlcs)
    # affiche les résultat en tableau
    print(dt.sort_values(by=['result']))

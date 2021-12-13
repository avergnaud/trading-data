import json

import pandas as pd


class BacktestResult:
    performance = ''
    inital_wallet = ''
    final_wallet = ''
    performanceVSUSDollar = ''
    performanceVSBuyAndHold = ''
    negativeTradesNumber = ''
    positiveTradesNumber = ''
    avgPositiveTrades = ''
    avgNegativeTrades = ''
    bestTrade = ''
    worstTrade = ''
    worstDrawback = ''
    totalFee = ''

    # def __init__(self):

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    def setInformations(self, ohlc, dt, wallet, inital_wallet):
        dt = dt.set_index(dt['date'])
        dt.index = pd.to_datetime(dt.index)

        dt['resultat'] = dt['wallet'].diff()
        dt['resultat%'] = dt['wallet'].pct_change() * 100
        dt.loc[dt['position'] == 'Buy', 'resultat'] = None
        dt.loc[dt['position'] == 'Buy', 'resultat%'] = None

        dt['tradeIs'] = ''
        dt.loc[dt['resultat'] > 0, 'tradeIs'] = 'Good'
        dt.loc[dt['resultat'] <= 0, 'tradeIs'] = 'Bad'

        ini_close = ohlc.iloc[0]['close']
        last_close = ohlc.iloc[len(ohlc) - 1]['close']

        hold_porcentage = ((last_close - ini_close) / ini_close) * 100
        algo_porcentage = ((wallet - inital_wallet) / inital_wallet) * 100
        vs_hold_porcentage = ((algo_porcentage - hold_porcentage) / hold_porcentage) * 100

        self.performance = str(round(algo_porcentage, 2)) + "%"
        self.inital_wallet = inital_wallet
        self.final_wallet = round(wallet,2)

        self.performanceVSUSDollar = str(round(hold_porcentage, 2)) + "%"
        self.performanceVSBuyAndHold = str(round(vs_hold_porcentage, 2)) + "%"

        self.negativeTradesNumber = str(dt.groupby('tradeIs')['date'].nunique()['Bad'])
        self.positiveTradesNumber = str(dt.groupby('tradeIs')['date'].nunique()['Good'])
        self.avgPositiveTrades = str(round(
            dt.loc[dt['tradeIs'] == 'Good', 'resultat%'].sum() / dt.loc[dt['tradeIs'] == 'Good', 'resultat%'].count(),
            2)) + "%"
        self.avgNegativeTrades = str(round(
            dt.loc[dt['tradeIs'] == 'Bad', 'resultat%'].sum() / dt.loc[dt['tradeIs'] == 'Bad', 'resultat%'].count(),
            2)) + "%"
        idbest = dt.loc[dt['tradeIs'] == 'Good', 'resultat%'].idxmax()
        idworst = dt.loc[dt['tradeIs'] == 'Bad', 'resultat%'].idxmin()
        self.bestTrade = "{0}%, the {1}".format(str(round(dt.loc[dt['tradeIs'] == 'Good', 'resultat%'].max(), 2)),
                                                str(dt['date'][idbest]))
        self.worstTrade = "{0}%, the {1}".format(str(round(dt.loc[dt['tradeIs'] == 'Bad', 'resultat%'].min(), 2)),
                                                 str(dt['date'][idworst]))
        self.worstDrawback = str(100 * round(dt['drawBack'].min(), 2)) + "%"
        self.totalFee = str(round(dt['frais'].sum(), 2)) + "$"


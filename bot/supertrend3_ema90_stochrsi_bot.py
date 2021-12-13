import os

from backtest.backtest_result import BacktestResult
from bot.generic_bot import GenericBot
import ftx
import pandas as pd
import pandas_ta as pda
import ta
from persistence.ohlc_dao import mongoDataToDataframe, get_by_timestamp_interval, get_by_timestamp

api_endpoint = 'https://ftx.com/api'
api_key = os.getenv('FTX_API_KEY')
api_secret = os.getenv('FTX_API_SECRET')


class Supertrend3Ema90StochRsiBot(GenericBot):

    NAME = "ema90_stochastic_rsi_super_trends"

    def __init__(self):
        self.client = ftx.FtxClient()
        pass

    @classmethod
    def getName(cls):
        return cls.NAME

    @classmethod
    def description(cls):
        description = 'Ce bot permet de calculer la Moyenne Mobile Exponentielle 90, le Stochastic RSI ainsi que 3 ' \
                      'supertrend de longueur et de multiplier différents' \
                      'Achat lorque qu au moins 2 supertrend sont à la hausse, que le prix de cloture est au dessus ' \
                      'du EMA90 que le RSI < 0.8' \
                      'Vente lorque qu au moins 2 supertrend sont à la baisse, que le RSI > 0.2.' \
                      '4000% sur l ADA'
        return description

    def back_test_between(self, ohlc_definition, from_timestamp_seconds, to_timestamp_seconds):
        ohlcs = mongoDataToDataframe(
            get_by_timestamp_interval(ohlc_definition, from_timestamp_seconds, to_timestamp_seconds))
        return self.backTest(ohlcs)

    def backTest(self, ohlc):
        ohlc.drop(ohlc.columns.difference(['open', 'high', 'low', 'close', 'volume']), axis=1, inplace=True)
        dt = pd.DataFrame(columns=['date', 'position', 'price', 'frais', 'fiat', 'coins', 'wallet', 'drawBack'])

        ohlc['EMA90'] = ta.trend.ema_indicator(ohlc['close'], 90)
        ohlc['STOCH_RSI'] = ta.momentum.stochrsi(ohlc['close'])

        ST_length = 20
        ST_multiplier = 3.0
        superTrend = pda.supertrend(ohlc['high'], ohlc['low'], ohlc['close'], length=ST_length,
                                    multiplier=ST_multiplier)
        ohlc['SUPER_TREND'] = superTrend['SUPERT_' + str(ST_length) + "_" + str(ST_multiplier)]
        ohlc['SUPER_TREND_DIRECTION1'] = superTrend['SUPERTd_' + str(ST_length) + "_" + str(ST_multiplier)]

        ST_length = 20
        ST_multiplier = 4.0
        superTrend = pda.supertrend(ohlc['high'], ohlc['low'], ohlc['close'], length=ST_length,
                                    multiplier=ST_multiplier)
        ohlc['SUPER_TREND'] = superTrend['SUPERT_' + str(ST_length) + "_" + str(ST_multiplier)]
        ohlc['SUPER_TREND_DIRECTION2'] = superTrend['SUPERTd_' + str(ST_length) + "_" + str(ST_multiplier)]

        ST_length = 40
        ST_multiplier = 8.0
        superTrend = pda.supertrend(ohlc['high'], ohlc['low'], ohlc['close'], length=ST_length,
                                    multiplier=ST_multiplier)
        ohlc['SUPER_TREND'] = superTrend['SUPERT_' + str(ST_length) + "_" + str(ST_multiplier)]
        ohlc['SUPER_TREND_DIRECTION3'] = superTrend['SUPERTd_' + str(ST_length) + "_" + str(ST_multiplier)]

        usdt = 1000
        coin = 0
        wallet = 1000
        lastAth = 0
        fee = 0.0007
        lastRow = ohlc.iloc[0]
        stopLoss = 0
        goOn = True

        for index, row in ohlc.iterrows():
            # Buy
            if row['SUPER_TREND_DIRECTION1'] + row['SUPER_TREND_DIRECTION2'] + row['SUPER_TREND_DIRECTION3'] >= 1 and \
                    row['STOCH_RSI'] < 0.8 and row['close'] > row['EMA90'] and usdt > 0 and goOn is True:
                buyPrice = row['close']
                # stopLoss = buyPrice - 0.02 * buyPrice
                coin = usdt / buyPrice
                frais = fee * coin
                coin = coin - frais
                usdt = 0
                wallet = coin * row['close']
                if wallet > lastAth:
                    lastAth = wallet
                # print("Buy COIN at",buyPrice,'$ the', index)
                myrow = {'date': index, 'position': "Buy", 'price': buyPrice, 'frais': frais * row['close'],
                         'fiat': usdt, 'coins': coin, 'wallet': wallet, 'drawBack': (wallet - lastAth) / lastAth}
                dt = dt.append(myrow, ignore_index=True)

            # Stop Loss
            # elif row['low'] < stopLoss and coin > 0:
            #   sellPrice = stopLoss
            #   usdt = coin * sellPrice
            #   frais = 0.005 * usdt
            #   usdt = usdt - frais
            #   coin = 0
            #   goOn = False
            #   wallet = usdt
            #   if wallet > lastAth:
            #     lastAth = wallet
            #   # print("Sell COIN at Stop Loss",sellPrice,'$ the', index)
            #   myrow = {'date': index,'position': "Sell",'price': sellPrice,'frais': frais,'fiat': usdt,'coins': coin,'wallet': wallet,'drawBack':(wallet-lastAth)/lastAth}
            #   dt = dt.append(myrow,ignore_index=True)

            # Sell
            elif row['SUPER_TREND_DIRECTION1'] + row['SUPER_TREND_DIRECTION2'] + row['SUPER_TREND_DIRECTION3'] < 1 and \
                    row['STOCH_RSI'] > 0.2:
                goOn = True
                if coin > 0:
                    sellPrice = row['close']
                    usdt = coin * sellPrice
                    frais = fee * usdt
                    usdt = usdt - frais
                    coin = 0
                    wallet = usdt
                    if wallet > lastAth:
                        lastAth = wallet
                    # print("Sell COIN at",sellPrice,'$ the', index)
                    myrow = {'date': index, 'position': "Sell", 'price': sellPrice, 'frais': frais, 'fiat': usdt,
                             'coins': coin, 'wallet': wallet, 'drawBack': (wallet - lastAth) / lastAth}
                    dt = dt.append(myrow, ignore_index=True)

            lastRow = row

        backtest_result = BacktestResult()
        backtest_result.setInformations(ohlc, dt, wallet, usdt)
        return backtest_result


if __name__ == "__main__":
    # entre le 01/01/2018 et le 31/12/2019
    # ohlc_brochain = mongoDataToDataframe(
    # get_by_timestamp_interval({'exchange': 'binance', 'pair': 'ETHUSDT', 'interval': '1h'}, 1514764800, 1577836799))
    # Depuis le 17 aout 2017
    ohlc_brochain = mongoDataToDataframe(
        get_by_timestamp({'exchange': 'binance', 'pair': 'ADAUSDT', 'interval': '1h'}, 1502928000))
    supertrend3ema90stochrsi = Supertrend3Ema90StochRsiBot()
    supertrend3ema90stochrsi.backTest(ohlc_brochain)

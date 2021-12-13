import os

import ftx
import pandas as pd
import ta

from backtest.backtest_result import BacktestResult
from bot.generic_bot import GenericBot
from persistence.ohlc_dao import mongoDataToDataframe, get_by_timestamp_interval

api_endpoint = 'https://ftx.com/api'
api_key = os.getenv('FTX_API_KEY')
api_secret = os.getenv('FTX_API_SECRET')


class MacdStochRsiBot(GenericBot):
    NAME: str = "macd_stochastic_rsi"

    def __init__(self):
        self.client = ftx.FtxClient()
        pass

    @classmethod
    def getName(cls):
        return cls.NAME

    @classmethod
    def description(cls):
        description = 'Ce bot permet de calculer le MACD plus le Stochastic RSI ' \
                      'Achat lorque le MACD croise sa moyenne mobile à la hausse et que le RSI < 0.7' \
                      'Vente lorque le MACD croise sa moyenne mobile à la baisse que le RSI > 0.2'
        return description

    def back_test_between(self, ohlc_definition, from_timestamp_seconds, to_timestamp_seconds):
        ohlcs = mongoDataToDataframe(
            get_by_timestamp_interval(ohlc_definition, from_timestamp_seconds, to_timestamp_seconds))
        return self.backTest(ohlcs)

    def backTest(self, ohlc):
        dt = pd.DataFrame(columns=['date', 'position', 'price', 'frais', 'fiat', 'coins', 'wallet', 'drawBack'])

        ohlc['MACD'] = ta.trend.macd(ohlc['close'], 26, 12)
        ohlc['MACD_SIGNAL'] = ta.trend.macd_signal(ohlc['close'])
        ohlc['MACD_HIST'] = ta.trend.macd_diff(ohlc['close'])
        ohlc['STOCH_RSI'] = ta.momentum.stochrsi(ohlc['close'])

        usdt = 1000
        initial_wallet = usdt
        coin = 0
        wallet = 1000
        last_ath = 0
        fee = 0.0007

        for index, row in ohlc.iterrows():
            # Buy
            if row['MACD'] > row['MACD_SIGNAL'] and row['STOCH_RSI'] < 0.7 and usdt > 0:
                coin = usdt / row['close']
                frais = fee * coin
                coin = coin - frais
                usdt = 0
                wallet = coin * row['close']
                if wallet > last_ath:
                    last_ath = wallet
                # print("Buy COIN at", ohlc['close'][index], '$ the', index)
                myrow = {'date': index, 'position': "Buy", 'price': row['close'], 'frais': frais, 'fiat': usdt,
                         'coins': coin, 'wallet': wallet, 'drawBack': (wallet - last_ath) / last_ath}
                dt = dt.append(myrow, ignore_index=True)

            # Sell
            if row['MACD'] < row['MACD_SIGNAL'] and row['STOCH_RSI'] > 0.3 and coin > 0:
                usdt = coin * row['close']
                frais = fee * usdt
                usdt = usdt - frais
                coin = 0
                wallet = usdt
                if wallet > last_ath:
                    last_ath = wallet
                # print("Sell COIN at", ohlc['close'][index], '$ the', index)
                myrow = {'date': index, 'position': "Sell", 'price': row['close'], 'frais': frais, 'fiat': usdt,
                         'coins': coin, 'wallet': wallet, 'drawBack': (wallet - last_ath) / last_ath}
                dt = dt.append(myrow, ignore_index=True)

        backtest_result = BacktestResult()
        backtest_result.setInformations(ohlc, dt, wallet, initial_wallet)
        return backtest_result


if __name__ == "__main__":
    ohlc_brochain = mongoDataToDataframe(
        get_by_timestamp_interval({'exchange': 'binance', 'pair': 'ETHUSDT', 'interval': '1h'}, 1514764800, 1577836799))
    # print(ohlcs.size)
    macdstochrsibot = MacdStochRsiBot()
    macdstochrsibot.backTest(ohlc_brochain)

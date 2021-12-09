import os
from math import floor

import ftx
import pandas as pd
import ta

from persistence.ohlc_dao import mongoDataToDataframe, get_by_timestamp_interval

api_endpoint = 'https://ftx.com/api'
api_key = os.getenv('FTX_API_KEY')
api_secret = os.getenv('FTX_API_SECRET')


class Ema2848StochRsiBot:
    def __init__(self):
        self.client = ftx.FtxClient()
        pass

    @staticmethod
    def description():
        description = 'Ce bot permet de calculer les Moyennes Mobiles Exponentielles 28 et 48 plus le Stochastic RSI ' \
                      'Achat lorque la EMA28 croise a la hausse la EMA48 et que le RSI < 0.8' \
                      'Vente lorque la EMA28 croise a la baisse la EMA48 et que le RSI > 0.2'
        return description

    @staticmethod
    def getBalance(myclient, coin):
        json_balance = myclient.get_balances()
        if not json_balance:
            return 0
        panda_balance = pd.DataFrame(json_balance)
        print(panda_balance)
        if panda_balance.loc[panda_balance['coin'] == coin].empty:
            return 0
        else:
            return float(panda_balance.loc[panda_balance['coin'] == coin]['total'])

    @staticmethod
    def truncate(n, decimals=0):
        r = floor(float(n) * 10 ** decimals) / 10 ** decimals
        return str(r)

    def backTest(self, ohlc):

        ohlc['EMA28'] = ta.trend.ema_indicator(ohlc['close'], 28)
        ohlc['EMA48'] = ta.trend.ema_indicator(ohlc['close'], 48)
        ohlc['STOCH_RSI'] = ta.momentum.stochrsi(ohlc['close'])

        usdt = 1000
        initalWallet = usdt
        coin = 0
        wallet = 1000
        last_ath = 0
        fee = 0.0007

        for index, row in ohlc.iterrows():
            # Buy
            if row['EMA28'] > row['EMA48'] and row['STOCH_RSI'] < 0.8 and usdt > 0:
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
                ohlc = ohlc.append(myrow, ignore_index=True)

            # Sell
            if row['EMA28'] < row['EMA48'] and row['STOCH_RSI'] > 0.2 and coin > 0:
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
                ohlc = ohlc.append(myrow, ignore_index=True)

        print("Final balance :", round(wallet, 2), "$")
        print("Performance vs US Dollar :", round(((wallet - initalWallet) / initalWallet) * 100, 2), "%")

    # Utilisation en condition réelle
    def launchBot(self, ohlc):
        account_name = ''
        pair_symbol = 'ETH/USD'
        fiat_symbol = 'USD'
        crypto_symbol = 'ETH'
        truncate = 3

        ohlc['EMA28'] = ta.trend.ema_indicator(ohlc['close'], 28)
        ohlc['EMA48'] = ta.trend.ema_indicator(ohlc['close'], 48)
        ohlc['STOCH_RSI'] = ta.momentum.stochrsi(ohlc['close'])

        fiat_amount = self.getBalance(self.client, fiat_symbol)
        crypto_amount = self.getBalance(self.client, crypto_symbol)
        actual_price = ohlc['close'].iloc[-1]

        min_token = 5 / actual_price
        print('coin price :', actual_price, 'usd balance', fiat_amount, 'coin balance :', crypto_amount)

        if ohlc['EMA28'].iloc[-2] > ohlc['EMA48'].iloc[-2] and ohlc['STOCH_RSI'].iloc[-2] < 0.8:
            if float(fiat_amount) > 5:
                quantity_buy = self.truncate(float(fiat_amount) / actual_price, truncate)
                buy_order = self.client.place_order(
                    market=pair_symbol,
                    side="buy",
                    price=None,
                    size=quantity_buy,
                    type='market')
                print("BUY", buy_order)
            else:
                print("If you  give me more USD I will buy more", crypto_symbol)

        elif ohlc['EMA28'].iloc[-2] < ohlc['EMA48'].iloc[-2] and ohlc['STOCH_RSI'].iloc[-2] > 0.2:
            if float(crypto_amount) > min_token:
                sell_order = self.client.place_order(
                    market=pair_symbol,
                    side="sell",
                    price=None,
                    size=self.truncate(truncate),
                    type='market')
                print("SELL", sell_order)
            else:
                print("If you give me more", crypto_symbol, "I will sell it")
        else:
            print("No opportunity to take")


if __name__ == "__main__":
    # bclient = BinanceClient()
    # ohlcs = bclient.get_ohlc('ETHUSDT', '1h', 1514764800000, 1577836799000)
    # print(ohlcs)
    # entre le 01/01/2018 et le 31/12/2019
    ohlc_brochain = mongoDataToDataframe(
        get_by_timestamp_interval({'exchange': 'binance', 'pair': 'ETHUSDT', 'interval': '1h'}, 1514764800, 1577836799))
    # print(ohlcs.size)
    ema2848stockrsi = Ema2848StochRsiBot()
    ema2848stockrsi.backTest(ohlc_brochain)

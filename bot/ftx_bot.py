from math import floor

import pandas as pd
import ta

from input.ftx_exchange.ftx_client import FtxClient


class FtxBot:
    def __init__(self):
        pass

    @staticmethod
    def getBalance(myclient, coin):
        jsonBalance = myclient.get_balances()
        if not jsonBalance:
            return 0
        panda_balance = pd.DataFrame(jsonBalance)
        print(panda_balance)
        if panda_balance.loc[panda_balance['coin'] == coin].empty:
            return 0
        else:
            return float(panda_balance.loc[panda_balance['coin'] == coin]['total'])

    @staticmethod
    def truncate(n, decimals=0):
        r = floor(float(n) * 10 ** decimals) / 10 ** decimals
        return str(r)

    def launchBot2(self, ohlc):

        accountName = ''
        pairSymbol = 'ETH/USD'
        fiatSymbol = 'USD'
        cryptoSymbol = 'ETH'
        myTruncate = 3

        ohlc['EMA28'] = ta.trend.ema_indicator(ohlc['close'], 28)
        ohlc['EMA48'] = ta.trend.ema_indicator(ohlc['close'], 48)
        ohlc['STOCH_RSI'] = ta.momentum.stochrsi(ohlc['close'])

        usdt = 1000
        initalWallet = usdt
        coin = 0
        wallet = 1000
        lastAth = 0
        lastIndex = ohlc.first_valid_index()
        fee = 0.0007

        for index, row in ohlc.iterrows():
            # Buy
            if row['EMA28'] > row['EMA48'] and row['STOCH_RSI'] < 0.8 and usdt > 0:
                coin = usdt / row['close']
                frais = fee * coin
                coin = coin - frais
                usdt = 0
                wallet = coin * row['close']
                if wallet > lastAth:
                    lastAth = wallet
                # print("Buy COIN at",df['close'][index],'$ the', index)
                myrow = {'date': index, 'position': "Buy", 'price': row['close'], 'frais': frais, 'fiat': usdt,
                         'coins': coin, 'wallet': wallet, 'drawBack': (wallet - lastAth) / lastAth}
                ohlc = ohlc.append(myrow, ignore_index=True)

            # Sell
            if row['EMA28'] < row['EMA48'] and row['STOCH_RSI'] > 0.2 and coin > 0:
                usdt = coin * row['close']
                frais = fee * usdt
                usdt = usdt - frais
                coin = 0
                wallet = usdt
                if wallet > lastAth:
                    lastAth = wallet
                # print("Sell COIN at",df['close'][index],'$ the', index)
                myrow = {'date': index, 'position': "Sell", 'price': row['close'], 'frais': frais, 'fiat': usdt,
                         'coins': coin, 'wallet': wallet, 'drawBack': (wallet - lastAth) / lastAth}
                ohlc = ohlc.append(myrow, ignore_index=True)
            lastIndex = index

        print("Final balance :", round(wallet, 2), "$")

    def launchBot(self, ohlc):
        accountName = ''
        pairSymbol = 'ETH/USD'
        fiatSymbol = 'USD'
        cryptoSymbol = 'ETH'
        myTruncate = 3

        ohlc['EMA28'] = ta.trend.ema_indicator(ohlc['close'], 28)
        ohlc['EMA48'] = ta.trend.ema_indicator(ohlc['close'], 48)
        ohlc['STOCH_RSI'] = ta.momentum.stochrsi(ohlc['close'])

        fiatAmount = 1000
        cryptoAmount = 0
        # fiatAmount = getBalance(client, fiatSymbol)
        # cryptoAmount = getBalance(client, cryptoSymbol)
        # actualPrice = ohlc['close'].iloc[-1]

        for index, row in ohlc.iterrows():
            actualPrice = ohlc['close'][last_index]
            minToken = 5 / actualPrice
            # print('coin price :', actualPrice, 'usd balance', fiatAmount, 'coin balance :', cryptoAmount)

            # if ohlc['EMA28'].iloc[-2] > ohlc['EMA48'].iloc[-2] and ohlc['STOCH_RSI'].iloc[-2] < 0.8:
            if ohlc['EMA28'][last_index] > ohlc['EMA48'][last_index] and ohlc['STOCH_RSI'][last_index] < 0.8:
                if float(fiatAmount) > 5:
                    quantityBuy = self.truncate(float(fiatAmount) / actualPrice, myTruncate)
                    print("quantityBuy : ", quantityBuy)
                    # buyOrder = client.place_order(
                    #     market=pairSymbol,
                    #     side="buy",
                    #     price=None,
                    #     size=quantityBuy,
                    #     type='market')
                    # print("BUY", buyOrder)
                    cryptoAmount = float(quantityBuy) - 0.0007 * float(quantityBuy)
                    fiatAmount = 0
                    print("Buy at", ohlc['close'][index], '$ the', index)
                else:
                    print("If you  give me more USD I will buy more", cryptoSymbol)

            # elif ohlc['EMA28'].iloc[-2] < ohlc['EMA48'].iloc[-2] and ohlc['STOCH_RSI'].iloc[-2] > 0.2:
            elif ohlc['EMA28'][last_index] < ohlc['EMA48'][last_index] and ohlc['STOCH_RSI'][last_index] > 0.2:
                if float(cryptoAmount) > minToken:
                    # sellOrder = client.place_order(
                    #     market=pairSymbol,
                    #     side="sell",
                    #     price=None,
                    #     size=truncate(myTruncate),
                    #     type='market')
                    # print("SELL", sellOrder)
                    fiatAmount = cryptoAmount * ohlc['close'][index]
                    fiatAmount = fiatAmount - 0.0007 * fiatAmount
                    cryptoAmount = 0
                    print("Sell at", ohlc['close'][index], '$ the', index)
                else:
                    print("If you give me more", cryptoSymbol, "I will sell it")
            else:
                print("No opportunity to take")
            last_index = index


if __name__ == "__main__":
    ftxclient = FtxClient()
    ohlcs = ftxclient.get_ohlc('ETH/USDT', 3600, 1483228817)
    # print(ohlcs.size)
    bibot = FtxBot()
    bibot.launchBot2(ohlcs)

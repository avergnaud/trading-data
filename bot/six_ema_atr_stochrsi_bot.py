import pandas as pd
import ta

from backtest.backtest_result import BacktestResult
from bot.generic_bot import GenericBot
from input.binance_exchange.binance_client import BinanceClient
from persistence.ohlc_dao import get_by_timestamp_interval, mongoDataToDataframe


class Ema6AtrStochRsiBot(GenericBot):
    NAME: str = "6_ema_stochastic_rsi"

    def __init__(self):
        pass

    @classmethod
    def getName(cls):
        return cls.NAME

    @classmethod
    def description(cls):
        description = 'Statégie de l aligator :' \
                      'Achat si les 6 moyennes mobiles sont orientées dans le bon sens et que le stochRsi n est pas en surachat (donc stochRsi < 0.82)' \
                      'Vente lorque la MM200 croise la MM la plus basse et que le stochRsi n est pas en survente (donc stochRsi > 0.2)' \
                      '8400% sur LINK, 3200% sur bitcoin '
        return description

    @staticmethod
    def buyCondition(row):
        if row['EMA1'] > row['EMA2'] > row['EMA3'] > row['EMA4'] > row['EMA5'] > row['EMA6'] \
                and row['STOCH_RSI'] < 0.82:
            return True
        else:
            return False

    @staticmethod
    def sellCondition(row):
        if row['EMA6'] > row['EMA1'] and row['STOCH_RSI'] > 0.2:
            return True
        else:
            return False

    def back_test_between(self, ohlc_definition, from_timestamp_seconds, to_timestamp_seconds):
        ohlcs = mongoDataToDataframe(
            get_by_timestamp_interval(ohlc_definition, from_timestamp_seconds, to_timestamp_seconds))
        return self.backTest(ohlcs)

    def backTest(self, ohlc):
        ohlc.drop(ohlc.columns.difference(['open', 'high', 'low', 'close', 'volume']), axis=1, inplace=True)
        dt = pd.DataFrame(columns=['date', 'position', 'price', 'frais', 'fiat', 'coins', 'wallet', 'drawBack'])

        # Exponential Moving Average non optimisé
        ohlc['EMA1'] = ta.trend.ema_indicator(close=ohlc['close'], window=7)
        ohlc['EMA2'] = ta.trend.ema_indicator(close=ohlc['close'], window=30)
        ohlc['EMA3'] = ta.trend.ema_indicator(close=ohlc['close'], window=50)
        ohlc['EMA4'] = ta.trend.ema_indicator(close=ohlc['close'], window=100)
        ohlc['EMA5'] = ta.trend.ema_indicator(close=ohlc['close'], window=121)
        ohlc['EMA6'] = ta.trend.ema_indicator(close=ohlc['close'], window=200)

        # Stochastic RSI
        ohlc['STOCH_RSI'] = ta.momentum.stochrsi(close=ohlc['close'], window=14, smooth1=3, smooth2=3)  # Non moyenné

        # Average True Range (ATR)
        ohlc['ATR'] = ta.volatility.average_true_range(high=ohlc['high'], low=ohlc['low'], close=ohlc['close'],
                                                       window=14)

        usdt = 1000
        inital_wallet = usdt
        coin = 0
        wallet = 1000
        last_ath = 0
        previous_row = ohlc.iloc[0]
        maker_fee = 0.0003
        taker_fee = 0.0007
        stop_loss = 0
        take_profit = 500000
        buy_ready = True
        sell_ready = True

        for index, row in ohlc.iterrows():
            # Buy market order
            if self.buyCondition(row) is True and usdt > 0 and buy_ready is True:
                # You can define here at what price you buy
                buyPrice = row['close']

                # Define the price of you SL and TP or comment it if you don't want a SL or TP
                # stopLoss = buyPrice - 2 * row['ATR']
                # takeProfit = buyPrice + 4 * row['ATR']

                coin = usdt / buyPrice
                fee = taker_fee * coin
                coin = coin - fee
                usdt = 0
                wallet = coin * row['close']
                if wallet > last_ath:
                    last_ath = wallet

                # print("Buy COIN at",buyPrice,'$ the', index)
                myrow = {'date': index, 'position': "Buy", 'reason': 'Buy Market', 'price': buyPrice,
                         'frais': fee * row['close'], 'fiat': usdt, 'coins': coin, 'wallet': wallet,
                         'drawBack': (wallet - last_ath) / last_ath}
                dt = dt.append(myrow, ignore_index=True)

                # Stop Loss
            elif row['low'] < stop_loss and coin > 0:

                sellPrice = stop_loss

                usdt = coin * sellPrice
                fee = maker_fee * usdt
                usdt = usdt - fee
                coin = 0
                buy_ready = False
                wallet = usdt
                if wallet > last_ath:
                    last_ath = wallet
                # print("Sell COIN at Stop Loss",sellPrice,'$ the', index)
                myrow = {'date': index, 'position': "Sell", 'reason': 'Sell Stop Loss', 'price': sellPrice,
                         'frais': fee, 'fiat': usdt, 'coins': coin, 'wallet': wallet,
                         'drawBack': (wallet - last_ath) / last_ath}
                dt = dt.append(myrow, ignore_index=True)

                # Take Profit
            elif row['high'] > take_profit and coin > 0:

                sellPrice = take_profit

                usdt = coin * sellPrice
                fee = maker_fee * usdt
                usdt = usdt - fee
                coin = 0
                buy_ready = False
                wallet = usdt
                if wallet > last_ath:
                    last_ath = wallet
                # print("Sell COIN at Take Profit Loss",sellPrice,'$ the', index)
                myrow = {'date': index, 'position': "Sell", 'reason': 'Sell Take Profit', 'price': sellPrice,
                         'frais': fee, 'fiat': usdt, 'coins': coin, 'wallet': wallet,
                         'drawBack': (wallet - last_ath) / last_ath}
                dt = dt.append(myrow, ignore_index=True)

                # Sell Market
            elif self.sellCondition(row) is True:
                buy_ready = True
                if coin > 0 and sell_ready == True:
                    sellPrice = row['close']
                    usdt = coin * sellPrice
                    frais = taker_fee * usdt
                    usdt = usdt - frais
                    coin = 0
                    wallet = usdt
                    if wallet > last_ath:
                        last_ath = wallet
                    # print("Sell COIN at",sellPrice,'$ the', index)
                    myrow = {'date': index, 'position': "Sell", 'reason': 'Sell Market', 'price': sellPrice,
                             'frais': frais, 'fiat': usdt, 'coins': coin, 'wallet': wallet,
                             'drawBack': (wallet - last_ath) / last_ath}
                    dt = dt.append(myrow, ignore_index=True)

            previous_row = row

        backtest_result = BacktestResult()
        backtest_result.setInformations(ohlc, dt, wallet, inital_wallet)
        return backtest_result

        # print("Buy and Hold Performence :", round(holdPorcentage, 2), "%")
        # Plein de donnée interessante
        # print("Performance vs Buy and Hold :", round(vsHoldPorcentage, 2), "%")
        # print("Number of negative trades : ", dt.groupby('tradeIs')['date'].nunique()['Bad'])
        # print("Number of positive trades : ", dt.groupby('tradeIs')['date'].nunique()['Good'])
        # print("Average Positive Trades : ", round(
        #     dt.loc[dt['tradeIs'] == 'Good', 'resultat%'].sum() / dt.loc[dt['tradeIs'] == 'Good', 'resultat%'].count(),
        #     2), "%")
        # print("Average Negative Trades : ", round(
        #     dt.loc[dt['tradeIs'] == 'Bad', 'resultat%'].sum() / dt.loc[dt['tradeIs'] == 'Bad', 'resultat%'].count(), 2),
        #       "%")
        # idbest = dt.loc[dt['tradeIs'] == 'Good', 'resultat%'].idxmax()
        # idworst = dt.loc[dt['tradeIs'] == 'Bad', 'resultat%'].idxmin()
        # print("Best trade +" + str(round(dt.loc[dt['tradeIs'] == 'Good', 'resultat%'].max(), 2)), "%, the ",
        #       dt['date'][idbest])
        # print("Worst trade", round(dt.loc[dt['tradeIs'] == 'Bad', 'resultat%'].min(), 2), "%, the ",
        #       dt['date'][idworst])
        # print("Worst drawBack", str(100 * round(dt['drawBack'].min(), 2)), "%")
        # print("Total fee : ", round(dt['frais'].sum(), 2), "$")
        # reasons = dt['reason'].unique()
        # for r in reasons:
        #     print(r + " number :", dt.groupby('reason')['date'].nunique()[r])
        #
        # dt[['wallet', 'price']].plot(subplots=True, figsize=(20, 10))


if __name__ == "__main__":
    bclient = BinanceClient()
    ohlcs = bclient.get_ohlc('BTCUSDT', '1h', 1606939487)
    # ohlc_brochain = get_by_timestamp({'exchange': 'binance', 'pair': 'ETHUSDT', 'interval': '1h'}, 1606939487)
    emaatrrsi_bot = Ema6AtrStochRsiBot()
    emaatrrsi_bot.backTest(ohlcs)

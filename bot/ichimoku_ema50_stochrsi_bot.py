import pandas as pd
import ta

from backtest.backtest_result import BacktestResult
from bot.generic_bot import GenericBot
from input.binance_exchange.binance_client import BinanceClient
from persistence.ohlc_dao import get_by_timestamp_interval


class IchimokuEma50StochRsiBot(GenericBot):

    NAME: str = "ema50_stochastic_rsi_ichimoku"

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
                      '6450% sur EGLD'
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
        ohlcs_list = get_by_timestamp_interval(ohlc_definition, from_timestamp_seconds, to_timestamp_seconds)
        ohlcs = pd.DataFrame(ohlcs_list)
        return self.backTest(ohlcs)

    def backTest(self, ohlc):
        ohlc.drop(ohlc.columns.difference(['open', 'high', 'low', 'close', 'volume']), axis=1, inplace=True)
        dt = pd.DataFrame(columns=['date', 'position', 'price', 'frais', 'fiat', 'coins', 'wallet', 'drawBack'])

        # Exponential Moving Average
        ohlc['EMA50']=ta.trend.ema_indicator(ohlc['close'], 50)

        # Stochastic RSI
        ohlc['STOCH_RSI'] = ta.momentum.stochrsi(close=ohlc['close'])

        # Ichomku cloud
        ohlc['KIJUN'] = ta.trend.ichimoku_base_line(ohlc['high'], ohlc['low'])
        ohlc['TENKAN'] = ta.trend.ichimoku_conversion_line(ohlc['high'], ohlc['low'])
        ohlc['SSA'] = ta.trend.ichimoku_a(ohlc['high'], ohlc['low'], 3, 38).shift(periods=48)
        ohlc['SSB'] = ta.trend.ichimoku_b(ohlc['high'], ohlc['low'], 38, 46).shift(periods=48)

        usdt = 1000
        inital_wallet = usdt
        coin = 0
        wallet = 1000
        last_ath = 0
        last_row = ohlc.iloc[0]
        fee = 0.0007
        stop_loss = 0

        for index, row in ohlc.iterrows():
            # Buy
            if row['close'] > row['SSA'] and row['close'] > row['SSB'] and row['STOCH_RSI'] < 0.8 and row['close'] > \
                    row['EMA50'] and usdt > 0:
                buy_price = row['close']
                # stopLoss = buyPrice - 0.05 * buyPrice
                coin = usdt / buy_price
                frais = fee * coin
                coin = coin - frais
                usdt = 0
                wallet = coin * row['close']
                if wallet > last_ath:
                    last_ath = wallet
                # print("Buy COIN at",buyPrice,'$ the', index)
                myrow = {'date': index, 'position': "Buy", 'price': buy_price, 'frais': frais, 'fiat': usdt,
                         'coins': coin, 'wallet': wallet, 'drawBack': (wallet - last_ath) / last_ath}
                dt = dt.append(myrow, ignore_index=True)

                # Stop Loss
                # elif row['low'] < stopLoss and coin > 0:
                #   sellPrice = stopLoss
                #   usdt = coin * sellPrice
                #   frais = 0.0002 * usdt
                #   usdt = usdt - frais
                #   coin = 0
                #   wallet = usdt
                #   if wallet > last_ath:
                #     last_ath = wallet
                #   # print("Sell COIN at",sellPrice,'$ the', index)
                #   myrow = {'date': index,'position': "Sell",'price': sellPrice,'frais': frais,'fiat': usdt,'coins': coin,'wallet': wallet,'drawBack':(wallet-last_ath)/last_ath}
                #   dt = dt.append(myrow,ignore_index=True)

                # Sell
            elif (row['close'] < row['SSA'] or row['close'] < row['SSB']) and row['STOCH_RSI'] > 0.2 and coin > 0:
                sell_price = row['close']
                usdt = coin * sell_price
                frais = fee * usdt
                usdt = usdt - frais
                coin = 0
                wallet = usdt
                if wallet > last_ath:
                    last_ath = wallet
                # print("Sell COIN at",sellPrice,'$ the', index)
                myrow = {'date': index, 'position': "Sell", 'price': sell_price, 'frais': frais, 'fiat': usdt,
                         'coins': coin, 'wallet': wallet, 'drawBack': (wallet - last_ath) / last_ath}
                dt = dt.append(myrow, ignore_index=True)

            last_row = row

        print("Final balance :", round(wallet, 2), "$")
        perf = str(round(((wallet - inital_wallet) / inital_wallet) * 100, 2)) + "%"
        print("Performance vs US Dollar :", perf)

        backtest_result = BacktestResult(perf)
        return backtest_result


if __name__ == "__main__":
    bclient = BinanceClient()
    ohlcs = bclient.get_ohlc('EGLDUSDT', '1h', 1577836800)
    # ohlc_brochain = get_by_timestamp({'exchange': 'binance', 'pair': 'ETHUSDT', 'interval': '1h'}, 1606939487)
    ichimokuemarsi_bot = IchimokuEma50StochRsiBot()
    ichimokuemarsi_bot.backTest(ohlcs)

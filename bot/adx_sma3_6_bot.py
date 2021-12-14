import pandas as pd
import ta

from backtest.backtest_result import BacktestResult
from bot.generic_bot import GenericBot
from persistence.ohlc_dao import get_by_timestamp_interval, mongoDataToDataframe


class AdxSma36Bot(GenericBot):
    NAME: str = "adx_sma_3_6"

    def __init__(self):
        pass

    @classmethod
    def getName(cls):
        return cls.NAME

    @classmethod
    def description(cls):
        description = 'AdxSmas '
        return description

    def back_test_between(self, ohlc_definition, from_timestamp_seconds, to_timestamp_seconds):
        ohlcs = mongoDataToDataframe(
            get_by_timestamp_interval(ohlc_definition, from_timestamp_seconds, to_timestamp_seconds))
        return self.backTest(ohlcs)

    def backTest(self, ohlc):

        dt = pd.DataFrame(columns=['date', 'position', 'price', 'frais', 'fiat', 'coins', 'wallet', 'drawBack'])

        ohlc['ADX'] = ta.trend.adx(ohlc['high'], ohlc['low'], ohlc['close'], 14)
        ohlc['SMA3'] = ta.trend.sma_indicator(ohlc['close'], 3)
        ohlc['SMA6'] = ta.trend.sma_indicator(ohlc['close'], 6)

        usdt = 1000
        inital_wallet = usdt
        coin = 0
        wallet = 1000
        last_ath = 0
        fee = 0.0007

        for index, row in ohlc.iterrows():
            # Buy
            if row['ADX'] > 25 and row['SMA3'] > row['SMA6'] and usdt > 0:
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
            if row['ADX'] < 25 and row['SMA3'] < row['SMA6'] and coin > 0:
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
        backtest_result.setInformations(ohlc, dt, wallet, inital_wallet)
        return backtest_result


if __name__ == "__main__":
    ohlc_brochain = mongoDataToDataframe(
        get_by_timestamp_interval({'exchange': 'binance', 'pair': 'ETHUSDT', 'interval': '1h'}, 1514764800,
                                  1577836799))
    adxsma36bot = AdxSma36Bot()
    adxsma36bot.backTest(ohlc_brochain)

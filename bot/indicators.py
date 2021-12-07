import numpy as np
import pandas as pd
import pandas_ta as pda
import ta

from input.binance_exchange.binance_client import BinanceClient


class Indicators:
    def __init__(self):
        pass

    @staticmethod
    def get_chop(high, low, close, window):
        tr1 = pd.DataFrame(high - low).rename(columns={0: 'tr1'})
        tr2 = pd.DataFrame(abs(high - close.shift(1))).rename(columns={0: 'tr2'})
        tr3 = pd.DataFrame(abs(low - close.shift(1))).rename(columns={0: 'tr3'})
        frames = [tr1, tr2, tr3]
        tr = pd.concat(frames, axis=1, join='inner').dropna().max(axis=1)
        atr = tr.rolling(1).mean()
        highh = high.rolling(window).max()
        lowl = low.rolling(window).min()
        ci = 100 * np.log10((atr.rolling(window).sum()) / (highh - lowl)) / np.log10(window)
        return ci

    def launchIndicators(self, ohlc):
        # Simple Moving Average
        ohlc['SMA'] = ta.trend.sma_indicator(ohlc['close'], window=12)

        # Exponential Moving Average
        ohlc['EMA'] = ta.trend.ema_indicator(close=ohlc['close'], window=12)

        # Relative Strength Index (RSI)
        ohlc['RSI'] = ta.momentum.rsi(close=ohlc['close'], window=14)

        # MACD
        MACD = ta.trend.MACD(close=ohlc['close'], window_fast=12, window_slow=26, window_sign=9)
        ohlc['MACD'] = MACD.macd()
        ohlc['MACD_SIGNAL'] = MACD.macd_signal()
        ohlc['MACD_DIFF'] = MACD.macd_diff()  # Histogramme MACD

        # Stochastic RSI
        ohlc['STOCH_RSI'] = ta.momentum.stochrsi(close=ohlc['close'], window=14, smooth1=3, smooth2=3)  # Non moyenné
        ohlc['STOCH_RSI_D'] = ta.momentum.stochrsi_d(close=ohlc['close'], window=14, smooth1=3,
                                                     smooth2=3)  # Orange sur TradingView
        ohlc['STOCH_RSI_K'] = ta.momentum.stochrsi_k(close=ohlc['close'], window=14, smooth1=3,
                                                     smooth2=3)  # Bleu sur TradingView

        # Ichimoku
        ohlc['KIJUN'] = ta.trend.ichimoku_base_line(high=ohlc['high'], low=ohlc['low'], window1=9, window2=26)
        ohlc['TENKAN'] = ta.trend.ichimoku_conversion_line(high=ohlc['high'], low=ohlc['low'], window1=9, window2=26)
        ohlc['SSA'] = ta.trend.ichimoku_a(high=ohlc['high'], low=ohlc['low'], window1=9, window2=26)
        ohlc['SSB'] = ta.trend.ichimoku_b(high=ohlc['high'], low=ohlc['low'], window2=26, window3=52)

        # Bollinger Bands
        BOL_BAND = ta.volatility.BollingerBands(close=ohlc['close'], window=20, window_dev=2)
        ohlc['BOL_H_BAND'] = BOL_BAND.bollinger_hband()  # Bande Supérieur
        ohlc['BOL_L_BAND'] = BOL_BAND.bollinger_lband()  # Bande inférieur
        ohlc['BOL_MAVG_BAND'] = BOL_BAND.bollinger_mavg()  # Bande moyenne

        # ADX
        ADX = ta.trend.ADXIndicator(ohlc['high'], ohlc['low'], ohlc['close'], window=14)
        ohlc['ADX'] = ADX.adx()
        ohlc['ADX_NEG'] = ADX.adx_neg()
        ohlc['ADX_POS'] = ADX.adx_pos()

        # Average True Range (ATR)
        ohlc['ATR'] = ta.volatility.average_true_range(high=ohlc['high'], low=ohlc['low'], close=ohlc['close'],
                                                       window=14)

        # Super Trend
        ST_length = 10
        ST_multiplier = 3.0
        superTrend = pda.supertrend(high=ohlc['high'], low=ohlc['low'], close=ohlc['close'], length=ST_length,
                                    multiplier=ST_multiplier)
        ohlc['SUPER_TREND'] = superTrend[
            'SUPERT_' + str(ST_length) + "_" + str(ST_multiplier)]  # Valeur de la super trend
        ohlc['SUPER_TREND_DIRECTION'] = superTrend[
            'SUPERTd_' + str(ST_length) + "_" + str(ST_multiplier)]  # Retourne 1 si vert et -1 si rouge

        # Awesome Oscillator
        ohlc['AWESOME_OSCILLATOR'] = ta.momentum.awesome_oscillator(high=ohlc['high'], low=ohlc['low'], window1=5,
                                                                    window2=34)

        # Kaufman’s Adaptive Moving Average (KAMA)
        ohlc['KAMA'] = ta.momentum.kama(close=ohlc['close'], window=10, pow1=2, pow2=30)

        # Choppiness index
        ohlc['CHOP'] = self.get_chop(high=ohlc['high'], low=ohlc['low'], close=ohlc['close'], window=14)

        print(ohlc)


if __name__ == "__main__":
    bclient = BinanceClient()
    # 01 janvier 20201
    ohlcs = bclient.get_ohlc('ETHUSDT', '1h', 1609489364)
    # print(ohlcs.size)
    indicator = Indicators()
    indicator.launchIndicators(ohlcs)

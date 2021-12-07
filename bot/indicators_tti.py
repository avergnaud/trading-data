"""
Trading-Technical-Indicators (tti) python library

File name: indicator_example.py
Example code for the trading technical indicators, for the docs.

Accumulation Distribution Line indicator and SCMN.SW.csv data file is used.
"""

from tti.indicators import RelativeVolatilityIndex

from input.binance_exchange.binance_client import BinanceClient


class IndicatorsTti:
    def __init__(self):
        pass

    def launchIndicators(self, ohlc):
        # Read data from csv file. Set the index to the correct column
        # (dates column)
        df = ohlc

        # Create indicator
        adl_indicator = RelativeVolatilityIndex(input_data=df)

        # Get indicator's calculated data
        print('\nTechnical Indicator data:\n', adl_indicator.getTiData())

        # Get indicator's value for a specific date
        print('\nTechnical Indicator value at 2012-09-06:', adl_indicator.getTiValue('2012-09-06'))

        # Get the most recent indicator's value
        print('\nMost recent Technical Indicator value:', adl_indicator.getTiValue())

        # Get signal from indicator
        print('\nTechnical Indicator signal:', adl_indicator.getTiSignal())

        # Show the Graph for the calculated Technical Indicator
        adl_indicator.getTiGraph().show()

        # Execute simulation based on trading signals
        simulation_data, simulation_statistics, simulation_graph = \
            adl_indicator.getTiSimulation(
                close_values=df[['close']], max_exposure=None,
                short_exposure_factor=1.5)
        print('\nSimulation Data:\n', simulation_data)
        print('\nSimulation Statistics:\n', simulation_statistics)

        # Show the Graph for the executed trading signal simulation
        simulation_graph.show()


if __name__ == "__main__":
    bclient = BinanceClient()
    # 01 janvier 20201
    ohlcs = bclient.get_ohlc('ETHUSDT', '1h', 1609489364)
    # print(ohlcs.size)
    indicator = IndicatorsTti()
    indicator.launchIndicators(ohlcs)

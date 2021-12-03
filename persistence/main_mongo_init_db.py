# import the PyMongo MongoClient class
from pymongo import ASCENDING

from mongo_constants import get_exchanges_collection, get_pairs_collection, get_ohlc_collection, \
    get_ohlc_definition_collection, get_intervals_collection, BINANCE, KRAKEN, FTX, GATE, KUCOIN
from input.binance_exchange.binance_client import BinanceClient
from input.kraken_exchange.kraken_client import KrakenClient
from input.ftx_exchange.ftx_client import FtxClient
from input.gate_exchange.gate_client import GateClient
from input.kucoin_exchange.kucoin_client import KucoinClient

#
# idempotent
#


# exchanges
exchanges = get_exchanges_collection()
if exchanges.find_one({'exchange': BINANCE}) is None:
    exchanges.insert_one({'exchange': BINANCE})
if exchanges.find_one({'exchange': KRAKEN}) is None:
    exchanges.insert_one({'exchange': KRAKEN})
if exchanges.find_one({'exchange': FTX}) is None:
    exchanges.insert_one({'exchange': FTX})
if exchanges.find_one({'exchange': GATE}) is None:
    exchanges.insert_one({'exchange': GATE})
if exchanges.find_one({'exchange': KUCOIN}) is None:
    exchanges.insert_one({'exchange': KUCOIN})

# pairs
pairs = get_pairs_collection()
# Binance
binanceClient = BinanceClient()
binance_pairs = binanceClient.get_pairs()
for binance_pair in binance_pairs:
    if pairs.find_one({'exchange': BINANCE, 'pair': binance_pair['symbol']}) is None:
        pairs.insert_one({'exchange': BINANCE, 'pair': binance_pair['symbol']})
# Kraken
krakenClient = KrakenClient()
kraken_pairs = krakenClient.get_pairs()
for kraken_pair in kraken_pairs:
    if pairs.find_one({'exchange': KRAKEN, 'pair': kraken_pair}) is None:
        pairs.insert_one({'exchange': KRAKEN, 'pair': kraken_pair})
# FTX
ftxClient = FtxClient()
ftx_pairs = ftxClient.get_pairs()
for ftx_pair in ftx_pairs:
    if pairs.find_one({'exchange': FTX, 'pair': ftx_pair}) is None:
        pairs.insert_one({'exchange': FTX, 'pair': ftx_pair})
# GATE
gateClient = GateClient()
gate_pairs = gateClient.get_pairs()
for gate_pair in gate_pairs:
    if pairs.find_one({'exchange': GATE, 'pair': gate_pair}) is None:
        pairs.insert_one({'exchange': GATE, 'pair': gate_pair})
# KuCoin
kucoinClient = KucoinClient()
kucoin_pairs = kucoinClient.get_pairs()
for kucoin_pair in kucoin_pairs:
    if pairs.find_one({'exchange': KUCOIN, 'pair': kucoin_pair['symbol']}) is None:
        pairs.insert_one({'exchange': KUCOIN, 'pair': kucoin_pair['symbol']})

# intervals
intervals = get_intervals_collection()
# Binance
binance_intervals = ['1m', '3m', '5m', '15m', '30m', '1h', '2h', '4h', '6h', '8h', '12h', '1d', '3d', '1w', '1M']
for binance_interval in binance_intervals:
    if intervals.find_one({'exchange': BINANCE, 'interval': binance_interval}) is None:
        intervals.insert_one({'exchange': BINANCE, 'interval': binance_interval})
# Kraken
kraken_intervals = [1, 5, 15, 30, 60, 240, 1440, 10080, 21600]
for kraken_interval in kraken_intervals:
    if intervals.find_one({'exchange': KRAKEN, 'interval': kraken_interval}) is None:
        intervals.insert_one({'exchange': KRAKEN, 'interval': kraken_interval})
kraken_intervals = [1, 5, 15, 30, 60, 240, 1440, 10080, 21600]
# FTX
# "resolution: window length in seconds. options: 15, 60, 300, 900, 3600, 14400, 86400,
# or any multiple of 86400 up to 30*86400" (86400 = 1 jour)
trentaine = [i for i in range(1, 30)]
multiples = [number * 86400 for number in trentaine]
ftx_intervals = [15, 60, 300, 900, 3600, 14400]
ftx_intervals.extend(multiples)
for ftx_interval in ftx_intervals:
    if intervals.find_one({'exchange': FTX, 'interval': ftx_interval}) is None:
        intervals.insert_one({'exchange': FTX, 'interval': ftx_interval})
# Gate
gate_intervals = ['10s', '1m', '5m', '15m', '30m', '1h', '4h', '8h', '1d', '1w', '1M']
for gate_interval in gate_intervals:
    if intervals.find_one({'exchange': GATE, 'interval': gate_interval}) is None:
        intervals.insert_one({'exchange': GATE, 'interval': gate_interval})
# Kucoin
kucoin_intervals = ['1min', '3min', '5min', '15min', '30min', '1hour', '2hour', '4hour', '6hour', '8hour', '12hour', '1day', '1week']
for kucoin_interval in kucoin_intervals:
    if intervals.find_one({'exchange': KUCOIN, 'interval': kucoin_interval}) is None:
        intervals.insert_one({'exchange': KUCOIN, 'interval': kucoin_interval})

# ohlc_definition
ohlc_definition = get_ohlc_definition_collection()

ohlc_definition.create_index([("exchange", ASCENDING), ("pair", ASCENDING), ("interval", ASCENDING)],
                             name='ohlc_definition_index', unique=True)

# ohlc
ohlc = get_ohlc_collection()

ohlc.create_index([("exchange", ASCENDING), ("pair", ASCENDING), ("interval", ASCENDING),
                   ("timestamp", ASCENDING)], name='ohlc_index', unique=True)

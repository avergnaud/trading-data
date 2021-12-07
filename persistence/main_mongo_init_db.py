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
std_30m = '30m'
std_1h = '1h'
std_4h = '4h'
std_1d = '1d'
std_1w = '1w'
intervals = get_intervals_collection()
# Binance
binance_disabled_intervals = ['1m', '3m', '5m', '15m']
binance_allowed_intervals = [
    {'interval': '30m', 'interval_std': std_30m},
    {'interval': '1h', 'interval_std': std_1h},
    {'interval': '2h', 'interval_std': None},
    {'interval': '4h', 'interval_std': std_4h},
    {'interval': '6h', 'interval_std': None},
    {'interval': '8h', 'interval_std': None},
    {'interval': '12h', 'interval_std': None},
    {'interval': '1d', 'interval_std': std_1d},
    {'interval': '3d', 'interval_std': None},
    {'interval': '1w', 'interval_std': std_1w}
]
for binance_interval in binance_disabled_intervals:
    if intervals.find_one({'exchange': BINANCE, 'interval': binance_interval}) is None:
        intervals.insert_one(
            {'exchange': BINANCE, 'interval': binance_interval, 'interval_std': None, 'allowed': False})
for binance_interval in binance_allowed_intervals:
    if intervals.find_one({'exchange': BINANCE, 'interval': binance_interval['interval']}) is None:
        intervals.insert_one({'exchange': BINANCE, 'interval': binance_interval['interval'],
                              'interval_std': binance_interval['interval_std'], 'allowed': True})
# Kraken
kraken_disabled_intervals = ['1', '5', '15']
kraken_allowed_intervals = [
    {'interval': '30', 'interval_std': std_30m},
    {'interval': '60', 'interval_std': std_1h},
    {'interval': '240', 'interval_std': std_4h},
    {'interval': '1440', 'interval_std': std_1d},
    {'interval': '10080', 'interval_std': std_1w}
]
for kraken_interval in kraken_disabled_intervals:
    if intervals.find_one({'exchange': KRAKEN, 'interval': kraken_interval}) is None:
        intervals.insert_one({'exchange': KRAKEN, 'interval': kraken_interval, 'interval_std': None, 'allowed': False})
for kraken_interval in kraken_allowed_intervals:
    if intervals.find_one({'exchange': KRAKEN, 'interval': kraken_interval['interval']}) is None:
        intervals.insert_one({'exchange': KRAKEN, 'interval': kraken_interval['interval'],
                              'interval_std': kraken_interval['interval_std'], 'allowed': True})
# FTX
# "resolution: window length in seconds. options: 15, 60, 300, 900, 3600, 14400, 86400,
# or any multiple of 86400 up to 30*86400" (86400 = 1 jour)
ftx_disabled_intervals = ['15', '60', '300', '900']
ftx_allowed_intervals = [
    {'interval': '3600', 'interval_std': std_1h},
    {'interval': '14400', 'interval_std': std_4h},
    {'interval': '86400', 'interval_std': std_1d},
    {'interval': '604800', 'interval_std': std_1w}
]
for ftx_interval in ftx_disabled_intervals:
    if intervals.find_one({'exchange': FTX, 'interval': ftx_interval}) is None:
        intervals.insert_one({'exchange': FTX, 'interval': ftx_interval, 'interval_std': None, 'allowed': False})
for ftx_interval in ftx_allowed_intervals:
    if intervals.find_one({'exchange': FTX, 'interval': ftx_interval['interval']}) is None:
        intervals.insert_one(
            {'exchange': FTX, 'interval': ftx_interval['interval'], 'interval_std': ftx_interval['interval_std'],
             'allowed': True})
# Gate
gate_disabled_intervals = ['10s', '1m', '5m', '15m']
gate_allowed_intervals = [
    {'interval': '30m', 'interval_std': std_30m},
    {'interval': '1h', 'interval_std': std_1h},
    {'interval': '4h', 'interval_std': std_4h},
    {'interval': '8h', 'interval_std': None},
    {'interval': '1d', 'interval_std': std_1d},
    {'interval': '1w', 'interval_std': std_1w},
]
for gate_interval in gate_disabled_intervals:
    if intervals.find_one({'exchange': GATE, 'interval': gate_interval}) is None:
        intervals.insert_one({'exchange': GATE, 'interval': gate_interval, 'interval_std': None, 'allowed': False})
for gate_interval in gate_allowed_intervals:
    if intervals.find_one({'exchange': GATE, 'interval': gate_interval['interval']}) is None:
        intervals.insert_one(
            {'exchange': GATE, 'interval': gate_interval['interval'], 'interval_std': gate_interval['interval_std'],
             'allowed': True})
# Kucoin
kucoin_disabled_intervals = ['1min', '3min', '5min', '15min']
kucoin_allowed_intervals = [
    {'interval': '30min', 'interval_std': std_30m},
    {'interval': '1hour', 'interval_std': std_1h},
    {'interval': '2hour', 'interval_std': None},
    {'interval': '4hour', 'interval_std': std_4h},
    {'interval': '6hour', 'interval_std': None},
    {'interval': '8hour', 'interval_std': None},
    {'interval': '12hour', 'interval_std': None},
    {'interval': '1day', 'interval_std': std_1d},
    {'interval': '1week', 'interval_std': std_1w}
]
for kucoin_interval in kucoin_disabled_intervals:
    if intervals.find_one({'exchange': KUCOIN, 'interval': kucoin_interval}) is None:
        intervals.insert_one({'exchange': KUCOIN, 'interval': kucoin_interval, 'interval_std': None, 'allowed': False})
for kucoin_interval in kucoin_allowed_intervals:
    if intervals.find_one({'exchange': KUCOIN, 'interval': kucoin_interval['interval']}) is None:
        intervals.insert_one({'exchange': KUCOIN, 'interval': kucoin_interval['interval'],
                              'interval_std': kucoin_interval['interval_std'], 'allowed': True})

# ohlc_definition
# ohlc_definition = get_ohlc_definition_collection()

# ohlc_definition.create_index([("exchange", ASCENDING), ("pair", ASCENDING), ("interval", ASCENDING)],
#                              name='ohlc_definition_index', unique=True)

# ohlc
# ohlc = get_ohlc_collection()

# ohlc.create_index([("exchange", ASCENDING), ("pair", ASCENDING), ("interval", ASCENDING),
#                    ("timestamp", ASCENDING)], name='ohlc_index', unique=True)

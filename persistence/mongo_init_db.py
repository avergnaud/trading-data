# import the PyMongo MongoClient class
from pymongo import MongoClient, ASCENDING
from mongo_constants import get_pairs_collection, get_ohlc_collection, get_ohlc_definition_collection
from input.binance_exchange.binance_client import BinanceClient


# pairs
pairs = get_pairs_collection()
pairs.delete_many({})
binanceClient = BinanceClient()
binance_pairs = binanceClient.get_pairs()
for binance_pair in binance_pairs:
    pairs.insert_one({ 'exchange': 'binance', 'pair': binance_pair['symbol']})


# ohlc
ohlc = get_ohlc_collection()

ohlc.create_index([("exchange", ASCENDING), ("pair", ASCENDING), ("interval", ASCENDING),
                   ("timestamp", ASCENDING)], name='ohlc_index', unique=True)


# ohlc_definition
ohlc_definition = get_ohlc_definition_collection()

ohlc_definition.create_index([("exchange", ASCENDING), ("pair", ASCENDING), ("interval", ASCENDING)],
                             name='ohlc_definition_index', unique=True)

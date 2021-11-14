# import the PyMongo MongoClient class
from pymongo import MongoClient, ASCENDING
from mongo_constants import get_ohlc_collection, get_ohlc_definition_collection

ohlc = get_ohlc_collection()

ohlc.create_index([("exchange", ASCENDING), ("pair", ASCENDING), ("interval", ASCENDING),
                   ("timestamp", ASCENDING)], name='ohlc_index', unique=True)

ohlc_definition = get_ohlc_definition_collection()

ohlc_definition.create_index([("exchange", ASCENDING), ("pair", ASCENDING), ("interval", ASCENDING)],
                             name='ohlc_definition_index', unique=True)

# import the PyMongo MongoClient class
from pymongo import MongoClient, ASCENDING
from mongo_constants import get_db, get_ohlc_collection

ohlc = get_ohlc_collection()

# exchange pair interval timestamp o h l c v

ohlc.create_index([("exchange", ASCENDING), ("pair", ASCENDING), ("interval", ASCENDING),
                   ("timestamp", ASCENDING)], name='ohlc_index', unique=True)



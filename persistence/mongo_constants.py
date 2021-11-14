from pymongo import MongoClient

# create a client instance of MongoClient
mongo_client = MongoClient('mongodb://localhost:27017')

# create a new database instance - if not exist
db = mongo_client.trading_data

# create a new collection instance from db - if not exist
ohlc = db.ohlc


def get_db():
    return db


def get_ohlc_collection():
    return ohlc

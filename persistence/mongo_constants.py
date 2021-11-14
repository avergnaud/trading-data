from pymongo import MongoClient

# create a client instance of MongoClient
mongo_client = MongoClient('mongodb://localhost:27017')

# create a new database instance - if not exist
db = mongo_client.trading_data

# la collection ohlc contient les données ohlc. Exemple :
# {
#   "_id" : ObjectId("6191062d60a19c6a6cfaef92"),
#   "exchange" : "binance",
#   "pair" : "ETHEUR",
#   "interval" : "1h",
#   "timestamp" : 1578070800,
#   "open" : 119.59, "
#   high" : 119.59,
#   "low" : 119.25,
#   "close" : 119.25,
#   "volume" : 6.71017
# }
ohlc = db.ohlc

# la collection ohlc_definition contient les définitions de ohlc à alimenter depuis les exchanges. Exemple :
# {
#   "_id" : ObjectId("6191062d60a19c6a6cfaef93"),
#   "exchange" : "binance",
#   "pair" : "ETHEUR",
#   "interval" : "1h"
# }
ohlc_definition = db.ohlc_definition


def get_db():
    return db


def get_ohlc_collection():
    return ohlc


def get_ohlc_definition_collection():
    return ohlc_definition
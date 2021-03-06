from pymongo import MongoClient
import os


mongo_user = os.environ.get('CLOUD_MONGO_USER')
if mongo_user is None:
    raise ValueError('CLOUD_MONGO_USER env variable is not set')

mongo_password = os.environ.get('CLOUD_MONGO_PASSWORD')
if mongo_password is None:
    raise ValueError('CLOUD_MONGO_PASSWORD env variable is not set')

cloud_db_url = "mongodb+srv://" + mongo_user + ":" + mongo_password + "@cluster0.tfnok.mongodb.net/trading_data?retryWrites=true&w=majority"

# create a client instance of MongoClient
# mongo_client = MongoClient('mongodb://localhost:27017')
mongo_client = MongoClient(cloud_db_url)

# create a new database instance - if not exist
db = mongo_client.trading_data

# la collection exchanges contient les exchanges
# {
#   "_id" : ObjectId("6191062d60a19c6a6cfaef91"),
#   "exchange" : "kraken"
# }
exchanges = db.exchanges

# la collection pairs contient les paires de trading (tickers) pour les différents exchanges. Exemple :
# {
#   "_id" : ObjectId("6191062d60a19c6a6cfaef91"),
#   "exchange" : "binance",
#   "pair" : "ETHEUR"
# }
pairs = db.pairs


# la collection intervals contient les intervales de trading propres à chaque exchange. Exemple :
# # {
# #   "_id" : ObjectId("6191062d60a19c6a6cfaef91"),
# #   "exchange" : "kraken",
# #   "pair" : 5
# # }
intervals = db.intervals


# la collection ohlc_definition contient les définitions de ohlc à alimenter depuis les exchanges. Exemple :
# {
#   "_id" : ObjectId("6191062d60a19c6a6cfaef93"),
#   "exchange" : "binance",
#   "pair" : "ETHEUR",
#   "interval" : "1h"
# }
ohlc_definition = db.ohlc_definition

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


BINANCE = 'binance'
KRAKEN = 'kraken'
FTX = 'ftx'
GATE = 'gate'
KUCOIN = 'kucoin'

def get_db():
    return db


def get_exchanges_collection():
    return exchanges


def get_pairs_collection():
    return pairs


def get_intervals_collection():
    return intervals


def get_ohlc_collection():
    return ohlc


def get_ohlc_definition_collection():
    return ohlc_definition

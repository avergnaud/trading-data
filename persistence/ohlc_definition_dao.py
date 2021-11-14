from persistence.mongo_constants import get_ohlc_definition_collection
from bson.objectid import ObjectId

# db: trading_data
# collection: ohlc_definition
# fields: exchange pair interval update_cron
# uniqueness: exchange pair interval

ohlc_definition_collection = get_ohlc_definition_collection()


# CREATE
def insert_or_update(ohlc_definition):
    """inserts or updates a single ohlc_definition document

    Parameters
    ----------
    ohlc_definition : object

    Returns
    -------
    void
    """

    # http://api.mongodb.com/python/current/api/pymongo/operations.html#pymongo.operations.UpdateOne
    ohlc_definition_collection.replace_one(
        {
            "exchange": ohlc_definition["exchange"],
            "pair": ohlc_definition["pair"],
            "interval": ohlc_definition["interval"]
        },
        ohlc_definition,
        upsert=True)


# READ
def find(ohlc_definition):

    # https://pymongo.readthedocs.io/en/stable/api/pymongo/collection.html#pymongo.collection.Collection.find_one
    result = ohlc_definition_collection.find_one(
        {
            "exchange": ohlc_definition["exchange"],
            "pair": ohlc_definition["pair"],
            "interval": ohlc_definition["interval"]
        })
    return result


def findById(id):
    result = ohlc_definition_collection.find_one(
        {
            "_id": ObjectId(id)
        })
    return result


# DELETE
def delete(ohlc_definition):
    """deletes a single ohlc_definition document

    Parameters
    ----------
    ohlc_definition : object

    Returns
    -------
    void
    """

    # https://pymongo.readthedocs.io/en/stable/api/pymongo/collection.html#pymongo.collection.Collection.delete_one
    ohlc_definition_collection.delete_one(
        {
            "exchange": ohlc_definition["exchange"],
            "pair": ohlc_definition["pair"],
            "interval": ohlc_definition["interval"]
        })


if __name__ == "__main__":
    ohlc_definition1 = {'exchange': 'binance','pair': 'ETHEUR', 'interval': '1h', 'update_cron': '*/10 * * * *'}
    insert_or_update(ohlc_definition1)
    ohlc_definition2 = {'exchange': 'binance','pair': 'ETHEUR', 'interval': '1h', 'update_cron': '*/15 * * * *'}
    insert_or_update(ohlc_definition2)
    result1 = find({'exchange': 'binance','pair': 'ETHEUR', 'interval': '1h'})
    print(result1)
    id = str(result1['_id'])
    result2 = findById(id)
    print(result2)
    delete({'exchange': 'binance','pair': 'ETHEUR', 'interval': '1h'})
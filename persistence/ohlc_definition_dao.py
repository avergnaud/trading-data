from persistence.mongo_constants import get_ohlc_definition_collection
from bson.objectid import ObjectId

# db: trading_data
# collection: ohlc_definition
# fields: exchange pair interval update_rate
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
    key = {
            "exchange": ohlc_definition["exchange"],
            "pair": ohlc_definition["pair"],
            "interval": ohlc_definition["interval"]
        }
    ohlc_definition_collection.replace_one(
        key,
        ohlc_definition,
        upsert=True)
    # replace_one does not return the upserted document...
    return find(key)


# READ
def find(ohlc_definition):

    # https://pymongo.readthedocs.io/en/stable/api/pymongo/collection.html#pymongo.collection.Collection.find_one
    result = ohlc_definition_collection.find_one(
        {
            "exchange": ohlc_definition["exchange"],
            "pair": ohlc_definition["pair"],
            "interval": ohlc_definition["interval"]
        })
    result['_id'] = str(result['_id'])
    return result


def get_all():
    # list
    ohlc_definitions = []
    for ohlc_definition in ohlc_definition_collection.find({}):
        ohlc_definition['_id'] = str(ohlc_definition['_id'])
        ohlc_definitions.append(ohlc_definition)
    return ohlc_definitions


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
    ohlc_definition1 = {'exchange': 'kraken','pair': 'BTCUSD', 'interval': 1440, 'update_rate': '5'}
    insert_or_update(ohlc_definition1)
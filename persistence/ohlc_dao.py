from persistence.mongo_constants import get_ohlc_collection
from pymongo import DESCENDING

# db: trading_data
# collection: ohlc
# fields: exchange pair interval timestamp open high low close volume
# uniqueness: exchange pair interval timestamp

ohlc_collection = get_ohlc_collection()


# UPSERT
def insert_or_update(ohlc):
    """inserts or updates a single ohlc document

    Parameters
    ----------
    ohlc : object

    Returns
    -------
    void
    """

    # http://api.mongodb.com/python/current/api/pymongo/operations.html#pymongo.operations.UpdateOne
    ohlc_collection.replace_one(
        {
            "exchange": ohlc["exchange"],
            "pair": ohlc["pair"],
            "interval": ohlc["interval"],
            "timestamp": ohlc["timestamp"]
        },
        ohlc,
        upsert=True)


# CREATE

# READ
def get_last_timestamp(ohlc):
    """retrieves last ohlc sorting by timestamp desc

    Parameters
    ----------
    ohlc : {exchange pair interval}

    Returns
    -------
    void
    """
    result = ohlc_collection.find(
        {'exchange': ohlc['exchange'], 'pair': ohlc['pair'], 'interval': ohlc['interval']}).sort(
        [('timestamp', DESCENDING)]).limit(1)
    for r in result:
        return r


def get_all(ohlc_definition):
    """gets all ohlc fitting definition

    Parameters
    ----------
    ohlc_definition : {exchange pair interval}

    Returns
    -------
    list
    """
    ohlcs = []
    result = ohlc_collection.find(
        {'exchange': ohlc_definition['exchange'], 'pair': ohlc_definition['pair'],
         'interval': ohlc_definition['interval']}).sort(
        [('timestamp', DESCENDING)])
    for ohlc in result:
        ohlc['_id'] = str(ohlc['_id'])
        ohlcs.append(ohlc)
    return ohlcs


def get_last(ohlc_definition, last):
    """gets last ohlc fitting definition

    Parameters
    ----------
    ohlc_definition : {exchange pair interval}
    last : last n ohlcs

    Returns
    -------
    list
    """
    ohlcs = []
    result = ohlc_collection.find(
        {'exchange': ohlc_definition['exchange'], 'pair': ohlc_definition['pair'],
         'interval': ohlc_definition['interval']}) \
        .sort(
        [('timestamp', DESCENDING)]
    ).limit(last)
    for ohlc in result:
        ohlc['_id'] = str(ohlc['_id'])
        ohlcs.append(ohlc)
    return ohlcs


# UPDATE

# DELETE


if __name__ == "__main__":
    ohlc1 = {'exchange': 'FAKE', 'pair': 'ETHEUR', 'interval': '1h', 'timestamp': 1635724800000,
             'open': 1000.1234567,
             'high': 2000.2345678, 'low': 500.3456789, 'close': 1750, 'volume': 10000}
    insert_or_update(ohlc1)
    ohlc2 = {'exchange': 'FAKE', 'pair': 'ETHEUR', 'interval': '1h', 'timestamp': 1635730000000,
             'open': 1002.1234567,
             'high': 2002.2345678, 'low': 504.3456789, 'close': 1751, 'volume': 3000}
    insert_or_update(ohlc2)
    ohlc3 = {'exchange': 'FAKE', 'pair': 'ETHEUR', 'interval': '1h', 'timestamp': 1635730000000, 'open': 1003,
             'high': 2002.2345678, 'low': 504.3456789, 'close': 1751, 'volume': 3000}
    insert_or_update(ohlc3)
    ohlc4 = {'exchange': 'FAKE', 'pair': 'ETHEUR', 'interval': '1h', 'timestamp': 1635800000000,
             'open': 1002.1234567,
             'high': 2002.2345678, 'low': 504.3456789, 'close': 1751, 'volume': 3000}
    insert_or_update(ohlc4)
    ohlc5 = {'exchange': 'FAKE', 'pair': 'ETHEUR', 'interval': '1h', 'timestamp': 1635800000000,
             'open': 1002.1234567,
             'high': 2002.2345678, 'low': 504.3456789, 'close': 1751, 'volume': 4000}
    insert_or_update(ohlc5)
    result = get_last_timestamp({'exchange': 'binance', 'pair': 'ETHEUR', 'interval': '1h'})
    print(result)

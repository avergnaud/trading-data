from persistence.mongo_constants import get_exchanges_collection

# db: trading_data
# collection: exchanges
# fields: exchange

exchanges_collection = get_exchanges_collection()


def get_all():
    # list
    exchanges = []
    for exchange in exchanges_collection.find({}):
        exchange['_id'] = str(exchange['_id'])
        exchanges.append(exchange)

    return exchanges


if __name__ == "__main__":
    result = get_all()
    print(type(result))
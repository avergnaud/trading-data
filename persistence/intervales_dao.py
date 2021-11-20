from persistence.mongo_constants import get_intervals_collection

# db: trading_data
# collection: pairs
# fields: exchange pair

intervales_collection = get_intervals_collection()


def get_all():
    # list
    intervales = []
    for intervale in intervales_collection.find({}):
        intervale['_id'] = str(intervale['_id'])
        intervales.append(intervale)
    return intervales


def get_by_exchange(exchange):
    # list
    intervales = []
    for intervale in intervales_collection.find({'exchange': exchange}):
        intervale['_id'] = str(intervale['_id'])
        intervales.append(intervale)
    return intervales


if __name__ == "__main__":
    result = get_all()
    print(result)
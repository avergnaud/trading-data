from persistence.mongo_constants import get_pairs_collection

# db: trading_data
# collection: pairs
# fields: exchange pair

pairs_collection = get_pairs_collection()


def get_all():
    # list
    pairs = []
    for pair in pairs_collection.find({}):
        pair['_id'] = str(pair['_id'])
        pairs.append(pair)

    return pairs


if __name__ == "__main__":
    result = get_all()
    print(type(result))
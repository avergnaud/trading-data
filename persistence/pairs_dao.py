from persistence.mongo_constants import get_pairs_collection

# db: trading_data
# collection: pairs
# fields: exchange pair

pairs_collection = get_pairs_collection()


def get_all():
    # list
    pairs = []
    for pair in pairs_collection.find({}):
        pairs.append(pair)

    # dict
    results_dict = dict()
    for index, value in enumerate(pairs):
        results_dict[index] = {'exchange': value['exchange'], 'pair': value['pair']}
    return results_dict


if __name__ == "__main__":
    result = get_all()
    print(type(result))
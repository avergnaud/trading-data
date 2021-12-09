from flask import Blueprint, jsonify
from persistence import exchanges_dao, pairs_dao, intervales_dao

# /exchanges
exchanges_page = Blueprint('exchanges_page', __name__, url_prefix='/exchanges')


@exchanges_page.route('/')
def get_exchanges():
    liste = exchanges_dao.get_all()
    return jsonify(liste)


# /:exchange_name/pairs
@exchanges_page.route("/<exchange>/pairs")
def get_exchange_pairs(exchange):
    liste = pairs_dao.get_by_exchange(exchange)
    return jsonify(liste)


# /:exchange_name/intervals
@exchanges_page.route("/<exchange>/intervals")
def get_exchange_intervals(exchange):
    liste = intervales_dao.get_by_exchange(exchange)
    return jsonify(liste)

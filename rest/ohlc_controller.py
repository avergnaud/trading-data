# /ohlcs
from flask import Blueprint, request, jsonify

from cron.feed_cron_manager import FeedCronManager
from persistence import ohlc_definition_dao, ohlc_dao

ohlcs_page = Blueprint('exchanges_page', __name__, url_prefix='/ohlcs')


# /definitions
@ohlcs_page.route("/definitions", methods=['GET', 'POST', 'DELETE'])
def ohlc_definitions():
    if request.method == 'POST':
        result = ohlc_definition_dao.insert_or_update(request.json)
        FeedCronManager.get_instance().add_cron(result)
        return jsonify(result), 200
    elif request.method == 'DELETE':
        ohlc_definition_dao.delete(request.json)
        FeedCronManager.get_instance().remove_cron(request.json)
        return jsonify(request.json), 204
    else:
        liste = ohlc_definition_dao.get_all()
        return jsonify(liste)


# /:exchange_name/:pair/:interval
@ohlcs_page.route("/<exchange>/<pair>/<interval>")
def get_all_ohlc(exchange, pair, interval):
    last = request.args.get('last')
    if last is not None:
        liste = ohlc_dao.get_last({
            'exchange': exchange,
            'pair': pair,
            'interval': interval
        }, int(last))
        return jsonify(liste)
    else:
        liste = ohlc_dao.get_all({
            'exchange': exchange,
            'pair': pair,
            'interval': interval
        })
        return jsonify(liste)

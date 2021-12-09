import base64
import io
import time
from threading import Thread

from flask import Flask, jsonify, request
from flask_cors import CORS

from cron.feed_cron_manager import FeedCronManager
from optimisations.rsi_trix import RsiTrix
from persistence import exchanges_dao, pairs_dao, intervales_dao, ohlc_definition_dao, ohlc_dao
from persistence.ohlc_dao import mongoDataToDataframe, get_by_timestamp
from utils.utils import pyplotToBase64Img

app = Flask(__name__)
CORS(app)


def threaded_function():
    ohlc_defs = ohlc_definition_dao.get_all()
    for ohlc_definition in ohlc_defs:
        # pour répartir les appels aux API, on attend 2 minutes entre chaque add_cron
        time.sleep(60)
        FeedCronManager.get_instance().add_cron(ohlc_definition)


@app.before_first_request
def before_first_request_func():
    print("Relaunching crons on startup !")
    thread = Thread(target=threaded_function)
    thread.start()


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


# /exchanges
@app.route("/exchanges")
def get_exchanges():
    liste = exchanges_dao.get_all()
    return jsonify(liste)


# /exchanges/:exchange_name/pairs
@app.route("/exchanges/<exchange>/pairs")
def get_exchange_pairs(exchange):
    liste = pairs_dao.get_by_exchange(exchange)
    return jsonify(liste)


# /exchanges/:exchange_name/intervals
@app.route("/exchanges/<exchange>/intervals")
def get_exchange_intervals(exchange):
    liste = intervales_dao.get_by_exchange(exchange)
    return jsonify(liste)


# /ohlc_definitions
@app.route("/ohlc_definitions", methods=['GET', 'POST', 'DELETE'])
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


# /exchanges/:exchange_name/intervals
@app.route("/ohlcs/<exchange>/<pair>/<interval>")
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


# /optimisations
@app.route("/optimisations")
def get_optimisations():
    ohlc_brochain = mongoDataToDataframe(
        get_by_timestamp({'exchange': 'binance', 'pair': 'ETHUSDT', 'interval': '1h'}, 1606939487))

    rsitrix = RsiTrix()
    return pyplotToBase64Img(rsitrix.launchOptimization(ohlc_brochain))


if __name__ == "__main__":
    try:
        # app.run(debug=True, host="0.0.0.0")
        # app.run(host="0.0.0.0")
        app.run()
    finally:
        # your "destruction" code
        print('Can you hear me?')

from flask import Flask, jsonify, request
from flask_cors import CORS

from cron.feed_cron_manager import FeedCronManager
from persistence import exchanges_dao, pairs_dao, intervales_dao, ohlc_definition_dao

app = Flask(__name__)
CORS(app)


@app.before_first_request
def before_first_request_func():
    print("Relaunching crons on startup !")
    ohlc_defs = ohlc_definition_dao.get_all()
    for ohlc_definition in ohlc_defs:
        FeedCronManager.get_instance().add_cron(ohlc_definition)


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


if __name__ == "__main__":
    print('RUNNING!')
    try:
        app.run(debug=True, host="0.0.0.0")
    finally:
        # your "destruction" code
        print('Can you hear me?')

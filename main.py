import time
from threading import Thread

from flask import Flask, jsonify, request
from flask_cors import CORS

from cron.feed_cron_manager import FeedCronManager
from persistence import exchanges_dao, pairs_dao, intervales_dao, ohlc_definition_dao, ohlc_dao

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
    return '{"param1":{"0":7.0,"1":8.0,"2":9.0,"3":10.0,"4":11.0,"5":12.0,"6":13.0,"7":14.0,"8":15.0,"9":16.0,' \
           '"10":17.0,"11":18.0,"12":19.0,"13":20.0,"14":21.0,"15":22.0,"16":23.0,"17":24.0,"18":25.0,"19":26.0,' \
           '"20":27.0,"21":28.0,"22":29.0},"result":{"0":3691.8112687692,"1":3868.3757249846,"2":6253.2851437062,' \
           '"3":5657.7754172073,"4":5637.857070928,"5":6245.0480508089,"6":5725.8842419585,"7":4848.1290702486,' \
           '"8":3977.8426991517,"9":3739.2251208418,"10":2964.5740828534,"11":2894.3730376287,"12":2446.8452659876,' \
           '"13":2753.3332577271,"14":3003.657207303,"15":3034.1452648782,"16":2877.6702888441,"17":2751.7471988231,' \
           '"18":2972.9477276795,"19":3011.3484857905,"20":3302.0256391334,"21":3206.4326356285,"22":2469.3394626285}} '

    # bclient = BinanceClient()
    # # 01 janvier 2021
    # ohlcs = bclient.get_ohlc('ETHUSDT', '1h', 1609489364)
    # # print(ohlcs.size)
    # param_opti = ParamOpti()
    # dt = param_opti.launchOptimization(ohlcs)
    # return dt


if __name__ == "__main__":
    try:
        # app.run(debug=True, host="0.0.0.0")
        # app.run(host="0.0.0.0")
        app.run()
    finally:
        # your "destruction" code
        print('Can you hear me?')

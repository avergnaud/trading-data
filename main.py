from flask import Flask, jsonify
from flask_cors import CORS
from persistence import exchanges_dao, pairs_dao, intervales_dao

app = Flask(__name__)
CORS(app)


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


if __name__=="__main__":
    app.run(debug=True)
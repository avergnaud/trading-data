from flask import Flask, jsonify
from flask_cors import CORS
from persistence import pairs_dao

app = Flask(__name__)
CORS(app)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/tmp/binance/pairs")
def get_binance_pairs():
    list = pairs_dao.get_all()
    return jsonify(list)

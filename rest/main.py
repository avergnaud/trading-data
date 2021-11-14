from flask import Flask
from persistence import pairs_dao

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/tmp/binance/pairs")
def get_binance_pairs():
    return pairs_dao.get_all()

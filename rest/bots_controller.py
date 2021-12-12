from flask import Blueprint, jsonify, request
from bot.bot_factory import get_all_bot_names, get_bot_by_name

# /bots
bots_page = Blueprint('bots_page', __name__, url_prefix='/bots')


@bots_page.route('/')
def get_bot_names():
    liste = get_all_bot_names()
    return jsonify(liste)


@bots_page.route("/<bot_name>/backtest")
def backtest(bot_name):
    exchange = request.args.get('exchange')
    pair = request.args.get('pair')
    interval = request.args.get('interval')
    from_timestamp_s = request.args.get('from_timestamp_s')
    to_timestamp_s = request.args.get('to_timestamp_s')
    bot = get_bot_by_name(bot_name)
    return_json = jsonify({})
    if bot is not None:
        ohlc_definition = {
            'exchange': exchange,
            'pair': pair,
            'interval': interval
        }
        result = bot.back_test_between(ohlc_definition, from_timestamp_s, to_timestamp_s)
        return_json = result.toJSON()
    return return_json

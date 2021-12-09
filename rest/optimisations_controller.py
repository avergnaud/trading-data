from flask import Blueprint

from optimisations.rsi_trix import RsiTrix
from persistence.ohlc_dao import mongoDataToDataframe, get_by_timestamp, get_by_timestamp_interval
from utils.utils import pyplotToBase64Img

optimisations_page = Blueprint('optimisations_page', __name__, url_prefix='/optimisations')


# /rsitrix
@optimisations_page.route('/rsitrix')
def get_optimisations_rsi_Trix():
    ohlc_brochain = mongoDataToDataframe(
        get_by_timestamp({'exchange': 'binance', 'pair': 'ETHUSDT', 'interval': '1h'}, 1606939487))

    rsitrix = RsiTrix()
    return pyplotToBase64Img(rsitrix.launchOptimization(ohlc_brochain))


# /rsitrix/:exchange_name/:pair/:interval/:start/:end
@optimisations_page.route('/rsitrix/<exchange>/<pair>/<interval>/<start>/<end>')
def get_optimisations_rsi_Trix(exchange, pair, interval, start, end):
    ohlc_brochain = mongoDataToDataframe(
        get_by_timestamp_interval({'exchange': exchange, 'pair': pair, 'interval': interval}, start, end))

    rsitrix = RsiTrix()
    return pyplotToBase64Img(rsitrix.launchOptimization(ohlc_brochain))

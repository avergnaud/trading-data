from flask import Blueprint, jsonify
from bot.bot_factory import get_all_bot_names

# /bots
bots_page = Blueprint('bots_page', __name__, url_prefix='/bots')


@bots_page.route('/')
def get_bot_names():
    liste = get_all_bot_names()
    return jsonify(liste)
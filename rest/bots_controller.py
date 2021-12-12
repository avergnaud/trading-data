from flask import Blueprint, jsonify
from persistence import exchanges_dao, pairs_dao, intervales_dao

# /bots
bots_page = Blueprint('bots_page', __name__, url_prefix='/bots')


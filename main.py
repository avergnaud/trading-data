import time
from threading import Thread

from flask import Flask
from flask_cors import CORS

from cron.feed_cron_manager import FeedCronManager
from persistence import ohlc_definition_dao
from rest.exchanges_controller import exchanges_page
from rest.ohlc_controller import ohlcs_page
from rest.optimisations_controller import optimisations_page

app = Flask(__name__)
app.register_blueprint(optimisations_page)
app.register_blueprint(exchanges_page)
app.register_blueprint(ohlcs_page)
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


if __name__ == "__main__":
    try:
        # app.run(debug=True, host="0.0.0.0")
        # app.run(host="0.0.0.0")
        app.run()
    finally:
        # your "destruction" code
        print('Can you hear me?')

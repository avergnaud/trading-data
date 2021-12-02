import threading
import time

import schedule

from input.binance_exchange.binance_feed import BinanceFeed


def run_continuously(interval=1):
    """Continuously run, while executing pending jobs at each
    elapsed time interval.
    @return cease_continuous_run: threading. Event which can
    be set to cease continuous run. Please note that it is
    *intended behavior that run_continuously() does not run
    missed jobs*. For example, if you've registered a job that
    should run every minute and you set a continuous run
    interval of one hour then your job won't be run 60 times
    at each interval but only once.
    """
    cease_continuous_run = threading.Event()

    class ScheduleThread(threading.Thread):
        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                schedule.run_pending()
                time.sleep(interval)

    continuous_thread = ScheduleThread()
    continuous_thread.start()
    return cease_continuous_run


class FeedCronManager:
    __instance = None

    def __init__(self):
        if FeedCronManager.__instance is not None:
            raise Exception("Utiliser la méthode get_instance() pour obtenir une instance de FeedCronManager")
        print("constructing FeedCronManager")
        self.feeders = {}
        self.thread_stop_handler = run_continuously()

    def __del__(self):
        # body of destructor
        print("destructing FeedCronManager")
        # Stop the background thread
        self.thread_stop_handler.set()

    @staticmethod
    def get_instance():
        if FeedCronManager.__instance is None:
            print("Création du FeedCronManager")
            FeedCronManager.__instance = FeedCronManager()
        return FeedCronManager.__instance

    def background_job(self, feed):
        print(f"Running {feed.exchange} {feed.pair} {feed.interval}")
        feed.update_data()

    # helper method
    def get_feed_by_ohlc_definition(self, ohlc_definition):
        match ohlc_definition['exchange']:
            case 'binance':
                return BinanceFeed(ohlc_definition['pair'], ohlc_definition['interval'])
            case _:
                # Anything not matched by the above
                print(f"No feeder found for {ohlc_definition}")
                return None

    def add_cron(self, ohlc_definition):
        print(f"add_cron({ohlc_definition})")
        feed = self.get_feed_by_ohlc_definition(ohlc_definition)
        if feed not in self.feeders:
            job = schedule.every(int(ohlc_definition['update_rate'])).minutes.do(self.background_job, feed)
            self.feeders[feed] = job

    def remove_cron(self, ohlc_definition):
        print(f"remove_cron({ohlc_definition})")
        feed = self.get_feed_by_ohlc_definition(ohlc_definition)
        if feed in self.feeders:
            job = self.feeders[feed]
            schedule.cancel_job(job)


if __name__ == "__main__":
    feedCronManager = FeedCronManager()
    feedCronManager.add_cron({
        'exchange': 'binance',
        'pair': 'ETHUSDT',
        'interval': '1h',
        'update_rate': 5
    })
    feedCronManager.add_cron({
        'exchange': 'binance',
        'pair': 'ETHUSDT',
        'interval': '4h',
        'update_rate': 5
    })

    # run_stop_continuously = run_continuously()

    # Do some other things...
    time.sleep(10 * 60)
    feedCronManager.remove_cron({
        'exchange': 'binance',
        'pair': 'ETHUSDT',
        'interval': '1h'
    })

    time.sleep(10 * 60)
    feedCronManager.remove_cron({
        'exchange': 'binance',
        'pair': 'ETHUSDT',
        'interval': '4h'
    })

    # Stop the background thread
    # run_stop_continuously.set()

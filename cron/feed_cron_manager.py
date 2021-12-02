import threading
import time

import schedule

from input.binance_exchange.binance_feed import BinanceFeed


feeders = {}


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


def background_job(feed):
    print(f"Running {feed.exchange} {feed.pair} {feed.interval}")
    feed.update_data()


# helper method
def get_feed_by_ohlc_definition(ohlc_definition):
    match ohlc_definition['exchange']:
        case 'binance':
            return BinanceFeed(ohlc_definition['pair'], ohlc_definition['interval'])
        case _:
            # Anything not matched by the above
            print(f"No feeder found for {ohlc_definition}")
            return None


def add_cron(ohlc_definition):
    print(f"add_cron({ohlc_definition})")
    feed = get_feed_by_ohlc_definition(ohlc_definition)
    if feed not in feeders:
        job = schedule.every(int(ohlc_definition['update_rate'])).minutes.do(background_job, feed)
        feeders[feed] = job


def remove_cron(ohlc_definition):
    print(f"remove_cron({ohlc_definition})")
    feed = get_feed_by_ohlc_definition(ohlc_definition)
    if feed in feeders:
        job = feeders[feed]
        schedule.cancel_job(job)


if __name__ == "__main__":
    add_cron({
        'exchange': 'binance',
        'pair': 'ETHUSDT',
        'interval': '1h',
        'update_rate': 5
    })
    add_cron({
        'exchange': 'binance',
        'pair': 'ETHUSDT',
        'interval': '4h',
        'update_rate': 5
    })

    run_stop_continuously = run_continuously()

    # Do some other things...
    time.sleep(10*60)
    remove_cron({
        'exchange': 'binance',
        'pair': 'ETHUSDT',
        'interval': '1h'
    })

    time.sleep(10*60)
    remove_cron({
        'exchange': 'binance',
        'pair': 'ETHUSDT',
        'interval': '4h'
    })

    # Stop the background thread
    run_stop_continuously.set()

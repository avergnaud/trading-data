import threading
import time

import schedule


# def run_continuously(interval=1):
#     """Continuously run, while executing pending jobs at each
#     elapsed time interval.
#     @return cease_continuous_run: threading. Event which can
#     be set to cease continuous run. Please note that it is
#     *intended behavior that run_continuously() does not run
#     missed jobs*. For example, if you've registered a job that
#     should run every minute and you set a continuous run
#     interval of one hour then your job won't be run 60 times
#     at each interval but only once.
#     """
#     cease_continuous_run = threading.Event()
#
#     class ScheduleThread(threading.Thread):
#         @classmethod
#         def run(cls):
#             while not cease_continuous_run.is_set():
#                 schedule.run_pending()
#                 time.sleep(interval)
#
#     continuous_thread = ScheduleThread()
#     continuous_thread.start()
#     return cease_continuous_run
#
#
# def background_job(exchange):
#     schedule.every().second.do(print('Hello from the background thread : ', exchange))

#
# def test():
#     # Start the background thread
#     stop_run_continuously = run_continuously()
#
#     # Do some other things...
#     time.sleep(10)
#
#     # Stop the background thread
#     stop_run_continuously.set()
#     return 'ok'


def foo_job(exchange):
    print("Hello from the background thread : ", exchange)


# Création du scheduler --> 1 par exchange
def create_cron(exchange):
    schedule.every().second.do(foo_job(exchange='test'))
    # Create a new scheduler
    # schedulerbinance = schedule.Scheduler()
    # Add jobs to the created scheduler
    # scheduler1.run_pending()

# Création de multiple jobs par scheduler
# def add_job(second, minute,hour,week, month)



# schedule.every(10).minutes.do(job)
# schedule.every().hour.do(job)
# schedule.every().day.at("10:30").do(job)

# schedule.every(10).seconds.do(job)


# schedule.every().hour.do(job)
# schedule.every().day.at("10:30").do(job)
# schedule.every(5).to(10).minutes.do(job)
# schedule.every().monday.do(job)
# schedule.every().wednesday.at("13:15").do(job)
# schedule.every().minute.at(":17").do(job)

# def greet(name):
#     print("Hello : ", name)
#
#
# def launch(name):
#     scheduler1 = schedule.Scheduler()
#     scheduler1.every(2).seconds.do(greet, name=name)
#     scheduler1.run_pending()
#
#
# @repeat(every().second, "World")
# @repeat(every().day, "Mars")
# def hello(planet):
#     print("Hello", planet)


if __name__ == "__main__":
    # Start the background thread
    # stop_run_continuously = run_continuously()
    #
    # # Do some other things...
    time.sleep(10)
    #
    # # Stop the background thread
    # stop_run_continuously.set()

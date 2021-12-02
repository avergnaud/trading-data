from crontab import CronTab


class CronManager:
    def __init__(self):
        print('construction CronManager')

    def run(self):
        print("run")

        mem_cron = CronTab(tab="""1 * * * * python test.py""")
        job = mem_cron.new()
        job.run()
        mem_cron.write()


if __name__ == "__main__":
    # cronManager = CronManager()
    # cronManager.run()
    mem_cron = CronTab(tab=""" 1 * * * * python test.py """)
    mem_cron.write("test.txt")
    # tab = CronTab(tabfile='filename.tab')
    # for result in tab.run_scheduler():
    #     print("This was printed to stdout by the process.")

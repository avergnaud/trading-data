from crontab import CronTab


class CronManager:
    def __init__(self):
        print('construction CronManager')

    def run(self):
        print("run")
        command = 'echo hello_world'
        mem_cron = CronTab(tab="""
          * * * * * echo hello_world'
        """)
        mem_cron.write()
        job = mem_cron.new()
        job.enable()


if __name__ == "__main__":
    cronManager = CronManager()
    cronManager.run()
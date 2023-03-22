from apscheduler.schedulers.background import BackgroundScheduler

from mainapp.processing.handle_common_rating import collect_common_rating
from mainapp.processing.handle_sessionfile import remove_sessions_old_files

TIME_1DAY_AGO = 1 * 24 * 60 * 60
TIME_HALFDAY_AGO = 0.5 * 24 * 60 * 60

scheduler = None


def run_apscheduler():
    global scheduler
    scheduler = BackgroundScheduler()
    scheduler.add_job(lambda: remove_sessions_old_files(time_ago=TIME_1DAY_AGO),
                      'cron',
                      hour=3,
                      id="job_remove_sessions",
                      replace_existing=True,
                      )
    scheduler.add_job(collect_common_rating,
                      'cron',
                      second='*/2',
                      id="collect_common_rating",
                      replace_existing=True
                      )

    scheduler.start()


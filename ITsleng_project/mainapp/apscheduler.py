from apscheduler.schedulers.background import BackgroundScheduler
from mainapp.processing.handle_sessionfile import remove_sessions_old_files

TIME_1DAY_AGO = 1 * 24 * 60 * 60

scheduler = None


def run_apscheduler():
    global scheduler
    scheduler = BackgroundScheduler()
    scheduler.add_job(remove_sessions_old_files,
                      'cron',
                      hour=3,
                      id="job_remove_sessions",
                      replace_existing=True,
                      )

    scheduler.start()

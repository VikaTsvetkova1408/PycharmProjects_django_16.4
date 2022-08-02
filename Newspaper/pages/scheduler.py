import logging
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util
from django.conf import settings
from news import jobs as news_jobs

scheduler = BackgroundScheduler(settings.SCHEDULER_CONFIG)


@util.close_old_connections
def delete_old_job_executions(max_age=604800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


def start():
    if settings.DEBUG:
        logging.basicConfig()
        logging.getLogger('apscheduler').setLevel(logging.DEBUG)

    scheduler.add_job(news_jobs.post_weekly_digest,
                      'cron',
                      id='post_weekly_digest',
                      day_of_week='fri',
                      hour='13',
                      minute='30',
                      # minute='*/1',  # for test
                      replace_existing=True)

    scheduler.add_job(delete_old_job_executions,
                      'cron',
                      id='delete_old_job_executions',
                      day_of_week='wed',
                      hour='00',
                      minute='00',
                      replace_existing=True)

    scheduler.start()

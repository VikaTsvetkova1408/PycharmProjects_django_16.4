from celery import shared_task
import time


@shared_task()
def test_task():
    print('mlem')
    time.sleep(10)

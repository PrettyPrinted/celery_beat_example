from celery import shared_task, current_app as celery_app
from redbeat import RedBeatSchedulerEntry
from celery.signals import task_success, task_prerun, task_postrun, task_failure
import random
from .models import Schedule, ScheduleTask
from .extensions import db
from datetime import datetime

@shared_task(bind=True, autoretry_for=(Exception,), retry_kwargs={'max_retries': 3, 'countdown': 5})
def withdrawal(self, payrolltransactnumber, red_beat_name):
    try:
        if not random.choice([0, 1]):
            raise Exception("Something went wrong")
        print(self.request.id,)

        print("WITHDRAWING: ", payrolltransactnumber)

        # the follow is to remove the scheduled task from the redbeat scheduler
        # otherwise it will eventually run again
        try:
            entry = RedBeatSchedulerEntry.from_key("redbeat:" + red_beat_name, app=celery_app)
        except KeyError:
            entry = None

        if entry:
            entry.delete()

        return "DONE"
    except Exception as e:
        raise self.retry(exc=e, countdown=10)
    
@shared_task(bind=True, retry_kwargs={'max_retries': 3, 'countdown': 30})
def call_api(self, schedule_name):
    try:
        raise Exception("Something went wrong")
        print("CALLING API")
    except Exception as e:
        raise self.retry(exc=e)
    return "DONE"

# @task_postrun.connect
# def task_postrun_handler(sender=None, headers=None, body=None, **kwargs):
#     # check to make sure task isn't there already because of retries
#     # how to handle?
#     # st = ScheduleTask(
#     #     schedule_id=Schedule.query.filter_by(schedule_name=kwargs["kwargs"]["schedule_name"]).first().id, # use keyword arguments
#     #     task_id=kwargs["task_id"],
#     # )
#     # db.session.add(st)
#     # db.session.commit()

# @task_failure.connect
# def task_failure_handler(sender=None, headers=None, body=None, **kwargs):
#     print("TASK_FAILURE")
#     print("headers")
#     print(headers)
#     print("body")
#     print(body)
#     print("kwargs")
#     print(kwargs)
#     print("sender")
#     print(sender)

import requests

@shared_task(bind=True)
def get_country_data(self, country, schedule_name):
    print("GETTING COUNTRY DATA")
    r = requests.get(f"https://restcountries.com/v3.1/name/{country}?fullText=true")
    return r.json()

from time import sleep

@shared_task(bind=True)
def send_email(self):
    sleep(10)
    print("SENDING EMAIL")
    return "SENT"
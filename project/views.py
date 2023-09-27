from flask import Blueprint, render_template, request, redirect, url_for
from celery import current_app as celery_app
#from flask import current_app
from celery.result import AsyncResult
from redbeat import RedBeatSchedulerEntry
from redbeat.schedules import rrule
from celery.schedules import crontab, schedule
from uuid import uuid4
from .models import Schedule, Task
from .extensions import db
from datetime import datetime
from .tasks import send_email


main = Blueprint("main", __name__)

@main.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        start_date = request.form.get("start_date")
        start_time = request.form.get("start_time")
        frequency = request.form.get("frequency")
        task = request.form.get("task")
        country = request.form.get("country")
        dt = datetime.strptime(start_date + " " + start_time, "%Y-%m-%d %H:%M")
        # interval = crontab(
        #     year=dt.year,
        #     month_of_year=dt.month, 
        #     day_of_month=dt.day, 
        #     hour=dt.hour, 
        #     minute=dt.minute)

        if frequency == "ONCE":
            interval = rrule(dtstart=dt, count=1, freq="DAILY")
        else:
            interval = rrule(freq="MINUTELY", dtstart=dt)

        schedule_name = str(uuid4())
        entry = RedBeatSchedulerEntry(schedule_name, 'project.tasks.get_country_data', interval, args=[country], kwargs={'schedule_name': schedule_name}, app=celery_app)
        entry.save()
        s = Schedule(
            schedule_name=schedule_name, 
            interval=str(interval),
            args="none"
        )
        db.session.add(s)
        db.session.commit()

        return redirect(url_for("main.index"))
    tasks = Task.query.all()
    return render_template("index.html")

# @main.route("/webhook")
# def webhook():
#     schedule_name = str(uuid4()) # can be whatever you want but should be unique for each scheduled task
#     #interval = crontab(month_of_year=8, day_of_month=23, hour=4, minute=54)
#     interval = schedule(run_every=20)  # seconds
#     # i think I need relative=True
#     entry = RedBeatSchedulerEntry(schedule_name, 'project.tasks.withdrawal', interval, args=[12345, schedule_name], app=celery_app) # options={'task_id':'overwrite-id-2'}
#     entry.save()
#     s = Schedule(
#         schedule_name=schedule_name, 
#         interval=str(interval), 
#         args=str([12345, schedule_name])
#     )
#     db.session.add(s)
#     db.session.commit()

#     return "Withdrawal scheduled"

@main.route("/task")
def task():
    res = AsyncResult('3f43693b-6271-4c28-8a37-f8613c34f99e',app=celery_app)
    print("OUPTUT")
    return res.result


@main.route("/rebuild")
def rebuild():
    schedules = Schedule.query.all() # active = True
    for schedule in schedules:
        #need start time and frequency
        if frequency == "ONCE":
            interval = rrule(dtstart=dt, count=1, freq="DAILY")
        else:
            interval = rrule(freq="MINUTELY", dtstart=dt)
        entry = RedBeatSchedulerEntry(schedule.schedule_name, 'project.tasks.call_api', interval, kwargs={'schedule_name': schedule.schedule_name}, app=celery_app)
        entry.save()

@main.route("/email")
def email():
    #send_email()
    send_email.delay()
    #send_email.apply_async(countdown=10)
    return "Email sent"
from .extensions import db

class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    schedule_name = db.Column(db.String(100), unique=True, nullable=False)
    interval = db.Column(db.String(100), nullable=False)
    args = db.Column(db.String(100), nullable=False)
    enabled = db.Column(db.Boolean, default=True, nullable=False)
    #total_run_count = db.Column(db.Integer, default=0, nullable=False) # derived
    tasks = db.relationship('ScheduleTask', backref='schedule', lazy=True)

class ScheduleTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    schedule_id = db.Column(db.Integer, db.ForeignKey('schedule.id'), nullable=False)
    #task_id = db.Column(db.ForeignKey('celery_taskmeta.task_id'), nullable=False) # celery task id can make a foreign key
    task_id = db.Column(db.String(100), nullable=False) # celery task id can make a foreign key

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
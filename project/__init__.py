from flask import Flask
from .utils import make_celery
from .views import main
from .extensions import db, admin
from .tasks import *
from .models import *
from flask_admin.contrib.sqla import ModelView
from sqlalchemy.ext.automap import automap_base
from markupsafe import Markup

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
    app.config["SECRET_KEY"] = "Oz8Z7Iu&DwoQK)g%*Wit2YpE#-46vy0n"
    app.config["CELERY_CONFIG"] = {
        "broker_url": "redis://redis", 
        "result_backend": "db+sqlite:////app/instance/db.sqlite3", 
        "redbeat_redis_url": "redis://redis",
        "result_extended": True,
        "result_expires": None
    }

    db.init_app(app)
    
    admin.init_app(app)

    app.register_blueprint(main)

    celery = make_celery(app)
    celery.set_default()

    # with app.app_context():
        
    #     Base = automap_base()
    #     Base.prepare(db.engine, reflect=True)
    #     CeleryTaskMeta = Base.classes.celery_taskmeta
    #     CeleryTaskSetMeta = Base.classes.celery_tasksetmeta
    #     class TaskView(ModelView):
    #         can_view_details = True

    #     admin.add_view(TaskView(CeleryTaskMeta, db.session))
    #     admin.add_view(ModelView(CeleryTaskSetMeta, db.session))

    #     db.Model.metadata.reflect(bind=db.engine)

    # from flask import url_for

    # class ScheduleView(ModelView):
    #     can_delete = False
    #     form_columns = ["schedule_name", "tasks"]
    #     column_list = ["schedule_name", "tasks"]

    #     def after_model_change(self, form, model, is_created):
    #         pass

    #     def after_model_delete(self, model):
    #         pass

    # class ScheduleTaskView(ModelView):
    #     can_delete = False
    #     can_edit = False
    #     can_view_details = True
    #     column_list = ["schedule", "task_id"]
    #     column_labels = {"task_id": "Task ID"}

    #     def _task_id_formatter(view, context, model, name):
    #         task = db.session.query(CeleryTaskMeta).filter_by(task_id=model.task_id).first()
    #         return Markup(
    #             u"<a href='%s'>%s</a>" % (
    #                 url_for('celery_taskmeta.details_view', id=task.id),
    #                 model.task_id
    #             ) if model.task_id else u"")

    #     column_formatters = {
    #         'task_id': _task_id_formatter
    #     }


    # admin.add_view(ScheduleView(Schedule, db.session))
    # admin.add_view(ScheduleTaskView(ScheduleTask, db.session))
    

    return app, celery
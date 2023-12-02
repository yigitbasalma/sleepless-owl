import os
import requests
import timeago
import datetime
import dateutil.parser

from flask import Flask
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_authorize import Authorize
from sqlalchemy import and_, desc, asc
from celery import Celery, Task
from abc import ABCMeta
from logging.config import dictConfig

requests.packages.urllib3.disable_warnings()

# Define the WSGI application object
app = Flask(__name__)

# Set project base
project_base = os.path.abspath(os.path.dirname(__file__))

# Configurations
app.config.from_object("w.config.config")

# SQLAlchemy init
db = SQLAlchemy(app)

# Socket init
socketio = SocketIO(app)

# LoginManager init
login_manager = LoginManager(app)

# AuthorizeManager init
authorize = Authorize(app)

# Migration controller init
migrate = Migrate(app, db)

# Logging init
dictConfig(app.config["LOGGING"])


def celery_init_app(_app):
    from .config import celery

    class FlaskTask(Task, metaclass=ABCMeta):
        def __call__(self, *args: object, **kwargs: object):
            with _app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(_app.name, task_cls=FlaskTask)
    celery.broker_url = _app.config["CELERY_BROKER_URL"]
    celery_app.config_from_object(celery)
    celery_app.set_default()
    _app.extensions["celery"] = celery_app
    return celery_app


# Celery init
celery = celery_init_app(app)


class Base(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)

    @classmethod
    def first(cls, conditions, columns=None):
        query = cls.query.filter(
            and_(
                *conditions
            )
        )

        if columns:
            query = query.with_entities(
                *columns
            )

        return query.first()

    @classmethod
    def all(cls, conditions, columns=None, as_dict=False, distinct=None, order_by="desc", order_by_column="created_at",
            limit=None):
        _order_by = dict(desc=desc, asc=asc)

        query = cls.query

        if columns:
            query = query.with_entities(
                *columns
            )

        if distinct:
            query = query.distinct(
                distinct
            )

        query = query.filter(
            and_(
                *conditions
            )
        ).order_by(_order_by[order_by](getattr(cls, order_by_column)))

        if limit:
            query = query.limit(limit)

        if as_dict:
            _data = []
            _columns = columns if columns else cls.__table__.columns

            for i in query.all():
                _dict = {}

                for k in _columns:
                    if k.key in ("created_at",):
                        _dict[k.key] = str(getattr(i, k.key))
                        continue

                    _dict[k.key] = getattr(i, k.key)

                _data.append(_dict)

            return _data

        return query.all()

    @classmethod
    def delete_all(cls, conditions):
        query = cls.query.filter(
            and_(
                *conditions
            )
        )

        query.delete()

    def as_dict(self):
        _dict = {}

        for k in self.__table__.columns:
            if k.key in ("password", "last_password_change"):
                continue

            if k.key in ("created_at", "cert_valid_until", "maintenance_since", "maintenance_until"):
                _dict[k.key] = str(getattr(self, k.key))
                continue

            _dict[k.key] = getattr(self, k.key)

        return _dict


# Constraint values
@app.context_processor
def constraints():
    return {
        **app.config["PAGE_CONFIG"]
    }


# Models
from .apps.auth.models import Users


@app.template_filter('timeago')
def fromnow(date):
    try:
        _date = date
        if isinstance(date, str):
            _date = dateutil.parser.parse(date)
        return timeago.format(_date)
    except (dateutil.parser._parser.ParserError, timeago.excepts.ParameterUnvalid):
        return date


@app.template_filter('get_user_info')
def get_user_info(obj):
    user = Users.first(conditions=[Users.id == obj])
    return f"{user.first_name} {user.last_name}"


@app.template_filter('task_names')
def get_task_names(obj):
    return ", ".join([i.name for i in obj])


@app.template_filter('get_for_js')
def get_for_js(obj):
    return [i.id for i in obj]


@app.template_filter('get_status_button')
def get_status_button(obj):
    return dict(unknown="btn-secondary", up="btn-success", down="btn-danger", partial="btn-warning").get(obj)


@app.template_filter('get_cert_button')
def get_status_button(obj):
    return dict(unknown="btn-secondary", valid="btn-success", expired="btn-danger").get(obj)

# Pages
from .apps.index.routes import index
from .apps.auth.routes import auth
from .apps.dashboard.routes import dashboard
from .apps.agents.routes import agents
from .apps.users.routes import users
from .apps.notification.routes import notification
from .apps.tasks.routes import tasks
from .apps.maintenance.routes import maintenance


@login_manager.user_loader
def load_user(user_id):
    return Users().first([Users.id == user_id])


# Create page
app.register_blueprint(index)
app.register_blueprint(auth)
app.register_blueprint(dashboard)
app.register_blueprint(agents)
app.register_blueprint(users)
app.register_blueprint(notification)
app.register_blueprint(tasks)
app.register_blueprint(maintenance)

# Import API resource
from .api import api_router

app.register_blueprint(api_router)

with app.app_context():
    db.create_all()

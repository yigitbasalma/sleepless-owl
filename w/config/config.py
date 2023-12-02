from wtforms import validators

from w.helpers.x_tools import datetime_pattern

# Statement for enabling the development environment
DEBUG = True

# Running env
ENV = "development"

# Session manager config
SESSION_TYPE = "redis"

# Celery
CELERY_BROKER_URL='redis://127.0.0.1:6379/5',
CELERY_RESULT_BACKEND='redis://127.0.0.1:6379/6'

# SQLAlchemy Config
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:Qazxsw123*@127.0.0.1:3306/sleepless_owl"
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ENGINE_OPTIONS = {
    "pool_size": 10,
    "pool_recycle": 120,
    "pool_pre_ping": True
}

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2

# Secret key for signing cookies
SECRET_KEY = "^740*4X7B4F.0gn0c21f69~_s|1vAM_*!K_::-*I8-9|i7|*S4W2^7|z*H24.tP"

# General config
BASE_URL = "owl.warewave.tech"

# Logging config
LOGGING = {
    "version": 1,
    "formatters": {
        "default": {
            "format": "[%(asctime)s] [%(levelname)s | %(funcName)s] %(message)s",
            "datefmt": "%B %d, %Y %H:%M:%S %Z",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
        }
    },
    "root": {"level": "INFO", "handlers": ["console"]},
}

# Application config
PAGE_CONFIG = dict(
    PAGE_TITLE="Multi Location Uptime Watcher",
    BRAND_NAME="Warewave Technology",
    COPYRIGHTS=datetime_pattern("copyrights")
)

# API config
API_VERSION = "/api/v1"

# Notification config
NOTIFICATION_PROVIDERS = dict(
    slack=dict(
        logo="/static/image/providers/slack.png",
        config_required=True,
        config_fields=dict(api_key=(str,))
    ),
    teams=dict(
        logo="/static/image/providers/teams.png",
        config_required=True,
        config_fields=dict(webhook_url=(str,))
    )
)

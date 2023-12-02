from datetime import datetime

from w import db, celery
from w.apps.notification.models import AlertHash


@celery.task
def track():
    for item in AlertHash.all(conditions=[]):
        try:
            if datetime.now() > item.expire:
                db.session.delete(item)
                db.session.commit()
        except Exception as e:
            print(e)

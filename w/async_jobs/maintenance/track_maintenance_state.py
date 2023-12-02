from datetime import datetime

from w import db, celery
from w.apps.maintenance.models import MaintenanceRules


@celery.task
def track():
    for maintenance in MaintenanceRules.all(conditions=[MaintenanceRules.completed == "False"]):
        if datetime.now() > maintenance.until:
            maintenance.completed = "True"
            db.session.commit()

            for task in maintenance.tasks:
                task.maintenance_active = "False"
                task.maintenance_since = None
                task.maintenance_until = None
                db.session.commit()

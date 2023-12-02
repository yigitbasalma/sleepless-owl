from datetime import datetime

from w import db, celery
from w.helpers.x_tools import convert_string_to_bool
from w.apps.maintenance.models import MaintenanceRules


@celery.task
def track():
    # Check regular maintenance
    for maintenance in MaintenanceRules.all(conditions=[MaintenanceRules.type == "regular",
                                                        MaintenanceRules.completed == "False"]):
        if maintenance.since < datetime.now() < maintenance.until:
            for task in maintenance.tasks:
                if not convert_string_to_bool(task.maintenance_active):
                    task.maintenance_active = "True"
                    task.maintenance_since = maintenance.since
                    task.maintenance_until = maintenance.until
                    db.session.commit()

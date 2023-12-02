from sqlalchemy.exc import IntegrityError
from datetime import datetime

from w import db
from w.helpers.x_tools import response_create, convert_string_to_bool
from w.apps.tasks.models import Tasks

from .models import MaintenanceRules


def create_new_regular_maintenance(form):
    name = form.name.data.title()
    since = datetime.strptime(form.since.data, "%d/%m/%Y %H:%M:%S")
    until = datetime.strptime(form.until.data, "%d/%m/%Y %H:%M:%S")
    tasks = [Tasks.first(conditions=[Tasks.id == i]) for i in form.tasks.data]

    if since > until:
        return response_create(
            data=dict(
                status="error",
                message="The start date cannot be greater than the end date!"
            )
        )
    elif datetime.now() > since:
        return response_create(
            data=dict(
                status="error",
                message="The start date cannot be less than today!"
            )
        )

    for task in tasks:
        if MaintenanceRules.first(conditions=[MaintenanceRules.tasks.any(id=task.id),
                                              MaintenanceRules.completed != "True"]):
            return response_create(
                data=dict(
                    status="error",
                    message=f"The '{task.name}' task has an active maintenance. "
                            f"You cannot define second one until completed first."
                )
            )

    # Create maintenance
    try:
        maintenance = MaintenanceRules(
            name=name,
            type="regular",
            since=since,
            until=until,
            tasks=tasks
        )
        db.session.add(maintenance)
    except IntegrityError:
        db.session.rollback()
        return response_create(
            data=dict(
                status="error",
                message=f"Maintenance already exists."
            )
        )

    db.session.commit()

    return response_create(
        data=dict(
            status="success",
            message="Maintenance is created.",
            refresh=True
        )
    )


def delete_maintenance_func(maintenance_id):
    maintenance = MaintenanceRules.first(conditions=[MaintenanceRules.id == maintenance_id,
                                                     MaintenanceRules.completed == "False"])

    if maintenance:
        for task in maintenance.tasks:
            if convert_string_to_bool(task.maintenance_active):
                task.maintenance_active = "False"
                task.maintenance_since = None
                task.maintenance_until = None
                db.session.commit()

        db.session.delete(maintenance)
        db.session.commit()

    return response_create(
        data=dict(
            status="success",
            message="Maintenance removed.",
            refresh=True
        )
    )

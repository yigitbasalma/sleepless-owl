from flask import Blueprint, render_template, jsonify, request
from flask_login import login_required

from w import authorize
from w.apps.tasks.models import Tasks

from .models import MaintenanceRules
from .forms import RegularMaintenanceForm
from .controllers import create_new_regular_maintenance, delete_maintenance_func

maintenance = Blueprint("maintenance", __name__, url_prefix="/maintenance")


@maintenance.route("/", methods=["GET"])
@login_required
@authorize.has_role("admin")
def index():
    regular_maintenance_form = RegularMaintenanceForm()
    regular_maintenance_form.tasks.choices.extend(
        [
            (i.id, i.name)
            for i in Tasks.all([])
        ]
    )

    return render_template(
        "maintenance/maintenance.html",
        regulars=MaintenanceRules.all(conditions=[MaintenanceRules.type == "regular"]),
        crons=MaintenanceRules.all(conditions=[MaintenanceRules.type == "cron"]),
        regular_maintenance_form=regular_maintenance_form
    )


@maintenance.route("/regular", methods=["POST"])
@login_required
@authorize.has_role("admin")
def create_regular_maintenance():
    regular_maintenance_form = RegularMaintenanceForm()
    regular_maintenance_form.tasks.choices.extend(
        [
            (i.id, i.name)
            for i in Tasks.all([])
        ]
    )

    if regular_maintenance_form.validate_on_submit():
        return create_new_regular_maintenance(form=regular_maintenance_form)

    _errors = []
    for fieldName, errorMessages in regular_maintenance_form.errors.items():
        for err in errorMessages:
            _errors.append(f"{regular_maintenance_form[fieldName].label.text}: {err}")

    return jsonify({
        "status": "error",
        "message": f"{_errors[0]}"
    })


@maintenance.route("/<int:maintenance_id>/delete", methods=["GET"])
@login_required
@authorize.has_role("admin")
def delete_maintenance(maintenance_id):
    return delete_maintenance_func(maintenance_id=maintenance_id)

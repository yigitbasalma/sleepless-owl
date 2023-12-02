from flask import Blueprint, render_template
from flask_login import login_required

from w.apps.agents.models import Agents
from w.apps.tasks.models import Tasks
from w.apps.tasks.forms import TaskForm, TCPTaskForm

dashboard = Blueprint("dashboard", __name__, url_prefix="/dashboard")


@dashboard.route("/", methods=["GET"])
@login_required
def index():
    task_form = TaskForm()
    task_form.agents.choices.extend(
        [
            (i.id, i.name)
            for i in Agents.all([])
        ]
    )
    tcp_task_form = TCPTaskForm()
    tcp_task_form.agents.choices.extend(
        [
            (i.id, i.name)
            for i in Agents.all([])
        ]
    )

    return render_template(
        "dashboard/dashboard.html",
        task_form=task_form,
        tcp_task_form=tcp_task_form,
        tasks=Tasks.all(conditions=[])
    )

from datetime import datetime, timedelta

from flask import Blueprint, jsonify
from flask_login import login_required
from flask_socketio import emit

from w import db, authorize, socketio
from w.helpers.x_tools import convert_string_to_bool
from w.apps.agents.models import Agents, AgentTaskStates, AgentTaskLogs

from .models import Tasks
from .forms import TaskForm, TCPTaskForm
from .controllers import (
    create_new_http_task_func,
    create_new_tcp_task_func,
    delete_task_func,
    update_http_task_func,
    update_tcp_task_func
)

tasks = Blueprint("tasks", __name__, url_prefix="/tasks")


@socketio.on('Task States')
def task_summaries():
    while 1:
        summaries = []
        for _task in Tasks.all(conditions=[]):
            task_states = AgentTaskStates.all(conditions=[
                AgentTaskStates.task_id == _task.id,
                AgentTaskStates.state == "success",
                AgentTaskStates.created_at.between(datetime.now() - timedelta(seconds=_task.period), datetime.now())
            ], distinct=AgentTaskStates.agent_id)
            task_state_percent = (len(task_states) / len(_task.agents)) * 100 if task_states else 0
            _summary = dict(id=_task.id, status=_task.status, cert_valid=_task.cert_valid,
                            cert_valid_until=f"{_task.cert_valid_until}", task_state_percent=task_state_percent,
                            in_maintenance=convert_string_to_bool(_task.maintenance_active),
                            maintenance_since=f"{_task.maintenance_since}",
                            maintenance_until=f"{_task.maintenance_until}")
            summaries.append(_summary)
        emit("summaries", summaries)
        db.session.commit()
        socketio.sleep(10)


@tasks.route("/<int:task_id>", methods=["GET"])
@login_required
def task(task_id):
    _task = Tasks.first(conditions=[Tasks.id == task_id])

    return jsonify({
        "task": _task.as_dict(),
        "agents": [i.id for i in _task.agents]
    })


@tasks.route("/<int:task_id>/logs", methods=["GET"])
@login_required
def task_logs(task_id):
    _task = Tasks.first(conditions=[Tasks.id == task_id])

    return jsonify({
        "name": _task.name,
        "logs": [
            dict(created_at=i.created_at, agent=i.agent.name, log=i.log)
            for i in AgentTaskLogs.all(conditions=[AgentTaskLogs.task_id == _task.id], order_by="asc")
        ]
    })


@tasks.route("/http/<int:task_id>/update", methods=["POST"])
@login_required
@authorize.has_role("admin")
def update_http_task(task_id):
    _task = Tasks.first(conditions=[Tasks.id == task_id])

    task_form = TaskForm()
    task_form.agents.choices.extend(
        [
            (i.id, i.name)
            for i in Agents.all([])
        ]
    )

    if task_form.validate_on_submit():
        return update_http_task_func(form=task_form, task_id=task_id)

    _errors = []
    for fieldName, errorMessages in task_form.errors.items():
        for err in errorMessages:
            _errors.append(f"{task_form[fieldName].label.text}: {err}")

    return jsonify({
        "status": "error",
        "message": f"{_errors[0]}"
    })


@tasks.route("/create/http", methods=["POST"])
@login_required
@authorize.has_role("admin")
def create_new_http_task():
    task_form = TaskForm()
    task_form.agents.choices.extend(
        [
            (i.id, i.name)
            for i in Agents.all([])
        ]
    )

    if task_form.validate_on_submit():
        return create_new_http_task_func(form=task_form)

    _errors = []
    for fieldName, errorMessages in task_form.errors.items():
        for err in errorMessages:
            _errors.append(f"{task_form[fieldName].label.text}: {err}")

    return jsonify({
        "status": "error",
        "message": f"{_errors[0]}"
    })


@tasks.route("/create/tcp", methods=["POST"])
@login_required
@authorize.has_role("admin")
def create_new_tcp_task():
    tcp_task_form = TCPTaskForm()
    tcp_task_form.agents.choices.extend(
        [
            (i.id, i.name)
            for i in Agents.all([])
        ]
    )

    if tcp_task_form.validate_on_submit():
        return create_new_tcp_task_func(form=tcp_task_form)

    _errors = []
    for fieldName, errorMessages in tcp_task_form.errors.items():
        for err in errorMessages:
            _errors.append(f"{tcp_task_form[fieldName].label.text}: {err}")

    return jsonify({
        "status": "error",
        "message": f"{_errors[0]}"
    })


@tasks.route("/tcp/<int:task_id>/update", methods=["POST"])
@login_required
@authorize.has_role("admin")
def update_tcp_task(task_id):
    _task = Tasks.first(conditions=[Tasks.id == task_id])

    tcp_task_form = TCPTaskForm()
    tcp_task_form.agents.choices.extend(
        [
            (i.id, i.name)
            for i in Agents.all([])
        ]
    )

    if tcp_task_form.validate_on_submit():
        return update_tcp_task_func(form=tcp_task_form, task_id=task_id)

    _errors = []
    for fieldName, errorMessages in tcp_task_form.errors.items():
        for err in errorMessages:
            _errors.append(f"{tcp_task_form[fieldName].label.text}: {err}")

    return jsonify({
        "status": "error",
        "message": f"{_errors[0]}"
    })


@tasks.route("/delete/<int:task_id>", methods=["GET"])
@login_required
@authorize.has_role("admin")
def delete_task(task_id):
    return delete_task_func(task_id=task_id)

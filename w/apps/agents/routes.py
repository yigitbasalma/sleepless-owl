from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required

from w import authorize

from .forms import AgentForm
from .controllers import create_new_agent, agent_metric_for_chart_func, widget_metric_for_chart_func
from .models import Agents

agents = Blueprint("agents", __name__, url_prefix="/agents")


@agents.route("/", methods=["GET", "POST"])
@login_required
@authorize.has_role("admin")
def index():
    agent_form = AgentForm()

    if request.method in ("POST", ):
        if agent_form.validate_on_submit():
            return create_new_agent(form=agent_form)

        _errors = []
        for fieldName, errorMessages in agent_form.errors.items():
            for err in errorMessages:
                _errors.append(f"{agent_form[fieldName].label.text}: {err}")

        return jsonify({
            "status": "error",
            "message": f"{_errors[0]}"
        })

    return render_template(
        "agents/agents.html",
        agent_form=agent_form,
        agents=Agents.all(conditions=[])
    )


@agents.route("/metrics/for-charts/<int:task_id>", methods=["GET"])
@login_required
def agent_metrics_for_chart(task_id):
    return agent_metric_for_chart_func(task_id=task_id, period=request.args.get("period", "30min"))


@agents.route("/metrics/for-widget/<int:task_id>", methods=["GET"])
@login_required
def widget_metrics_for_chart(task_id):
    return widget_metric_for_chart_func(task_id=task_id)

import random
import pandas

from datetime import timedelta, datetime
from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError

from w import db
from w.helpers.x_tools import response_create
from w.apps.tasks.models import Tasks

from .models import Agents, AgentMetrics


def create_new_agent(form):
    name = form.name.data.title()
    location = form.location.data.title()

    # Create agent
    try:
        agent = Agents(
            name=name,
            location=location,
            color="".join(["#"+''.join([random.choice('0123456789ABCDEF') for _ in range(6)]) for _ in range(1)])
        )
        db.session.add(agent)
    except IntegrityError:
        db.session.rollback()
        return response_create(
            data=dict(
                status="error",
                message=f"Something went wrong."
            )
        )

    db.session.commit()

    return response_create(
        data=dict(
            status="success",
            message="Agent is created.",
            refresh=True
        )
    )


def agent_metric_for_chart_func(task_id, period):
    available_periods = {
        "30min": dict(minutes=30),
        "1hour": dict(minutes=60),
        "3hour": dict(hours=3),
        "6hour": dict(hours=6),
        "24hour": dict(hours=24),
        "1week": dict(weeks=1),
        "1month": dict(weeks=4),
        "1year": dict(days=365)
    }
    end_date = datetime.now()
    metrics = AgentMetrics.all(conditions=[
        AgentMetrics.task_id == task_id,
        AgentMetrics.created_at.between(end_date - timedelta(**available_periods.get(period)), end_date)
    ])
    max_value = AgentMetrics.query.with_entities(db.func.max(AgentMetrics.value)).filter(
        and_(
            AgentMetrics.task_id == task_id,
            AgentMetrics.created_at.between(end_date - timedelta(**available_periods.get(period)), end_date)
        )
    ).first()
    _tmp = dict()
    data = dict(labels=[], datasets=[], max=max_value[0])

    if metrics:
        for metric in metrics:
            if _tmp.get(metric.agents.name):
                _tmp[metric.agents.name]["value"].append(dict(y=metric.value, x=metric.created_at))
                continue

            _tmp[metric.agents.name] = dict(value=[dict(y=metric.value, x=metric.created_at)], color=metric.agents.color)

        for k, v in _tmp.items():
            data["datasets"].append({
                "data": v["value"],
                "borderColor": v["color"],
                "backgroundColor": v["color"],
                "label": k
            })

    data["labels"] = [
        date for date in pandas.date_range(end_date - timedelta(**available_periods.get(period)), end_date,
                                           freq=timedelta(minutes=1))
    ]

    return response_create(
        data=dict(
            status="success",
            data=data
        )
    )


def widget_metric_for_chart_func(task_id):
    end_date = datetime.now()
    task = Tasks.first(conditions=[Tasks.id == task_id])
    metrics_24_hour = AgentMetrics.all(conditions=[
        AgentMetrics.task_id == task_id,
        AgentMetrics.agents.has(Agents.id.in_([i.id for i in task.agents])),
        AgentMetrics.created_at.between(end_date - timedelta(seconds=87030), end_date),
        AgentMetrics.value > 0
    ])
    metrics_30_day = AgentMetrics.all(conditions=[
        AgentMetrics.task_id == task_id,
        AgentMetrics.agents.has(Agents.id.in_([i.id for i in task.agents])),
        AgentMetrics.created_at.between(end_date - timedelta(seconds=87030 * 30), end_date),
        AgentMetrics.value > 0
    ])
    avg_30_min = AgentMetrics.first(conditions=[
        AgentMetrics.task_id == task_id,
        AgentMetrics.created_at.between(end_date - timedelta(minutes=30), end_date),
        AgentMetrics.value > 0
    ], columns=[db.func.avg(AgentMetrics.value)])
    avg_24_hours = AgentMetrics.first(conditions=[
        AgentMetrics.task_id == task_id,
        AgentMetrics.created_at.between(end_date - timedelta(hours=24), end_date),
        AgentMetrics.value > 0
    ], columns=[db.func.avg(AgentMetrics.value)])

    # Clac data points for uptime
    uptime_24_hours_dp = 86400 / task.period * len(task.agents)
    uptime_30_day_dp = 86400 * 30 / task.period * len(task.agents)

    return response_create(
        data=dict(
            status="success",
            data=dict(avg_30_min=f"{avg_30_min[0]:.2f}" if avg_30_min[0] else 0,
                      avg_24_hour=f"{avg_24_hours[0]:.2f}" if avg_24_hours[0] else 0,
                      uptime_24_hours=f"{(len(metrics_24_hour) / uptime_24_hours_dp) * 100:.3f}",
                      uptime_30_day=f"{(len(metrics_30_day) / uptime_30_day_dp) * 100:.3f}")
        )
    )

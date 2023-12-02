import json
import re

from sqlalchemy.exc import IntegrityError

from w import db
from w.helpers.x_tools import response_create
from w.apps.agents.models import Agents

from .models import Tasks


def create_new_http_task_func(form):
    name = form.name.data.title()
    task_type = form.task_type.data
    url = form.url.data
    username = form.username.data
    password = form.password.data
    headers = form.headers.data
    data = form.data.data
    return_codes = form.return_codes.data
    period = form.period.data
    agents = Agents.all(conditions=[Agents.id.in_(form.agents.data)])

    # Check headers and data
    if data:
        try:
            json.loads(data)
        except json.decoder.JSONDecodeError:
            return response_create(
                data=dict(
                    status="error",
                    message="'Data' must be a valid json string."
                )
            )

    if headers:
        try:
            json.loads(headers)
        except json.decoder.JSONDecodeError:
            return response_create(
                data=dict(
                    status="error",
                    message="'Headers' must be a valid json string."
                )
            )

    if period < 20:
        return response_create(
            data=dict(
                status="error",
                message="Minimum period value is should be 20 seconds."
            )
        )

    if return_codes:
        for code in return_codes.split(","):
            if not re.search("[2-5][0-9][0-9]", code):
                return response_create(
                    data=dict(
                        status="error",
                        message="'Return Code' must be a valid http return code."
                    )
                )
    else:
        return_codes = "200"

    # Create task
    try:
        task = Tasks(
            name=name,
            type=task_type,
            url=url,
            username=username,
            password=password,
            headers=headers,
            data=data,
            return_codes=return_codes,
            agents=agents,
            period=period
        )
        db.session.add(task)
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
            message="Task created.",
            refresh=True
        )
    )


def create_new_tcp_task_func(form):
    name = form.name.data.title()
    task_type = form.task_type.data
    ip_address = form.ip_address.data
    port = form.port.data
    period = form.period.data
    agents = Agents.all(conditions=[Agents.id.in_(form.agents.data)])

    # Create task
    try:
        task = Tasks(
            name=name,
            type=task_type,
            ip_address=ip_address,
            port=port,
            agents=agents,
            period=period
        )
        db.session.add(task)
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
            message="Task created.",
            refresh=True
        )
    )


def update_http_task_func(form, task_id):
    task = Tasks.first(conditions=[Tasks.id == task_id])

    if task:
        name = form.name.data.title()
        url = form.url.data
        username = form.username.data
        password = form.password.data
        headers = form.headers.data
        data = form.data.data
        return_codes = form.return_codes.data
        period = form.period.data
        agents = Agents.all(conditions=[Agents.id.in_(form.agents.data)])

        fields = dict(name=name, url=url, username=username, password=password, headers=headers, data=data,
                      period=period, return_codes=return_codes, agents=agents)

        for field, value in fields.items():
            if getattr(task, field) != value:
                setattr(task, field, value)

        db.session.commit()

    return response_create(
        data=dict(
            status="success",
            message="Task updated.",
            refresh=True
        )
    )


def update_tcp_task_func(form, task_id):
    task = Tasks.first(conditions=[Tasks.id == task_id])

    if task:
        name = form.name.data.title()
        ip_address = form.ip_address.data
        port = form.port.data
        period = form.period.data
        agents = Agents.all(conditions=[Agents.id.in_(form.agents.data)])

        fields = dict(name=name, ip_address=ip_address, port=port, period=period, agents=agents)

        for field, value in fields.items():
            if getattr(task, field) != value:
                setattr(task, field, value)

        db.session.commit()

    return response_create(
        data=dict(
            status="success",
            message="Task updated.",
            refresh=True
        )
    )


def delete_task_func(task_id):
    task = Tasks.first(conditions=[Tasks.id == task_id])

    if task:
        db.session.delete(task)
        db.session.commit()

    return response_create(
        data=dict(
            status="success",
            message="Task removed.",
            refresh=True
        )
    )

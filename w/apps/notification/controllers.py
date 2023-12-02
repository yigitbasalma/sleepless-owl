import json

from sqlalchemy.exc import IntegrityError

from w import app, db
from w.helpers.x_tools import response_create
from w.apps.tasks.models import Tasks

from .models import Providers, Rules


def create_new_provider(form):
    name = form.name.data.title()
    provider_name = form.provider_name.data.lower()
    config = form.config.data
    _config = json.loads(config)

    for field, field_types in app.config["NOTIFICATION_PROVIDERS"][provider_name]["config_fields"].items():
        _field = _config.get(field)
        if not _field:
            return response_create(
                data=dict(
                    status="error",
                    message=f"'{field}' is required for this provider."
                )
            )
        if not isinstance(_field, field_types):
            return response_create(
                data=dict(
                    status="error",
                    message=f"'{field}' type is must be one of {field_types}."
                )
            )

    # Create notification
    try:
        provider = Providers(
            name=name,
            provider_name=provider_name,
            provider_image=app.config["NOTIFICATION_PROVIDERS"][provider_name]["logo"],
            config=config
        )
        db.session.add(provider)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return response_create(
            data=dict(
                status="error",
                message=f"Something went wrong."
            )
        )

    return response_create(
        data=dict(
            status="success",
            message="Provider is created.",
            refresh=True
        )
    )


def create_new_rule(form):
    name = form.name.data.title()
    provider = Providers.first(conditions=[Providers.id == form.provider_id.data])
    tasks = [Tasks.first(conditions=[Tasks.id == i]) for i in form.tasks.data]
    config = form.config.data
    _config = json.loads(config)

    if provider.provider_name in ("slack", ):
        if not _config.get("channel"):
            return response_create(
                data=dict(
                    status="error",
                    message=f"When using Slack provider, the 'channel' config key must be user."
                )
            )

    if not _config.get("task-down-alerts"):
        _config["task-down-alerts"] = True

    if not _config.get("agent-down-alerts"):
        _config["agent-down-alerts"] = True

    if not _config.get("certificate-expire-alerts"):
        _config["certificate-expire-alerts"] = True
        _config["certificate-expire-alerts-start-before"] = "1-Month"
        _config["certificate-expire-alerts-send-ratio"] = "weekly"

    # Create agent
    try:
        rule = Rules(
            name=name,
            provider_id=provider.id,
            config=json.dumps(_config),
            tasks=tasks
        )
        db.session.add(rule)
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
            message="Rule is created.",
            refresh=True
        )
    )


def update_provider_func(form, provider_id):
    provider = Providers.first(conditions=[Providers.id == provider_id])

    if provider:
        name = form.name.data.title()
        config = form.config.data

        fields = dict(name=name, config=config)

        for field, value in fields.items():
            if getattr(provider, field) != value:
                setattr(provider, field, value)

        db.session.commit()

    return response_create(
        data=dict(
            status="success",
            message="Provider updated.",
            refresh=True
        )
    )


def delete_rule_func(rule_id):
    rule = Rules.first(conditions=[Rules.id == rule_id])

    if rule:
        db.session.delete(rule)
        db.session.commit()

    return response_create(
        data=dict(
            status="success",
            message="Rule removed.",
            refresh=True
        )
    )


def delete_provider_func(provider_id):
    provider = Providers.first(conditions=[Providers.id == provider_id])

    if provider:
        if provider.rules:
            return response_create(
                data=dict(
                    status="error",
                    message="Provider has rule(s). Please remove rule(s) before."
                )
            )

        db.session.delete(provider_id)
        db.session.commit()

    return response_create(
        data=dict(
            status="success",
            message="Rule removed.",
            refresh=True
        )
    )


def update_rule_func(form, rule_id):
    rule = Rules.first(conditions=[Rules.id == rule_id])

    if rule:
        name = form.name.data.title()
        config = form.config.data
        tasks = [Tasks.first(conditions=[Tasks.id == i]) for i in form.tasks.data]

        fields = dict(name=name, config=config, tasks=tasks)

        for field, value in fields.items():
            if getattr(rule, field) != value:
                setattr(rule, field, value)

        db.session.commit()

    return response_create(
        data=dict(
            status="success",
            message="Rule updated.",
            refresh=True
        )
    )

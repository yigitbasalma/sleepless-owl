import json

from datetime import datetime, timedelta

from w import db, celery
from w.helpers.x_tools import calculate_hash, convert_string_to_bool
from w.apps.tasks.models import Tasks
from w.apps.notification.models import Rules, AlertHash

from w.adapters.slack_adapter import send as slack_send
from w.adapters.teams_adapter import send as teams_send

PROVIDERS = dict(slack=slack_send, teams=teams_send)


@celery.task
def track():
    tasks = Tasks.all(conditions=[
        Tasks.status != "up"
    ])

    for task in tasks:
        rules = Rules.all(conditions=[
            Rules.tasks.any(id=task.id)
        ])

        if convert_string_to_bool(task.maintenance_active):
            continue

        if rules:
            for rule in rules:
                rule_config = json.loads(rule.config)

                if rule_config["task-down-alerts"]:
                    notification = dict(
                        subject=f"Your task is {'failing' if task.status == 'down' else 'partially failing'} for "
                                f"{task.name} ({task.url if task.type == 'http' else task.ip_address + ':' + str(task.port)})",
                        message=f"Your task is {'failing' if task.status == 'down' else 'partially failing'} for "
                                f"{task.name} ({task.url if task.type == 'http' else task.ip_address + ':' + str(task.port)})",
                        when=datetime.now(),
                        alert_type="Monitoring Task Failure"
                    )

                    alert_hash = calculate_hash(
                        f"{notification['subject']}{notification['message']}{rule.providers.provider_name}"
                    )

                    alert_history = AlertHash.first(conditions=[AlertHash.alert_hash == alert_hash])
                    if alert_history:
                        continue

                    if not PROVIDERS.get(rule.providers.provider_name)(
                            config=json.loads(rule.providers.config), rule_config=rule_config, **notification):
                        continue
                    db.session.add(AlertHash(
                        alert_hash=alert_hash,
                        expire=datetime.now() + timedelta(seconds=task.period)
                    ))
                    db.session.commit()

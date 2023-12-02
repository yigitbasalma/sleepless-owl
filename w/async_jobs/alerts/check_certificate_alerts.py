import json

from datetime import datetime, timedelta
from urllib.parse import urlparse

from w import db, celery
from w.helpers.x_tools import calculate_hash
from w.apps.tasks.models import Tasks
from w.apps.notification.models import Rules, AlertHash

from w.adapters.slack_adapter import send as slack_send
from w.adapters.teams_adapter import send as teams_send

PROVIDERS = dict(slack=slack_send, teams=teams_send)
SEND_RATIO = dict(weekly=dict(days=7))


@celery.task
def track():
    tasks = Tasks.all(conditions=[
        Tasks.url.like("https://%"),
        Tasks.cert_valid_until.isnot(None)
    ])

    for task in tasks:
        url = urlparse(task.url)
        rules = Rules.all(conditions=[
            Rules.tasks.any(id=task.id)
        ])

        if rules:
            for rule in rules:
                rule_config = json.loads(rule.config)

                if rule_config["certificate-expire-alerts"]:
                    before_count, delta_attribute = rule_config["certificate-expire-alerts-start-before"].split("-")

                    if task.cert_valid_until <= datetime.now() + timedelta(**{delta_attribute: int(before_count)}):
                        notification = dict(
                            subject=f"Your certificate is expiring for {url.hostname}",
                            message=f"'{url.hostname}' certificate will be expired until {task.cert_valid_until}. "
                                    f"Please take your action.",
                            when=task.cert_valid_until,
                            alert_type="Certificate Expiration"
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
                            expire=datetime.now() + timedelta(**SEND_RATIO.get(rule_config["certificate-expire-alerts-send-ratio"]))
                        ))
                        db.session.commit()

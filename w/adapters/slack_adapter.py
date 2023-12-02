import json

from slack_sdk import WebClient

TEMPLATE = r"""
[
    {
        "type": "header",
        "text": {
            "type": "plain_text",
            "text": "You have a new alert for $AlertType :fire:",
            "emoji": true
        }
    },
    {
        "type": "section",
        "fields": [
            {
                "type": "mrkdwn",
                "text": "*Type:*\n$AlertType"
            },
            {
                "type": "mrkdwn",
                "text": "*When:*\n$ValidUntil"
            }
        ]
    },
    {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "*Message:*\n$Message"
        }
    }
]
"""


def send(config, rule_config, **kwargs):
    client = WebClient(token=config["api_key"])
    try:
        return client.chat_postMessage(
            as_user=True,
            username="sleepless-owl",
            channel=f'{rule_config["channel"]}',
            text=TEMPLATE
            .replace("$ValidUntil", f'{kwargs.get("when")}')
            .replace("$Message", f'{kwargs.get("message")}')
            .replace("$AlertType", f'{kwargs.get("alert_type")}'),
            blocks=json.loads(
                TEMPLATE
                .replace("$ValidUntil", f'{kwargs.get("when")}')
                .replace("$Message", f'{kwargs.get("message")}')
                .replace("$AlertType", f'{kwargs.get("alert_type")}'),
                strict=False
            )
        )
    except Exception as e:
        print(e)

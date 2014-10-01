"""
Notifier for Slackmon

Copyright (c) 2014 Brandon Huey <brandon@polytap.com>
"""

import requests
import json

import config

def slack_error(response):

    slack_error_payload = {
        "username": "Slackmon",
        'text': u"\u2602 " +
        "Problem: " + response.url +
        " " + "with status " +
        str(response.status_code)
    }

    slack_notify = requests.post(
        config.SLACK_INCOMING_WEBHOOK,
        data=json.dumps(slack_error_payload),
        headers={'content-type': 'application/json'}
    )

def slack_recovery(payload):

    slack_recovery_playload = {
        "username": "Slackmon",
        'text': u"\u2602 " +
        "Recovery: " + response.url +
        " " + "with status " +
        str(response.status_code)
    }

    slack_notify = requests.post(
        config.SLACK_INCOMING_WEBHOOK,
        data=json.dumps(slack_recovery_playload),
        headers={'content-type': 'application/json'}
    )

def hipchat_error(payload):
    pass

def hipchat_recovery(self, payload):
    pass


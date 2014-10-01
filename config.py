#!/usr/bin/env python
"""
Configuration for Slackmon

Copyright (c) 2014 Brandon Huey <brandon@polytap.com>
"""

import json

CONFIG = json.load(open('../slackmon.json'))

# Database parameters
DATABASE = {'drivername': CONFIG["database"]["drivername"],
            'host': CONFIG["database"]["host"],
            'port': CONFIG["database"]["port"],
            'username': CONFIG["database"]["username"],
            'password': CONFIG["database"]["password"],
            'database': CONFIG["database"]["database"]}

# Check parameters
URLS = CONFIG["checks"]["urls"]
TIMEOUT = float(CONFIG["checks"]["timeout"])
FREQUENCY = int(CONFIG["checks"]["frequency"])
UNIT = CONFIG["checks"]["unit"]

# Slack parameters
SLACK_USERNAME = CONFIG["slack"]["username"]
SLACK_INCOMING_WEBHOOK = CONFIG["slack"]["incoming_webhook"]



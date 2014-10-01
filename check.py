"""
Service check for Slackmon

Copyright (c) 2014 Brandon Huey <brandon@polytap.com>
"""

import grequests
import requests
import json
import datetime

import config
import db
from models import Check, db_connect, create_checks_table
import notify

from sqlalchemy.orm import sessionmaker

class CheckSites(object):

    def __init__(self):
        engine = db_connect()
        create_checks_table(engine)
        self.Session = sessionmaker(bind=engine)

    def exception_handler(self, request, exception):
        payload = {"username": "Slackmon", "text": "Timeout loading " + request.url}
        notify.slack_error(exception)

    def process_response(self, response, **kwargs):
        session = self.Session()
        is_muted = 'FALSE'
        is_up = 'TRUE' if response.status_code == 200 else 'FALSE'

        new_response = Check(url=response.url, last_status=response.status_code,
                             content_type=response.headers["Content-type"],
                             is_up=is_up, is_muted=is_muted)

        if not session.query(Check).filter_by(url=response.url).count():
            session.add(new_response)
            session.commit()
        else:
            session.query(Check).filter_by(url=response.url).update
            ({Check.last_status: response.status_code,
            Check.last_request: datetime.datetime.now(),
            Check.is_up: is_up, Check.is_muted: is_muted})
            session.commit()

        if response.status_code != 200:
            notify.slack_error(response)
            return
        else:
            #print "Check ok"
            return

    def run_checks(self):
        reqs = (grequests.get(url,
               timeout=config.TIMEOUT,
               hooks={'response' : self.process_response})
               for url in config.URLS)
        grequests.map(reqs, exception_handler=self.exception_handler)

if __name__ == '__main__':
    job = CheckSites()
    job.run_checks()


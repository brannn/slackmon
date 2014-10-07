"""
Service check for Slackmon

Copyright (c) 2014 Brandon Huey <brandon@polytap.com>
"""

import grequests
import requests
import json
import datetime
import sys

import config
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
        #notify.slack_error(exception)

    def process_response(self, response, **kwargs):
        is_muted = 'FALSE'
        is_up = 'TRUE' if response.status_code == 200 else 'FALSE'
        check_data = Check(url=response.url, last_status=response.status_code,
                           elapsed_time=response.elapsed.total_seconds(),
                           content_type=response.headers["Content-type"],
                           is_up=is_up, is_muted=is_muted)
        if not self.active_url(response):
            self.add_url(check_data)
            print "Not found"
        else:
            self.update_url(response)
        if response.status_code != 200:
            notify.slack_error(response)
            return
        else:
            return

    def run_checks(self):
        reqs = (grequests.get(url,
               timeout=config.TIMEOUT,
               hooks={'response' : self.process_response})
               for url in config.URLS)
        grequests.map(reqs, exception_handler=self.exception_handler)

    def active_url(self, response, **kwargs):
        session = self.Session()
        result = session.query(Check).filter_by(url=response.url).count()
        session.close()
        return result

    def add_url(self, check_data, **kwargs):
        sys.stdout.write("Adding untracked URL %s" % url)
        session = self.Session()
        session.add(check_data)
        session.commit()
        session.close()

    def update_url(self, response, **kwargs):
        session = self.Session()
        session.query(Check).filter_by(url=response.url).update(
            {Check.last_status: response.status_code,
            Check.elapsed_time: response.elapsed.total_seconds(),
            Check.last_request: datetime.datetime.now()})
        session.commit()
        session.close()
        sys.stdout.write("%s: Updated %s %s %s\n" %
            (datetime.datetime.now(),
            response.url,
            response.status_code,
            response.elapsed.total_seconds()))

if __name__ == '__main__':
    job = CheckSites()
    job.run_checks()


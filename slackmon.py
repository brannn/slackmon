"""
Slackmon

Copyright (c) 2014 Brandon Huey <brandon@polytap.com>
"""

import schedule
import time
import functools

import config
from check import CheckSites

def catch_exceptions(job_func):
    @functools.wraps(job_func)
    def wrapper(*args, **kwargs):
        try:
            job_func(*args, **kwargs)
        except:
            import traceback
            print(traceback.format_exc())
    return wrapper

@catch_exceptions
def job():
    j = CheckSites()
    j.run_checks()

schedule.every(config.FREQUENCY).minutes.do(job)

try:
    while True:
        schedule.run_pending()
        time.sleep(1)
except KeyboardInterrupt:
     print "\nQuitting..."
     sys.exit(2)


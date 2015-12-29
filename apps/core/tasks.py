from __future__ import absolute_import

from celery import shared_task

@shared_task(ignore_result=True)
def dummy():
    return True
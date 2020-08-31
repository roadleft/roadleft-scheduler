#-*- coding: utf-8 -*-
from django.shortcuts import render, HttpResponse
from datetime import datetime
import time
import webbrowser
from django.conf import settings
from . import models

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from django_apscheduler.jobstores import DjangoJobStore, register_events
from django_apscheduler.models import DjangoJobExecution

jobstores = {
    'default': DjangoJobStore()
}

executors = {
      'default': ThreadPoolExecutor(20), # 最多20个线程同时执行
      'processpool': ProcessPoolExecutor(5)
}

job_defaults = {
    'coalesce': False, # 相同任务触发多次
    'max_instances': 10 # 每个任务最多同时触发三次
}

scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults, timezone=settings.TIME_ZONE)
#  daemon=True,
scheduler.start()



def notify(request, ttype=None, pk=None):
    model = getattr(models, ttype.capitalize())
    obj = model.objects.get(pk=pk)
    # scheduler.add_job(tick, 'interval', seconds=10)
    context = {
        'obj': obj,
        'time': datetime.now(),
    }
    return render(request, 'clock/notify.html', context)
    # return(HttpResponse("{}, {}".format(obj.name, datetime.now())))

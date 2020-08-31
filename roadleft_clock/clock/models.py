import time
from datetime import datetime
from django.db import models
from .tasks import tasks
from .views import scheduler
import webbrowser


def hello(_type, pk):
    webbrowser.open(url="http://127.0.0.1:8000/notify/{}/{}/".format(_type, pk))
    print('Hello! The time is: %s\n' % datetime.now())


tasks = tuple(tasks)


class Date(models.Model):
    event = models.CharField(choices=tasks, max_length=20)
    name = models.CharField(max_length=200, help_text='What Event!')
    date = models.DateTimeField()
    created_time = models.DateTimeField(auto_now_add=True)
    changed_time = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        scheduler.add_job(hello, args=['date', self.pk], trigger='date', run_date=self.date, id='task_date_{}'.format(self.pk), replace_existing=True)
        # scheduler.shutdown()
        # scheduler.start()

    def delete(self, *args, **kwargs):
        '''
            fail, you know why?
        '''
        print("dfdfdfsdfsdfsdfsdfsdf")
        scheduler.remove_job('task_date_{}'.format(self.pk))
        super().delete(*args, **kwargs)    

    def pause_job(self):
        scheduler.pause_job('task_date{}'.format(self.pk))

    def resume(self):
        scheduler.resume_job('task_date{}'.format(self.pk))

    class Meta:
        verbose_name = "date"
        verbose_name_plural = "date"
        
    # timezone =  


class Interval(models.Model):
    event = models.CharField(choices=tasks, max_length=20)
    name = models.CharField(max_length=200, help_text='What Event!')
    weeks = models.SmallIntegerField(default=0, help_text='number of weeks to wait')
    days = models.SmallIntegerField(default=0,  help_text='number of days to wait')
    hours = models.SmallIntegerField(default=0, help_text='umber of hours to wait')
    minutes = models.SmallIntegerField(default=0, help_text='umber of minutes to wait')
    seconds = models.SmallIntegerField(default=0, help_text='umber of seconds to wait')
    start_date = models.DateTimeField(blank=True, null=True, help_text='starting point for the interval calculation')
    end_date = models.DateTimeField(blank=True, null=True, help_text='latest possible date/time to trigger on')
    # timezone = 
    jitter = models.SmallIntegerField(default=0, help_text="advance or delay the job execution by ``jitter`` seconds at most")
    created_time = models.DateTimeField(auto_now_add=True)
    changed_time = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        kw = {
            'weeks': self.weeks,
            'days': self.days,
            'hours': self.hours,
            'minutes': self.minutes,
            'seconds': self.seconds,
            'start_date': self.start_date if self.start_date else None,
            'end_date': self.end_date if self.end_date else None,
            'jitter': self.jitter
        }
        scheduler.add_job(hello, args=['interval', self.pk], trigger='interval', id='task_interval_{}'.format(self.pk), replace_existing=True, **kw)
        # scheduler.shutdown()
        # scheduler.start()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        scheduler.remove_job('task_interval_{}'.format(self.pk))

    def pause_job(self):
        scheduler.pause_job('task_interval_{}'.format(self.pk))

    def resume(self):
        scheduler.resume_job('task_interval_{}'.format(self.pk)) 

    class Meta:
        verbose_name = "interval"
        verbose_name_plural = "interval"
   

class Cron(models.Model):
    event = models.CharField(choices=tasks, max_length=20)
    name = models.CharField(max_length=200, help_text='What Event!')
    year = models.CharField(default='*', max_length=20, help_text="4-digit year")
    month = models.CharField(default='*', max_length=20, help_text="month (1-12)")
    day = models.CharField(default='*', max_length=20, help_text="day of the (1-31)")
    week = models.CharField(default='*', max_length=20, help_text="ISO week (1-53)")
    day_of_week = models.CharField(default='*', max_length=40, help_text="number or name of weekday (0-6 or mon,tue,wed,thu,fri,sat,sun)")
    hour = models.CharField(default='*', max_length=20, help_text="hour (0-23)")
    minute = models.CharField(default='*', max_length=20, help_text="minute (0-59)")
    second = models.CharField(default='*', max_length=20, help_text="second (0-59)")
    start_date = models.DateTimeField(blank=True, null=True, help_text="earliest possible date/time to trigger on (inclusive)")
    end_date = models.DateTimeField(blank=True, null=True, help_text="latest possible date/time to trigger on (inclusive)")
    # timezone = 
    jitter = models.SmallIntegerField(default=0, help_text="advance or delay the job execution by ``jitter`` seconds at most")
    created_time = models.DateTimeField(auto_now_add=True)
    changed_time = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        kw = {
            'year': self.year,
            'month': self.month,
            'day': self.day,
            'week': self.week,
            'day_of_week': self.day_of_week,
            'hour': self.hour,
            'minute': self.minute,
            'second': self.second,
            'start_date': self.start_date if self.start_date else None,
            'end_date': self.end_date if self.end_date else None,
            'jitter': self.jitter
        }
        scheduler.add_job(hello, args=['cron', self.pk], trigger='cron', id='task_cron_{}'.format(self.pk), replace_existing=True, **kw)
        # scheduler.shutdown()
        # scheduler.start()

    class Meta:
        verbose_name = "cron"
        verbose_name_plural = "cron"


from django.db.models.signals import pre_delete
from django.dispatch import receiver


@receiver(pre_delete, sender=Interval, dispatch_uid='interval_delete_signal')
def log_deleted_interval(sender, instance, using, **kwargs):
    print("excute delete interval")
    scheduler.remove_job('task_interval_{}'.format(instance.pk))    


@receiver(pre_delete, sender=Cron, dispatch_uid='cron_delete_signal')
def log_deleted_cron(sender, instance, using, **kwargs):
    print("excute delete interval")
    scheduler.remove_job('task_cron_{}'.format(instance.pk))              
